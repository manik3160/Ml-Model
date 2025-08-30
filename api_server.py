#!/usr/bin/env python3
"""
API Server for Content Monitoring ML Model

This Flask server wraps your existing ML model to provide HTTP API endpoints
for your Next.js application. It doesn't change any code in your ML model.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from content_monitoring_system import monitor_social_media_content, ContentFilteringPipeline
import base64
import io
from PIL import Image
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js

# Initialize the pipeline once (global instance)
pipeline = None

def initialize_pipeline():
    """Initialize the ML pipeline once"""
    global pipeline
    try:
        pipeline = ContentFilteringPipeline()
        pipeline.text_monitor.load_restricted_words()
        logger.info("ML Pipeline initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize ML Pipeline: {e}")
        return False

@app.route('/api/check-content', methods=['POST'])
def check_content():
    """Check content using your existing ML model"""
    try:
        # Ensure pipeline is initialized
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        text_content = data.get('text', '')
        image_base64 = data.get('image', None)
        user_id = data.get('user_id', None)
        
        # Validate input
        if not text_content and not image_base64:
            return jsonify({'error': 'Either text or image must be provided'}), 400
        
        # Convert base64 image to bytes if provided
        image_data = None
        if image_base64:
            try:
                # Remove data URL prefix if present
                if ',' in image_base64:
                    image_base64 = image_base64.split(',')[1]
                
                image_data = base64.b64decode(image_base64)
                logger.info(f"Image decoded successfully for user: {user_id}")
            except Exception as e:
                logger.error(f"Failed to decode image: {e}")
                return jsonify({'error': 'Invalid image format'}), 400
        
        # Use your existing ML model (NO CHANGES NEEDED)
        logger.info(f"Checking content for user: {user_id}")
        result = monitor_social_media_content(
            text_content=text_content,
            image_path=image_data,
            user_id=user_id,
            pipeline=pipeline
        )
        
        logger.info(f"Content check completed for user: {user_id}, decision: {result.get('overall_decision')}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in content check: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-text-only', methods=['POST'])
def check_text_only():
    """Check only text content (faster for text-only posts)"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        text_content = data.get('text', '')
        user_id = data.get('user_id', None)
        
        if not text_content:
            return jsonify({'error': 'Text content is required'}), 400
        
        # Use your existing ML model (NO CHANGES NEEDED)
        logger.info(f"Checking text content for user: {user_id}")
        result = monitor_social_media_content(
            text_content=text_content,
            user_id=user_id,
            pipeline=pipeline
        )
        
        logger.info(f"Text check completed for user: {user_id}, decision: {result.get('overall_decision')}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in text check: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-image-only', methods=['POST'])
def check_image_only():
    """Check only image content"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        image_base64 = data.get('image', None)
        user_id = data.get('user_id', None)
        
        if not image_base64:
            return jsonify({'error': 'Image is required'}), 400
        
        # Convert base64 image to bytes
        try:
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            
            image_data = base64.b64decode(image_base64)
            logger.info(f"Image decoded successfully for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to decode image: {e}")
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Use your existing ML model (NO CHANGES NEEDED)
        logger.info(f"Checking image content for user: {user_id}")
        result = monitor_social_media_content(
            image_path=image_data,
            user_id=user_id,
            pipeline=pipeline
        )
        
        logger.info(f"Image check completed for user: {user_id}, decision: {result.get('overall_decision')}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in image check: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({
                    'status': 'unhealthy',
                    'message': 'ML Pipeline failed to initialize',
                    'ml_model_ready': False
                }), 500
        
        return jsonify({
            'status': 'healthy',
            'message': 'ML Model API is running',
            'ml_model_ready': True,
            'endpoints': [
                '/api/check-content',
                '/api/check-text-only',
                '/api/check-image-only',
                '/api/health'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Health check failed: {str(e)}',
            'ml_model_ready': False
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get content monitoring statistics"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        stats = pipeline.get_statistics()
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET', 'PUT'])
def manage_config():
    """Get or update configuration"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        if request.method == 'GET':
            return jsonify(pipeline.config)
        
        elif request.method == 'PUT':
            data = request.json
            if not data:
                return jsonify({'error': 'No configuration data provided'}), 400
            
            pipeline.update_config(data)
            return jsonify({
                'message': 'Configuration updated successfully',
                'config': pipeline.config
            })
    
    except Exception as e:
        logger.error(f"Error managing config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restricted-words', methods=['GET', 'POST'])
def manage_restricted_words():
    """Get or add restricted words"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        if request.method == 'GET':
            return jsonify({
                'restricted_words': list(pipeline.text_monitor.restricted_words),
                'count': len(pipeline.text_monitor.restricted_words)
            })
        
        elif request.method == 'POST':
            data = request.json
            if not data or 'words' not in data:
                return jsonify({'error': 'Words list is required'}), 400
            
            new_words = data['words']
            if isinstance(new_words, str):
                new_words = [new_words]
            
            pipeline.text_monitor.restricted_words.update(new_words)
            return jsonify({
                'message': f'Added {len(new_words)} new restricted words',
                'total_count': len(pipeline.text_monitor.restricted_words)
            })
    
    except Exception as e:
        logger.error(f"Error managing restricted words: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restricted-words/update-from-api', methods=['POST'])
def update_restricted_words_from_api():
    """Update restricted words by testing against the Bad Words API"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        data = request.json or {}
        words_to_test = data.get('words_to_test', None)
        
        # Update restricted words from API
        api_confirmed_words = pipeline.text_monitor.update_restricted_words_from_api(words_to_test)
        
        return jsonify({
            'message': 'Restricted words updated from Bad Words API',
            'api_confirmed_words': list(api_confirmed_words) if api_confirmed_words else [],
            'total_count': len(pipeline.text_monitor.restricted_words),
            'method': 'api_enhanced'
        })
    
    except Exception as e:
        logger.error(f"Error updating restricted words from API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-text-with-api', methods=['POST'])
def check_text_with_api():
    """Check text content using the Bad Words API for enhanced validation"""
    try:
        if pipeline is None:
            if not initialize_pipeline():
                return jsonify({'error': 'ML Pipeline not available'}), 500
        
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required'}), 400
        
        text_content = data.get('text', '')
        user_id = data.get('user_id', None)
        
        # Use API-enhanced text checking
        result = pipeline.text_monitor.check_text_with_api(text_content)
        
        # Add user context if provided
        if user_id:
            result['user_id'] = user_id
        
        # Format response similar to main content check
        if result.get('combined_decision', False):
            result['action'] = 'block'
            result['message'] = 'Content blocked due to policy violation'
            result['overall_decision'] = 'unsafe'
        else:
            result['action'] = 'allow'
            result['message'] = 'Content approved'
            result['overall_decision'] = 'safe'
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in API-enhanced text check: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize pipeline on startup
    if initialize_pipeline():
        logger.info("Starting Content Monitoring API Server...")
        logger.info("Available endpoints:")
        logger.info("  POST /api/check-content     - Check text and/or image content")
        logger.info("  POST /api/check-text-only   - Check text content only")
        logger.info("  POST /api/check-image-only  - Check image content only")
        logger.info("  GET  /api/health            - Health check")
        logger.info("  GET  /api/stats             - Get statistics")
        logger.info("  GET  /api/config            - Get configuration")
        logger.info("  PUT  /api/config            - Update configuration")
        logger.info("  GET  /api/restricted-words  - Get restricted words")
        logger.info("  POST /api/restricted-words  - Add restricted words")
        logger.info("  POST /api/restricted-words/update-from-api - Update from Bad Words API")
        logger.info("  POST /api/check-text-with-api - Enhanced text check with API")
        
        # Start the server
        app.run(
            host='0.0.0.0',  # Allow external connections
            port=5001,        # Port 5001 (avoiding macOS AirPlay conflict)
            debug=False,      # Production mode
            threaded=True     # Handle multiple requests
        )
    else:
        logger.error("Failed to initialize ML Pipeline. Server not started.")
        exit(1)
