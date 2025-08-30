#!/usr/bin/env python3
"""
Test script for Bad Words API integration

This script demonstrates how to use the new Bad Words API integration
in the content monitoring system.
"""

import requests
import json
import time

# API configuration
API_BASE = "http://localhost:5001/api"
BAD_WORDS_API_KEY = "kADcC1YMTjR636KcjnMVtdQ2l4yewM2J"

def test_api_health():
    """Test if the API server is running"""
    print("🏥 Testing API Health...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        return False

def test_restricted_words_update():
    """Test updating restricted words from Bad Words API"""
    print("\n🔄 Testing Restricted Words Update from Bad Words API...")
    try:
        response = requests.post(
            f"{API_BASE}/restricted-words/update-from-api",
            json={"words_to_test": [
                "test", "hello", "fuck", "shit", "damn", "kill", "hate",
                "violence", "abuse", "racism", "sexism", "spam", "scam"
            ]}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully updated restricted words from API")
            print(f"   API confirmed words: {len(data.get('api_confirmed_words', []))}")
            print(f"   Total restricted words: {data.get('total_count', 0)}")
            print(f"   Method: {data.get('method', 'unknown')}")
            
            if data.get('api_confirmed_words'):
                print(f"   Confirmed words: {', '.join(data['api_confirmed_words'][:5])}...")
        else:
            print(f"❌ Failed to update restricted words: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error updating restricted words: {e}")

def test_enhanced_text_check():
    """Test the enhanced text checking with Bad Words API"""
    print("\n🔍 Testing Enhanced Text Check with Bad Words API...")
    
    test_texts = [
        "Hello everyone! How are you doing today?",
        "This is a test message with some inappropriate content like fuck and shit",
        "Let's go to the park and have fun!",
        "I hate all people from that community and want them gone",
        "This is spam content with fake news and clickbait"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n   Test {i}: {text[:50]}...")
        
        try:
            response = requests.post(
                f"{API_BASE}/check-text-with-api",
                json={"text": text, "user_id": f"test_user_{i}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'unknown')
                decision = data.get('overall_decision', 'unknown')
                method = data.get('method', 'unknown')
                
                print(f"      Action: {action}")
                print(f"      Decision: {decision}")
                print(f"      Method: {method}")
                
                if data.get('api_result'):
                    api_result = data['api_result']
                    print(f"      API Result: {api_result}")
                
                if data.get('restricted_words'):
                    print(f"      Restricted words: {', '.join(data['restricted_words'])}")
                    
            else:
                print(f"      ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting

def test_current_restricted_words():
    """Test getting current restricted words"""
    print("\n📋 Testing Current Restricted Words...")
    try:
        response = requests.get(f"{API_BASE}/restricted-words")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current restricted words: {data.get('count', 0)}")
            
            # Show first few words
            words = data.get('restricted_words', [])
            if words:
                print(f"   Sample words: {', '.join(words[:10])}")
                if len(words) > 10:
                    print(f"   ... and {len(words) - 10} more")
        else:
            print(f"❌ Failed to get restricted words: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting restricted words: {e}")

def test_bad_words_api_direct():
    """Test the Bad Words API directly"""
    print("\n🌐 Testing Bad Words API Directly...")
    
    test_words = ["hello", "fuck", "shit", "damn", "kill", "hate"]
    
    for word in test_words:
        try:
            headers = {
                'X-Api-Key': BAD_WORDS_API_KEY
            }
            
            params = {
                'text': word
            }
            
            response = requests.get(
                "https://api.api-ninjas.com/v1/profanityfilter",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_profanity = data.get('has_profanity', False)
                print(f"   '{word}': {'❌ Profanity' if has_profanity else '✅ Safe'}")
            else:
                print(f"   '{word}': ❌ API Error {response.status_code}")
                
        except Exception as e:
            print(f"   '{word}': ❌ Error {e}")
        
        time.sleep(0.5)  # Rate limiting

def main():
    """Main test function"""
    print("🚀 Bad Words API Integration Test")
    print("=" * 50)
    
    # Check API health first
    if not test_api_health():
        print("\n❌ API server is not running. Please start it first:")
        print("   python api_server.py")
        return
    
    # Test the integration
    test_restricted_words_update()
    test_enhanced_text_check()
    test_current_restricted_words()
    test_bad_words_api_direct()
    
    print("\n✨ Bad Words API Integration Test Complete!")
    print("\n📚 What was tested:")
    print("   ✅ Updating restricted words from Bad Words API")
    print("   ✅ Enhanced text checking with API integration")
    print("   ✅ Current restricted words retrieval")
    print("   ✅ Direct Bad Words API testing")
    
    print("\n🔧 Next steps:")
    print("   1. The system now uses your Bad Words API key")
    print("   2. Restricted words are dynamically updated from the API")
    print("   3. Text checking is enhanced with real-time API validation")
    print("   4. You can customize the word list by modifying the test words")

if __name__ == "__main__":
    main()
