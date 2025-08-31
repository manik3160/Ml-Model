#!/usr/bin/env python3
"""
Content Monitoring API Server (Lite) - Flask-based API without ML dependencies

This server provides REST API endpoints for content monitoring using the lite version
of the content monitoring system.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime
from content_monitoring_lite import ContentMonitoringPipelineLite

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize content monitoring pipeline
pipeline = None

def initialize_pipeline():
    """Initialize the content monitoring pipeline"""
    global pipeline
    try:
        pipeline = ContentMonitoringPipelineLite()
        pipeline.initialize()
        logger.info("Content monitoring pipeline initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize pipeline: {e}")
        pipeline = None
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Content Monitoring API (Lite)',
        'version': '1.0.0'
    })

@app.route('/monitor/text', methods=['POST'])
def monitor_text():
    """Monitor text content for violations"""
    try:
        if pipeline is None:
            return jsonify({
                'error': 'Content monitoring pipeline not initialized',
                'status': 'error'
            }), 500
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field in request body',
                'status': 'error'
            }), 400
        
        text = data['text']
        user_id = data.get('user_id', 'unknown')
        
        if not isinstance(text, str) or len(text.strip()) == 0:
            return jsonify({
                'error': 'Text must be a non-empty string',
                'status': 'error'
            }), 400
        
        # Monitor the text content
        result = pipeline.monitor_text(text, user_id)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in monitor_text: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/monitor/batch', methods=['POST'])
def monitor_batch():
    """Monitor multiple text contents in batch"""
    try:
        if pipeline is None:
            return jsonify({
                'error': 'Content monitoring pipeline not initialized',
                'status': 'error'
            }), 500
        
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'Missing texts field in request body',
                'status': 'error'
            }), 400
        
        texts = data['texts']
        user_id = data.get('user_id', 'unknown')
        
        if not isinstance(texts, list):
            return jsonify({
                'error': 'Texts must be a list',
                'status': 'error'
            }), 400
        
        if len(texts) > 100:  # Limit batch size
            return jsonify({
                'error': 'Batch size cannot exceed 100 texts',
                'status': 'error'
            }), 400
        
        # Process each text
        results = []
        for i, text in enumerate(texts):
            if isinstance(text, str) and len(text.strip()) > 0:
                result = pipeline.monitor_text(text, f"{user_id}_batch_{i}")
                results.append({
                    'index': i,
                    'text': text[:100] + '...' if len(text) > 100 else text,
                    'result': result
                })
            else:
                results.append({
                    'index': i,
                    'text': str(text),
                    'error': 'Invalid text format'
                })
        
        return jsonify({
            'status': 'success',
            'results': results,
            'total_processed': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in monitor_batch: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/stats', methods=['GET'])
def get_statistics():
    """Get monitoring statistics"""
    try:
        if pipeline is None:
            return jsonify({
                'error': 'Content monitoring pipeline not initialized',
                'status': 'error'
            }), 500
        
        stats = pipeline.get_statistics()
        
        return jsonify({
            'status': 'success',
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_statistics: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/words/restricted', methods=['GET'])
def get_restricted_words():
    """Get list of restricted words"""
    try:
        if pipeline is None:
            return jsonify({
                'error': 'Content monitoring pipeline not initialized',
                'status': 'error'
            }), 500
        
        restricted_words = list(pipeline.text_monitor.restricted_words)
        
        return jsonify({
            'status': 'success',
            'restricted_words': restricted_words,
            'count': len(restricted_words),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_restricted_words: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/test', methods=['POST'])
def test_endpoint():
    """Test endpoint for development"""
    try:
        data = request.get_json() or {}
        text = data.get('text', 'Hello, this is a test message')
        
        if pipeline is None:
            return jsonify({
                'error': 'Content monitoring pipeline not initialized',
                'status': 'error'
            }), 500
        
        # Test the text
        result = pipeline.monitor_text(text, 'test_user')
        
        return jsonify({
            'status': 'success',
            'test_text': text,
            'result': result,
            'message': 'Test completed successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in test_endpoint: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': [
            'GET /health',
            'POST /monitor/text',
            'POST /monitor/batch',
            'GET /stats',
            'GET /words/restricted',
            'POST /test'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Content Monitoring API Server (Lite)...")
    print("=" * 60)
    print("Available endpoints:")
    print("  GET  /health              - Health check")
    print("  POST /monitor/text        - Monitor single text")
    print("  POST /monitor/batch       - Monitor multiple texts")
    print("  GET  /stats               - Get statistics")
    print("  GET  /words/restricted    - Get restricted words")
    print("  POST /test                - Test endpoint")
    print("=" * 60)
    print("Server will run on http://localhost:5002")
    print("=" * 60)
    
    try:
        # Initialize pipeline before starting server
        pipeline = ContentMonitoringPipelineLite()
        pipeline.initialize()
        print("✅ Content monitoring pipeline initialized")
        
        # Start the server
        app.run(
            host='0.0.0.0',
            port=5002,
            debug=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        exit(1)
