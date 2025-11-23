"""
TIBCO BW XPath Parser
Extracts XPath expressions from TIBCO BusinessWorks process files
"""

import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Any
import uuid


class XPathParser:
    """Parser for TIBCO BW process files to extract XPath expressions"""
    
    def __init__(self):
        self.namespaces = {
            'bw': 'http://www.tibco.com/xmlns/bw/process/2003',
            'xsl': 'http://www.w3.org/1999/XSL/Transform',
            'tibco': 'http://www.tibco.com/xmlns/aemeta/services/2002'
        }
    
    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """
        Parse TIBCO BW file and extract all XPath expressions
        
        Args:
            filepath: Path to the BW process file
            
        Returns:
            Dictionary with metadata and list of XPath expressions
        """
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            metadata = self._extract_metadata(root)
            xpaths = self._extract_xpaths(root)
            
            return {
                'metadata': metadata,
                'xpaths': xpaths
            }
            
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML file: {str(e)}")
    
    def _extract_metadata(self, root: ET.Element) -> Dict[str, Any]:
        """Extract process-level metadata"""
        metadata = {
            'process_name': root.get('name', 'Unknown'),
            'description': '',
            'variables': [],
            'schemas': []
        }
        
        # Try to find process description
        desc_elem = root.find('.//description')
        if desc_elem is not None and desc_elem.text:
            metadata['description'] = desc_elem.text.strip()
        
        # Extract process variables
        for var in root.findall('.//processVariables'):
            var_name = var.get('name', '')
            var_type = var.get('type', '')
            if var_name:
                metadata['variables'].append({
                    'name': var_name,
                    'type': var_type
                })
        
        return metadata
    
    def _extract_xpaths(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Extract all XPath expressions from the process"""
        xpaths = []
        
        # Find XPath in mapper activities
        for mapper in root.findall('.//mapping'):
            xpath_expr = mapper.get('expression', '')
            if xpath_expr and self._is_xpath(xpath_expr):
                xpaths.append({
                    'id': str(uuid.uuid4()),
                    'expression': xpath_expr,
                    'location': 'Mapper',
                    'activity': mapper.get('target', 'Unknown'),
                    'context': self._extract_context(mapper)
                })
        
        # Find XPath in transition conditions
        for transition in root.findall('.//transition'):
            condition = transition.get('condition', '')
            if condition and self._is_xpath(condition):
                xpaths.append({
                    'id': str(uuid.uuid4()),
                    'expression': condition,
                    'location': 'Transition Condition',
                    'activity': transition.get('to', 'Unknown'),
                    'context': {'type': 'condition'}
                })
        
        # Find XPath in activity configurations
        for activity in root.findall('.//config'):
            xpath_expr = activity.text
            if xpath_expr and self._is_xpath(xpath_expr.strip()):
                xpaths.append({
                    'id': str(uuid.uuid4()),
                    'expression': xpath_expr.strip(),
                    'location': 'Activity Configuration',
                    'activity': activity.get('name', 'Unknown'),
                    'context': {}
                })
        
        # Find XPath in text content (common in BW files)
        for elem in root.iter():
            if elem.text and self._is_xpath(elem.text.strip()):
                # Avoid duplicates
                if not any(x['expression'] == elem.text.strip() for x in xpaths):
                    xpaths.append({
                        'id': str(uuid.uuid4()),
                        'expression': elem.text.strip(),
                        'location': f'{elem.tag}',
                        'activity': elem.get('name', 'Unknown'),
                        'context': {}
                    })
        
        return xpaths
    
    def _is_xpath(self, text: str) -> bool:
        """Check if a string looks like an XPath expression"""
        if not text or len(text) < 3:
            return False
        
        xpath_indicators = [
            '/', '@', '[', ']', 
            'text()', 'node()', 
            'ancestor::', 'child::', 'parent::',
            'following::', 'preceding::',
            'count(', 'sum(', 'concat(',
            'substring(', 'string(',
            '$'  # variable reference
        ]
        
        return any(indicator in text for indicator in xpath_indicators)
    
    def _extract_context(self, element: ET.Element) -> Dict[str, Any]:
        """Extract contextual information about the XPath"""
        context = {}
        
        # Get source and target information
        context['source'] = element.get('source', '')
        context['target'] = element.get('target', '')
        context['type'] = element.get('type', 'mapping')
        
        # Look for schema references
        schema_ref = element.get('schemaRef', '')
        if schema_ref:
            context['schema'] = schema_ref
        
        return context
