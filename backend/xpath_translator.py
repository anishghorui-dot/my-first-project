"""
XPath to Plain Language Translator
Converts XPath expressions into human-readable descriptions
"""

import re
from typing import Dict, List, Any


class XPathTranslator:
    """Translates XPath expressions to plain language"""
    
    def __init__(self):
        self.operators = {
            '=': 'equals',
            '!=': 'does not equal',
            '>': 'is greater than',
            '>=': 'is greater than or equal to',
            '<': 'is less than',
            '<=': 'is less than or equal to',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT'
        }
        
        self.functions = {
            'count': 'count the number of',
            'sum': 'calculate the sum of',
            'concat': 'combine',
            'substring': 'extract part of',
            'string': 'convert to text',
            'number': 'convert to number',
            'boolean': 'convert to true/false',
            'contains': 'contains',
            'starts-with': 'starts with',
            'string-length': 'get the length of',
            'normalize-space': 'remove extra spaces from',
            'translate': 'replace characters in',
            'upper-case': 'convert to uppercase',
            'lower-case': 'convert to lowercase'
        }
    
    def translate(self, xpath: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Translate XPath expression to plain language
        
        Args:
            xpath: XPath expression to translate
            context: Additional context about the expression
            
        Returns:
            Dictionary with translation and metadata
        """
        context = context or {}
        
        # Clean up the XPath
        xpath = xpath.strip()
        
        # Determine the type of XPath expression
        expr_type = self._determine_type(xpath)
        
        # Generate description based on type
        if expr_type == 'selection':
            description = self._translate_selection(xpath, context)
        elif expr_type == 'condition':
            description = self._translate_condition(xpath, context)
        elif expr_type == 'function':
            description = self._translate_function(xpath, context)
        elif expr_type == 'variable':
            description = self._translate_variable(xpath, context)
        else:
            description = self._translate_generic(xpath, context)
        
        # Break down into steps
        steps = self._generate_steps(xpath, context)
        
        # Determine confidence level
        confidence = self._calculate_confidence(xpath)
        
        return {
            'description': description,
            'steps': steps,
            'confidence': confidence,
            'type': expr_type,
            'data_flow': self._extract_data_flow(xpath, context)
        }
    
    def _determine_type(self, xpath: str) -> str:
        """Determine the type of XPath expression"""
        if xpath.startswith('$'):
            return 'variable'
        elif any(op in xpath for op in ['=', '!=', '>', '<', ' and ', ' or ']):
            return 'condition'
        elif any(f'{func}(' in xpath for func in self.functions.keys()):
            return 'function'
        else:
            return 'selection'
    
    def _translate_selection(self, xpath: str, context: Dict) -> str:
        """Translate path selection XPath"""
        # Remove leading slash
        path = xpath.lstrip('/')
        
        # Split by slashes to get path components
        parts = [p for p in path.split('/') if p]
        
        if not parts:
            return "Select the root element"
        
        # Build human-readable path
        readable_parts = []
        for part in parts:
            # Handle predicates [...]
            if '[' in part:
                base, predicate = part.split('[', 1)
                predicate = predicate.rstrip(']')
                readable_parts.append(
                    f"{self._humanize_name(base)} where {self._translate_predicate(predicate)}"
                )
            # Handle attributes @name
            elif part.startswith('@'):
                attr_name = part[1:]
                readable_parts.append(f"the {self._humanize_name(attr_name)} attribute")
            # Handle text()
            elif part == 'text()':
                readable_parts.append("the text content")
            # Regular element
            else:
                readable_parts.append(self._humanize_name(part))
        
        # Build final description
        if len(readable_parts) == 1:
            return f"Select {readable_parts[0]}"
        else:
            path_desc = " → ".join(readable_parts)
            return f"Navigate to: {path_desc}"
    
    def _translate_condition(self, xpath: str, context: Dict) -> str:
        """Translate conditional XPath"""
        # Handle simple comparisons
        for op, op_text in self.operators.items():
            if op in xpath:
                parts = xpath.split(op, 1)
                if len(parts) == 2:
                    left = self._translate_operand(parts[0].strip())
                    right = self._translate_operand(parts[1].strip())
                    return f"Check if {left} {op_text} {right}"
        
        # Handle logical operators
        if ' and ' in xpath.lower():
            conditions = re.split(r'\s+and\s+', xpath, flags=re.IGNORECASE)
            translated = [self._translate_condition(c.strip(), context) for c in conditions]
            return " AND ".join(translated)
        
        if ' or ' in xpath.lower():
            conditions = re.split(r'\s+or\s+', xpath, flags=re.IGNORECASE)
            translated = [self._translate_condition(c.strip(), context) for c in conditions]
            return " OR ".join(translated)
        
        return f"Evaluate condition: {xpath}"
    
    def _translate_function(self, xpath: str, context: Dict) -> str:
        """Translate function calls"""
        for func_name, func_desc in self.functions.items():
            pattern = f'{func_name}\\(([^)]+)\\)'
            match = re.search(pattern, xpath)
            if match:
                args = match.group(1)
                arg_desc = self._humanize_name(args)
                
                if func_name in ['count', 'sum', 'string-length']:
                    return f"{func_desc.capitalize()} {arg_desc}"
                elif func_name == 'concat':
                    arg_parts = [a.strip().strip("'\"") for a in args.split(',')]
                    return f"Combine: {' + '.join(arg_parts)}"
                elif func_name == 'substring':
                    return f"Extract part of {arg_desc}"
                elif func_name in ['contains', 'starts-with']:
                    arg_parts = [a.strip().strip("'\"") for a in args.split(',', 1)]
                    if len(arg_parts) == 2:
                        return f"Check if {arg_parts[0]} {func_desc} '{arg_parts[1]}'"
                else:
                    return f"{func_desc.capitalize()} {arg_desc}"
        
        return f"Apply function: {xpath}"
    
    def _translate_variable(self, xpath: str, context: Dict) -> str:
        """Translate variable references"""
        var_name = xpath.lstrip('$')
        if '/' in var_name:
            parts = var_name.split('/')
            var_base = parts[0]
            path = ' → '.join(self._humanize_name(p) for p in parts[1:])
            return f"Get {path} from variable '{var_base}'"
        else:
            return f"Use the value of variable '{var_name}'"
    
    def _translate_generic(self, xpath: str, context: Dict) -> str:
        """Generic translation fallback"""
        return f"XPath expression: {self._humanize_name(xpath)}"
    
    def _translate_predicate(self, predicate: str) -> str:
        """Translate predicate expressions inside []"""
        # Handle position predicates
        if predicate.isdigit():
            return f"position {predicate}"
        
        # Handle last()
        if predicate == 'last()':
            return "the last item"
        
        # Handle conditions
        if any(op in predicate for op in self.operators.keys()):
            return self._translate_condition(predicate, {})
        
        return predicate
    
    def _translate_operand(self, operand: str) -> str:
        """Translate operand in a condition"""
        operand = operand.strip()
        
        # String literal
        if (operand.startswith("'") and operand.endswith("'")) or \
           (operand.startswith('"') and operand.endswith('"')):
            return operand.strip("'\"")
        
        # Number
        if operand.replace('.', '').isdigit():
            return operand
        
        # Variable
        if operand.startswith('$'):
            return f"variable {operand[1:]}"
        
        # Path
        return self._humanize_name(operand)
    
    def _humanize_name(self, name: str) -> str:
        """Convert technical names to human-readable format"""
        # Remove namespace prefixes
        if ':' in name:
            name = name.split(':', 1)[1]
        
        # Handle camelCase and PascalCase
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        
        # Handle snake_case
        name = name.replace('_', ' ')
        
        # Handle kebab-case
        name = name.replace('-', ' ')
        
        # Lowercase and clean up
        name = name.lower().strip()
        
        return name if name else 'unknown'
    
    def _generate_steps(self, xpath: str, context: Dict) -> List[str]:
        """Break down XPath into step-by-step instructions"""
        steps = []
        
        # For path expressions, break down by /
        if '/' in xpath and not xpath.startswith('$'):
            parts = [p for p in xpath.split('/') if p]
            for i, part in enumerate(parts, 1):
                if part.startswith('@'):
                    steps.append(f"Step {i}: Access the {self._humanize_name(part[1:])} attribute")
                elif '[' in part:
                    base = part.split('[')[0]
                    steps.append(f"Step {i}: Select {self._humanize_name(base)} with specific criteria")
                else:
                    steps.append(f"Step {i}: Navigate to {self._humanize_name(part)}")
        
        return steps
    
    def _calculate_confidence(self, xpath: str) -> str:
        """Calculate confidence level of translation"""
        # High confidence for simple paths and common patterns
        if xpath.count('/') <= 2 and '[' not in xpath and not any(op in xpath for op in self.operators.keys()):
            return 'high'
        
        # Low confidence for complex nested expressions
        if xpath.count('[') > 2 or xpath.count('(') > 3:
            return 'low'
        
        return 'medium'
    
    def _extract_data_flow(self, xpath: str, context: Dict) -> Dict[str, Any]:
        """Extract data flow information"""
        return {
            'source': context.get('source', 'Unknown'),
            'target': context.get('target', 'Unknown'),
            'operation': self._determine_type(xpath)
        }
