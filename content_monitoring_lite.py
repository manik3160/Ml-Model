#!/usr/bin/env python3
"""
Content Monitoring Lite - Core functionality without heavy ML dependencies

This version provides the essential content monitoring features without requiring
TensorFlow, making it suitable for environments with dependency constraints.
"""

import json
import os
import logging
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextContentMonitorLite:
    """Lightweight text content monitoring using word-based detection"""
    
    def __init__(self, max_length: int = 512):
        self.restricted_words = set()
        self.max_length = max_length
        self.categories = ['safe', 'inappropriate', 'hate_speech', 'violence', 'spam']
        self.bad_words_api_key = "kADcC1YMTjR636KcjnMVtdQ2l4yewM2J"
        self.bad_words_api_url = "https://api.api-ninjas.com/v1/profanityfilter"
        
    def load_restricted_words(self, file_path: Optional[str] = None) -> None:
        """Load restricted words from file or use default set"""
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.restricted_words = set(line.strip().lower() for line in f)
            logger.info(f"Loaded {len(self.restricted_words)} restricted words from file")
        else:
            # Use comprehensive default restricted words
            self.restricted_words = {
                'hate', 'violence', 'abuse', 'harassment', 'discrimination',
                'racism', 'sexism', 'homophobia', 'bullying', 'threats',
                'illegal', 'drugs', 'weapons', 'terrorism', 'extremism',
                'spam', 'scam', 'fake_news', 'misinformation', 'knife',
                'murder', 'kill', 'suicide', 'death', 'ass', 'asshole',
                'bastard', 'bitch', 'bloody', 'cock', 'crap', 'cunt',
                'damn', 'dick', 'fuck', 'fucker', 'fucking', 'hell',
                'motherfucker', 'nigga', 'nigger', 'piss', 'pussy',
                'shit', 'slut', 'whore', 'bollocks', 'bugger'
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
        
        severity_score = len(found_restricted) / len(words) if words else 0
        
        return {
            'is_restricted': len(found_restricted) > 0,
            'restricted_words': found_restricted,
            'severity': severity_score,
            'method': 'word_check',
            'confidence': 'high' if severity_score > 0.1 else 'medium' if severity_score > 0.05 else 'low'
        }
    
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
    
    def analyze_text_content(self, text: str) -> Dict:
        """Comprehensive text content analysis"""
        if len(text) > self.max_length:
            text = text[:self.max_length]
            logger.warning(f"Text truncated to {self.max_length} characters")
        
        # Perform multiple checks
        word_check = self.simple_word_check(text)
        api_check = self.check_text_with_api(text)
        
        # Calculate overall risk score
        risk_score = 0.0
        if word_check['is_restricted']:
            risk_score += 0.6
        if api_check.get('api_result', {}).get('has_profanity', False):
            risk_score += 0.4
        
        # Determine category
        if risk_score >= 0.8:
            category = 'hate_speech'
        elif risk_score >= 0.6:
            category = 'violence'
        elif risk_score >= 0.4:
            category = 'inappropriate'
        elif risk_score >= 0.2:
            category = 'spam'
        else:
            category = 'safe'
        
        return {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'category': category,
            'risk_score': min(risk_score, 1.0),
            'is_restricted': risk_score >= 0.4,
            'word_check': word_check,
            'api_check': api_check,
            'timestamp': datetime.now().isoformat(),
            'method': 'lite_analysis'
        }

class ContentMonitoringPipelineLite:
    """Lightweight content monitoring pipeline"""
    
    def __init__(self):
        self.text_monitor = TextContentMonitorLite()
        self.log_file = "content_violations_lite.log"
        
    def initialize(self):
        """Initialize the monitoring pipeline"""
        logger.info("🚀 Initializing Content Monitoring Pipeline (Lite)...")
        
        # Load restricted words
        self.text_monitor.load_restricted_words()
        
        # Set up logging
        self._setup_logging()
        
        logger.info("✅ Content Monitoring Pipeline (Lite) initialized successfully")
    
    def _setup_logging(self):
        """Set up logging for content violations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
    
    def monitor_text(self, text: str, user_id: str = "unknown") -> Dict:
        """Monitor text content for violations"""
        try:
            # Analyze text content
            analysis = self.text_monitor.analyze_text_content(text)
            
            # Log violations
            if analysis['is_restricted']:
                self._log_violation(user_id, text, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error monitoring text: {e}")
            return {
                'error': str(e),
                'is_restricted': False,
                'method': 'error_fallback'
            }
    
    def _log_violation(self, user_id: str, text: str, analysis: Dict):
        """Log content violations"""
        violation_log = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'text_preview': text[:100] + '...' if len(text) > 100 else text,
            'category': analysis['category'],
            'risk_score': analysis['risk_score'],
            'restricted_words': analysis['word_check'].get('restricted_words', [])
        }
        
        logger.warning(f"Content violation detected: {violation_log}")
        
        # Save to log file
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(violation_log) + '\n')
        except Exception as e:
            logger.error(f"Error writing to log file: {e}")
    
    def get_statistics(self) -> Dict:
        """Get monitoring statistics"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                
                violations = len(lines)
                return {
                    'total_violations': violations,
                    'log_file': self.log_file,
                    'status': 'active'
                }
            else:
                return {
                    'total_violations': 0,
                    'log_file': self.log_file,
                    'status': 'no_violations_yet'
                }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'error': str(e)}

def main():
    """Main function to demonstrate the lite system"""
    print("🚀 Content Monitoring System (Lite) - No ML Dependencies")
    print("=" * 60)
    
    try:
        # Initialize pipeline
        pipeline = ContentMonitoringPipelineLite()
        pipeline.initialize()
        
        # Test with sample content
        test_cases = [
            "This is a completely safe message",
            "I hate this content and want to kill someone",
            "This is spam content with fake news",
            "Hello, how are you today?"
        ]
        
        print("\n🧪 Testing content monitoring...")
        for i, text in enumerate(test_cases, 1):
            print(f"\nTest {i}: {text[:50]}...")
            result = pipeline.monitor_text(text, f"user_{i}")
            print(f"Result: {result['category']} (Risk: {result['risk_score']:.2f})")
        
        # Show statistics
        stats = pipeline.get_statistics()
        print(f"\n📊 Statistics: {stats}")
        
        print("\n🎉 Lite system test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
