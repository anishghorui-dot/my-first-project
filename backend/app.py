"""
TIBCO BW XPath to Plain Language Translator - Backend API
Flask application that parses TIBCO BW files and translates XPath expressions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from xpath_parser import XPathParser
from xpath_translator import XPathTranslator

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'xml', 'process', 'bwp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

parser = XPathParser()
translator = XPathTranslator()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'xpath-translator'})


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload TIBCO BW file for processing
    Returns: file_id and basic metadata
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: XML, PROCESS, BWP'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse file to extract XPath expressions
        parsed_data = parser.parse_file(filepath)
        
        return jsonify({
            'file_id': filename,
            'original_name': file.filename,
            'xpath_count': len(parsed_data.get('xpaths', [])),
            'metadata': parsed_data.get('metadata', {})
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500


@app.route('/api/translate', methods=['POST'])
def translate_xpath():
    """
    Translate specific XPath expression to plain language
    Body: { "xpath": "...", "context": {...} }
    """
    data = request.get_json()
    
    if not data or 'xpath' not in data:
        return jsonify({'error': 'XPath expression required'}), 400
    
    try:
        xpath_expr = data['xpath']
        context = data.get('context', {})
        
        translation = translator.translate(xpath_expr, context)
        
        return jsonify({
            'xpath': xpath_expr,
            'plain_language': translation['description'],
            'steps': translation.get('steps', []),
            'confidence': translation.get('confidence', 'medium'),
            'data_flow': translation.get('data_flow', {})
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500


@app.route('/api/parse/<file_id>', methods=['GET'])
def parse_file(file_id):
    """
    Get all XPath expressions from a previously uploaded file
    Returns: list of XPath expressions with metadata
    """
    try:
        filename = secure_filename(file_id)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        parsed_data = parser.parse_file(filepath)
        
        # Translate all XPath expressions
        results = []
        for xpath_item in parsed_data.get('xpaths', []):
            translation = translator.translate(
                xpath_item['expression'],
                xpath_item.get('context', {})
            )
            
            results.append({
                'id': xpath_item['id'],
                'xpath': xpath_item['expression'],
                'plain_language': translation['description'],
                'location': xpath_item.get('location', ''),
                'activity': xpath_item.get('activity', ''),
                'steps': translation.get('steps', []),
                'confidence': translation.get('confidence', 'medium'),
                'context': xpath_item.get('context', {})
            })
        
        return jsonify({
            'file_id': file_id,
            'metadata': parsed_data.get('metadata', {}),
            'translations': results,
            'total_count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Parsing failed: {str(e)}'}), 500


@app.route('/api/batch-translate', methods=['POST'])
def batch_translate():
    """
    Translate multiple XPath expressions at once
    Body: { "xpaths": [{"expr": "...", "context": {...}}, ...] }
    """
    data = request.get_json()
    
    if not data or 'xpaths' not in data:
        return jsonify({'error': 'XPath list required'}), 400
    
    try:
        results = []
        for item in data['xpaths']:
            translation = translator.translate(
                item['expr'],
                item.get('context', {})
            )
            results.append({
                'xpath': item['expr'],
                'plain_language': translation['description'],
                'steps': translation.get('steps', []),
                'confidence': translation.get('confidence', 'medium')
            })
        
        return jsonify({'translations': results}), 200
        
    except Exception as e:
        return jsonify({'error': f'Batch translation failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
