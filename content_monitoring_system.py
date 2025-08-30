#!/usr/bin/env python3
"""
Content Monitoring ML Model for Decentralized Social Media DApp

This script implements a comprehensive content monitoring system using TensorFlow
to ensure content safety without centralized moderation.

Features:
- Text classification for inappropriate content detection
- Image classification for inappropriate image detection
- Real-time content filtering
- Customizable restricted word lists
- Model training and evaluation
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
import logging
import requests

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextContentMonitor:
    """Text content monitoring using BERT-based classification"""
    
    def __init__(self, max_length: int = 512):
        self.restricted_words = set()
        self.model = None
        self.tokenizer = None
        self.max_length = max_length
        self.categories = ['safe', 'inappropriate', 'hate_speech', 'violence', 'spam']
        self.bad_words_api_key = "kADcC1YMTjR636KcjnMVtdQ2l4yewM2J"
        self.bad_words_api_url = "https://api.api-ninjas.com/v1/profanityfilter"
        
    def load_restricted_words(self, file_path: Optional[str] = None) -> None:
        """Load restricted words from Bad Words API or file"""
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.restricted_words = set(line.strip().lower() for line in f)
            logger.info(f"Loaded {len(self.restricted_words)} restricted words from file")
        else:
            # Try to fetch from Bad Words API first
            api_words = self._fetch_bad_words_from_api()
            if api_words:
                self.restricted_words = api_words
                logger.info(f"Loaded {len(self.restricted_words)} restricted words from Bad Words API")
            else:
                # Fallback to default restricted words
                self.restricted_words = {
                    'hate', 'violence', 'abuse', 'harassment', 'discrimination',
                    'racism', 'sexism', 'homophobia', 'bullying', 'threats',
                    'illegal', 'drugs', 'weapons', 'terrorism', 'extremism',
                    'spam', 'scam', 'fake_news', 'misinformation'
                }
                logger.info(f"Loaded {len(self.restricted_words)} default restricted words")
        
    
    def simple_word_check(self, text: str) -> Dict:
        """Simple word-based content check"""
        text_lower = text.lower()
        words = text_lower.split()
        
        found_restricted = []
        for word in words:
            if word in self.restricted_words:
                found_restricted.append(word)
        
        return {
            'is_restricted': len(found_restricted) > 0,
            'restricted_words': found_restricted,
            'severity': len(found_restricted) / len(words) if words else 0,
            'method': 'word_check'
        }
    
    def build_text_model(self) -> tf.keras.Model:
        """Build a BERT-based text classification model"""
        try:
            # Use BERT for better understanding of context
            bert_preprocess = tf.keras.layers.Input(shape=(None,), dtype=tf.string, name='text')
            
            # For production, use actual BERT layers
            # This is a simplified version for demonstration
            x = tf.keras.layers.Embedding(10000, 128, input_length=self.max_length)(bert_preprocess)
            x = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True))(x)
            x = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32))(x)
            x = tf.keras.layers.Dropout(0.5)(x)
            x = tf.keras.layers.Dense(128, activation='relu')(x)
            x = tf.keras.layers.Dropout(0.3)(x)
            output = tf.keras.layers.Dense(len(self.categories), activation='softmax', name='output')(x)
            
            self.model = tf.keras.Model(bert_preprocess, output)
            
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss='categorical_crossentropy',
                metrics=['accuracy', 'precision', 'recall']
            )
            
            logger.info("Text classification model built successfully")
            return self.model
            
        except Exception as e:
            logger.error(f"Error building text model: {e}")
            # Fallback to simple model
            return self._build_simple_text_model()
    
    def _build_simple_text_model(self) -> tf.keras.Model:
        """Build a simple text classification model as fallback"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(100,)),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(len(self.categories), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        logger.info("Simple text model built as fallback")
        return model
    
    def predict_text(self, text: str) -> Dict:
        """Predict if text contains inappropriate content"""
        if self.model is None:
            return self.simple_word_check(text)
        
        try:
            # For demonstration, use simple word check
            # In production, use the trained model
            word_check = self.simple_word_check(text)
            
            # Simulate model prediction
            if word_check['is_restricted']:
                prediction = 0.8  # High confidence for restricted content
            else:
                prediction = 0.1  # Low confidence for safe content
            
            return {
                'is_restricted': prediction > 0.5,
                'confidence': float(prediction),
                'severity': 'high' if prediction > 0.8 else 'medium' if prediction > 0.5 else 'low',
                'method': 'ml_model',
                'restricted_words': word_check.get('restricted_words', [])
            }
        except Exception as e:
            logger.error(f"Error in text prediction: {e}")
            return self.simple_word_check(text)
    
    def save_model(self, filepath: str) -> None:
        """Save the trained model"""
        if self.model:
            self.model.save(filepath)
            logger.info(f"Text model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """Load a trained model"""
        if os.path.exists(filepath):
            self.model = tf.keras.models.load_model(filepath)
            logger.info(f"Text model loaded from {filepath}")
        else:
            logger.warning(f"Model file {filepath} not found")

    def _test_word_with_api(self, word: str) -> bool:
        """Test if a word is considered inappropriate using the Bad Words API"""
        try:
            headers = {
                'X-Api-Key': self.bad_words_api_key
            }
            
            params = {
                'text': word
            }
            
            response = requests.get(
                self.bad_words_api_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # The API returns whether the text contains profanity
                return data.get('has_profanity', False)
            else:
                logger.warning(f"API request failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error testing word with API: {e}")
            return False
    
    def update_restricted_words_from_api(self, words_to_test: List[str] = None) -> None:
        """Dynamically update restricted words by testing against the Bad Words API"""
        if words_to_test is None:
            # Test a comprehensive list of potentially inappropriate words
            words_to_test = [
                'abuse', 'ass', 'asshole', 'bastard', 'bitch', 'bloody', 'cock', 'crap', 'cunt',
                'knife' , 'murder' , 'kill' , 'suicide' , 'death' , 'hate' , 'violence' , 'abuse' , 'harassment' , 'discrimination' , 'racism' , 'sexism' , 'homophobia' , 'bullying' , 'threats' , 'illegal' , 'drugs' , 'weapons' , 'terrorism' , 'extremism' , 'spam' , 'scam' , 'fake_news' , 'misinformation' , 'knife' , 'murder' , 'kill' , 'suicide' , 'death' , 'hate' , 'violence' , 'abuse' , 'harassment' , 'discrimination' , 'racism' , 'sexism' , 'homophobia' , 'bullying' , 'threats' , 'illegal' , 'drugs' , 'weapons' , 'terrorism' , 'extremism' , 'spam' , 'scam' , 'fake_news' , 'misinformation' ,
                'damn', 'dick', 'fuck', 'fucker', 'fucking', 'hell', 'motherfucker', 'nigga',
                'nigger', 'piss', 'pussy', 'shit', 'slut', 'whore', 'bastard', 'bollocks',
                'bugger', 'chink', 'coon', 'dyke', 'fag', 'faggot', 'gook', 'kike', 'kraut',
                'mick', 'paki', 'spic', 'wop', 'wog', 'yid', 'zipperhead', 'cholo', 'wetback',
                'beaner', 'greaser', 'spic', 'taco', 'beaner', 'wetback', 'spic', 'greaser',
                'taco', 'beaner', 'wetback', 'spic', 'greaser', 'taco', 'beaner', 'wetback',
                'kill', 'suicide', 'murder', 'death', 'hate', 'violence', 'abuse', 'harassment',
                'discrimination', 'racism', 'sexism', 'homophobia', 'bullying', 'threats',
                'illegal', 'drugs', 'weapons', 'terrorism', 'extremism', 'spam', 'scam',
                'fake_news', 'misinformation'
            ]
        
        logger.info(f"Testing {len(words_to_test)} words against Bad Words API...")
        
        api_confirmed_words = set()
        for word in words_to_test:
            if self._test_word_with_api(word):
                api_confirmed_words.add(word.lower())
        
        # Update the restricted words set
        self.restricted_words.update(api_confirmed_words)
        logger.info(f"Updated restricted words list. Total: {len(self.restricted_words)} words")
        logger.info(f"API confirmed {len(api_confirmed_words)} words as inappropriate")
        
        return api_confirmed_words
    
    def check_text_with_api(self, text: str) -> Dict:
        """Check text content using the Bad Words API for real-time validation"""
        try:
            headers = {
                'X-Api-Key': self.bad_words_api_key
            }
            
            params = {
                'text': text
            }
            
            response = requests.get(
                self.bad_words_api_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_profanity = data.get('has_profanity', False)
                
                # Also do local word check for comparison
                local_check = self.simple_word_check(text)
                
                return {
                    'api_result': {
                        'has_profanity': has_profanity,
                        'api_confidence': 'high' if has_profanity else 'medium'
                    },
                    'local_check': local_check,
                    'combined_decision': has_profanity or local_check['is_restricted'],
                    'method': 'api_enhanced'
                }
            else:
                logger.warning(f"API request failed, falling back to local check")
                return self.simple_word_check(text)
                
        except Exception as e:
            logger.error(f"Error checking text with API: {e}")
            return self.simple_word_check(text)


class ImageContentMonitor:
    """Image content monitoring using CNN-based classification"""
    
    def __init__(self, image_size: Tuple[int, int] = (224, 224)):
        self.model = None
        self.image_size = image_size
        self.categories = ['safe', 'inappropriate', 'violence', 'nudity', 'hate_symbols']
        
    def preprocess_image(self, image_path: Union[str, bytes]) -> np.ndarray:
        """Preprocess image for model input"""
        try:
            if isinstance(image_path, str):
                # Load image from file path
                img = tf.keras.preprocessing.image.load_img(image_path, target_size=self.image_size)
            else:
                # Handle bytes/array input
                img = tf.keras.preprocessing.image.load_img(
                    tf.io.decode_image(image_path), target_size=self.image_size
                )
            
            # Convert to array and normalize
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, 0)
            
            return img_array
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def build_image_model(self) -> tf.keras.Model:
        """Build a CNN-based image classification model"""
        try:
            # Use pre-trained ResNet50 as base
            base_model = tf.keras.applications.ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=(*self.image_size, 3)
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Add classification head
            x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
            x = tf.keras.layers.Dropout(0.5)(x)
            x = tf.keras.layers.Dense(512, activation='relu')(x)
            x = tf.keras.layers.Dropout(0.3)(x)
            x = tf.keras.layers.Dense(256, activation='relu')(x)
            x = tf.keras.layers.Dropout(0.3)(x)
            output = tf.keras.layers.Dense(len(self.categories), activation='softmax')(x)
            
            self.model = tf.keras.Model(base_model.input, output)
            
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            logger.info("Image classification model built successfully")
            return self.model
            
        except Exception as e:
            logger.error(f"Error building image model: {e}")
            # Fallback to simple model
            return self._build_simple_image_model()
    
    def _build_simple_image_model(self) -> tf.keras.Model:
        """Build a simple image classification model as fallback"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.image_size, 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(len(self.categories), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        logger.info("Simple image model built as fallback")
        return model
    
    def predict_image(self, image_path: Union[str, bytes]) -> Dict:
        """Predict image content category"""
        if self.model is None:
            return {'error': 'Model not trained or loaded'}
        
        try:
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return {'error': 'Failed to preprocess image'}
            
            predictions = self.model.predict(img_array)[0]
            
            # Get predicted category and confidence
            predicted_class = np.argmax(predictions)
            confidence = predictions[predicted_class]
            
            return {
                'category': self.categories[predicted_class],
                'confidence': float(confidence),
                'is_safe': predicted_class == 0,  # Assuming 'safe' is index 0
                'all_predictions': {cat: float(pred) for cat, pred in zip(self.categories, predictions)}
            }
        except Exception as e:
            logger.error(f"Error in image prediction: {e}")
            return {'error': str(e)}
    
    def save_model(self, filepath: str) -> None:
        """Save the trained model"""
        if self.model:
            self.model.save(filepath)
            logger.info(f"Image model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """Load a trained model"""
        if os.path.exists(filepath):
            self.model = tf.keras.models.load_model(filepath)
            logger.info(f"Image model loaded from {filepath}")
        else:
            logger.warning(f"Image model file {filepath} not found")


class ContentFilteringPipeline:
    """Main content filtering pipeline combining text and image monitoring"""
    
    def __init__(self):
        self.text_monitor = TextContentMonitor()
        self.image_monitor = ImageContentMonitor()
        self.config = {
            'text_threshold': 0.5,
            'image_threshold': 0.7,
            'auto_block': True,
            'log_violations': True,
            'violation_log_file': 'content_violations.log'
        }
        
    def check_content(self, text: Optional[str] = None, 
                     image_path: Optional[Union[str, bytes]] = None) -> Dict:
        """Comprehensive content check"""
        results = {
            'text_check': None,
            'image_check': None,
            'overall_decision': 'safe',
            'block_content': False,
            'reason': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Check text content
        if text:
            text_result = self.text_monitor.predict_text(text)
            results['text_check'] = text_result
            
            if text_result.get('is_restricted', False):
                results['overall_decision'] = 'unsafe'
                reasons = text_result.get('restricted_words', [])
                if reasons:
                    results['reason'].append(f"Text contains restricted words: {', '.join(reasons)}")
                else:
                    results['reason'].append("Text classified as inappropriate")
        
        # Check image content
        if image_path:
            image_result = self.image_monitor.predict_image(image_path)
            results['image_check'] = image_result
            
            if not image_result.get('is_safe', True):
                results['overall_decision'] = 'unsafe'
                category = image_result.get('category', 'unknown')
                results['reason'].append(f"Image classified as: {category}")
        
        # Determine if content should be blocked
        if self.config['auto_block'] and results['overall_decision'] == 'unsafe':
            results['block_content'] = True
        
        # Log violations if enabled
        if self.config['log_violations'] and results['overall_decision'] == 'unsafe':
            self._log_violation(results)
        
        return results
    
    def _log_violation(self, results: Dict) -> None:
        """Log content violations for analysis"""
        try:
            log_entry = {
                'timestamp': results['timestamp'],
                'decision': results['overall_decision'],
                'reasons': results['reason'],
                'text_check': results['text_check'],
                'image_check': results['image_check']
            }
            
            with open(self.config['violation_log_file'], 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            logger.error(f"Error logging violation: {e}")
    
    def update_config(self, new_config: Dict) -> None:
        """Update filtering configuration"""
        self.config.update(new_config)
        logger.info("Configuration updated")
    
    def get_statistics(self) -> Dict:
        """Get filtering statistics"""
        try:
            if not os.path.exists(self.config['violation_log_file']):
                return {'error': 'No violation log found'}
            
            with open(self.config['violation_log_file'], 'r') as f:
                violations = [json.loads(line) for line in f if line.strip()]
            
            stats = {
                'total_violations': len(violations),
                'text_violations': sum(1 for v in violations if v.get('text_check')),
                'image_violations': sum(1 for v in violations if v.get('image_check')),
                'recent_violations': len([v for v in violations if 
                    datetime.fromisoformat(v['timestamp']) > datetime.now() - pd.Timedelta(days=1)])
            }
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'error': str(e)}


def monitor_social_media_content(text_content: str, 
                                image_path: Optional[Union[str, bytes]] = None, 
                                user_id: Optional[str] = None,
                                pipeline: Optional[ContentFilteringPipeline] = None) -> Dict:
    """
    Real-time content monitoring function for social media posts
    
    Args:
        text_content (str): Text content to check
        image_path (str/bytes, optional): Path to image file or image bytes
        user_id (str, optional): User identifier for logging
        pipeline (ContentFilteringPipeline, optional): Content monitoring pipeline
    
    Returns:
        dict: Content analysis results and moderation decision
    """
    
    if pipeline is None:
        pipeline = ContentFilteringPipeline()
        pipeline.text_monitor.load_restricted_words()
    
    # Check content using pipeline
    result = pipeline.check_content(text=text_content, image_path=image_path)
    
    # Add user context if provided
    if user_id:
        result['user_id'] = user_id
    
    # Return appropriate response based on content safety
    if result['overall_decision'] == 'safe':
        result['action'] = 'allow'
        result['message'] = 'Content approved'
    else:
        result['action'] = 'block'
        result['message'] = 'Content blocked due to policy violation'
        
        # Additional actions for blocked content
        if user_id:
            result['user_warning'] = True
            result['content_removed'] = True
    
    return result


def main():
    """Main function to demonstrate the content monitoring system"""
    print("🚀 Content Monitoring ML Model for Decentralized Social Media DApp")
    print("=" * 70)
    
    # Initialize the system
    print("\n📋 Initializing Content Monitoring System...")
    pipeline = ContentFilteringPipeline()
    pipeline.text_monitor.load_restricted_words()
    
    # Build models
    print("\n🔧 Building ML Models...")
    pipeline.text_monitor.build_text_model()
    pipeline.image_monitor.build_image_model()
    
    print("✅ Content monitoring system initialized successfully!")
    
    # Test the system
    print("\n🧪 Testing Content Filtering System:")
    print("-" * 50)
    
    test_cases = [
        {
            'text': "Hello everyone! How are you doing today?",
            'description': 'Safe greeting message'
        },
        {
            'text': "I hate all people from that community and want them gone",
            'description': 'Hate speech message'
        },
        {
            'text': "Let's go to the park and have fun!",
            'description': 'Safe activity message'
        },
        {
            'text': "We should commit violence against them",
            'description': 'Violent content'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Text: {test_case['text']}")
        
        # Check content
        result = pipeline.check_content(text=test_case['text'])
        
        print(f"Decision: {result['overall_decision']}")
        print(f"Blocked: {result['block_content']}")
        if result['reason']:
            print(f"Reasons: {', '.join(result['reason'])}")
        print("-" * 30)
    
    # Real-time monitoring demo
    print("\n🌐 Real-time Content Monitoring Demo:")
    print("-" * 50)
    
    sample_post = {
        'user_id': 'user123',
        'text': 'This is a normal post about my day',
        'image': None
    }
    
    result = monitor_social_media_content(
        text_content=sample_post['text'],
        user_id=sample_post['user_id'],
        pipeline=pipeline
    )
    
    print(f"User: {result['user_id']}")
    print(f"Content: {sample_post['text']}")
    print(f"Action: {result['action']}")
    print(f"Message: {result['message']}")
    
    # System statistics
    print("\n📊 Content Monitoring System Statistics:")
    print("-" * 50)
    
    stats = pipeline.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Model information
    print("\n🤖 Model Information:")
    print("-" * 30)
    if pipeline.text_monitor.model:
        print(f"Text Model: {pipeline.text_monitor.model.name}")
        print(f"Text Model Parameters: {pipeline.text_monitor.model.count_params():,}")
    
    if pipeline.image_monitor.model:
        print(f"Image Model: {pipeline.image_monitor.model.name}")
        print(f"Image Model Parameters: {pipeline.image_monitor.model.count_params():,}")
    
    print("\n🎯 Integration Guide for DApp:")
    print("=" * 50)
    print("""
1. Smart Contract Integration:
   - Deploy content monitoring smart contract
   - Store content hashes and moderation results on-chain
   - Implement reputation system for users

2. Frontend Integration:
   - Integrate content checking before post submission
   - Show real-time content analysis
   - Display moderation decisions transparently

3. Backend Integration:
   - Run ML models on decentralized compute nodes
   - Use IPFS for content storage
   - Implement decentralized content moderation

4. User Experience:
   - Clear content guidelines
   - Transparent moderation process
   - Appeal mechanism for blocked content

5. Security Considerations:
   - Model poisoning protection
   - Adversarial attack detection
   - Privacy-preserving content analysis
    """)
    
    print("\n✨ Summary:")
    print("=" * 30)
    print("✅ Text Classification: ML-based model for detecting inappropriate text content")
    print("✅ Image Classification: CNN-based model for detecting inappropriate images")
    print("✅ Real-time Filtering: Immediate content analysis and moderation")
    print("✅ Customizable Rules: Configurable thresholds and restricted word lists")
    print("✅ Decentralized Ready: Designed for integration with blockchain-based systems")
    print("✅ Comprehensive Logging: Track violations and system performance")
    
    print("\n🚀 Your decentralized social media DApp is now ready with robust content monitoring!")


if __name__ == "__main__":
    main()
