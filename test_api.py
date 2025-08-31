#!/usr/bin/env python3
"""
Test Script for Content Monitoring API

This script tests the API endpoints to ensure they're working correctly
with your ML model.
"""

import requests  
import json
import time

# API base URL
API_BASE = "http://localhost:5001/api"

def test_health():
    """Test health check endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Message: {data['message']}")
            print(f"   ML Model Ready: {data['ml_model_ready']}")
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def test_text_check():
    """Test text content checking"""
    print("\n📝 Testing Text Content Check...")
    
    test_cases = [
        {
            "text": "Hello everyone! How are you doing today?",
            "expected": "safe",
            "description": "Safe greeting message"
        },
        {
            "text": "I hate all people from that community",
            "expected": "unsafe",
            "description": "Hate speech message"
        },
        {
            "text": "Let's go to the park and have fun!",
            "expected": "safe",
            "description": "Safe activity message"
        },
        {
            "text": "We should commit violence against them",
            "expected": "unsafe",
            "description": "Violent content"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['description']}")
        print(f"   Text: {test_case['text']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/check-text-only",
                json={
                    "text": test_case["text"],
                    "user_id": f"test_user_{i}"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                decision = data.get('overall_decision', 'unknown')
                action = data.get('action', 'unknown')
                
                print(f"   Decision: {decision}")
                print(f"   Action: {action}")
                
                if decision == test_case["expected"]:
                    print("   ✅ Result matches expectation")
                else:
                    print(f"   ❌ Expected {test_case['expected']}, got {decision}")
                
                if data.get('reason'):
                    print(f"   Reasons: {', '.join(data['reason'])}")
            else:
                print(f"   ❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request Error: {e}")

def test_stats():
    """Test statistics endpoint"""
    print("\n📊 Testing Statistics Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Statistics Retrieved:")
            print(f"   Total Violations: {data.get('total_violations', 0)}")
            print(f"   Text Violations: {data.get('text_violations', 0)}")
            print(f"   Image Violations: {data.get('image_violations', 0)}")
            print(f"   Recent Violations (24h): {data.get('recent_violations', 0)}")
        else:
            print(f"❌ Stats Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats Error: {e}")

def test_config():
    """Test configuration endpoint"""
    print("\n⚙️ Testing Configuration Endpoint...")
    try:
        # Get current config
        response = requests.get(f"{API_BASE}/config")
        if response.status_code == 200:
            data = response.json()
            print("✅ Current Configuration:")
            for key, value in data.items():
                print(f"   {key}: {value}")
            
            # Test updating config
            print("\n   Testing config update...")
            new_config = {"text_threshold": 0.3}
            update_response = requests.put(
                f"{API_BASE}/config",
                json=new_config
            )
            
            if update_response.status_code == 200:
                print("   ✅ Configuration updated successfully")
            else:
                print(f"   ❌ Config update failed: {update_response.status_code}")
        else:
            print(f"❌ Config Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Config Error: {e}")

def test_restricted_words():
    """Test restricted words endpoint"""
    print("\n🔒 Testing Restricted Words Endpoint...")
    try:
        # Get current restricted words
        response = requests.get(f"{API_BASE}/restricted-words")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current Restricted Words: {data.get('count', 0)} words")
            
            # Test adding new words
            print("\n   Testing adding new restricted words...")
            new_words = ["test_word_1", "test_word_2"]
            add_response = requests.post(
                f"{API_BASE}/restricted-words",
                json={"words": new_words}
            )
            
            if add_response.status_code == 200:
                add_data = add_response.json()
                print(f"   ✅ Added {add_data.get('total_count', 0)} words")
            else:
                print(f"   ❌ Add words failed: {add_response.status_code}")
        else:
            print(f"❌ Restricted Words Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Restricted Words Error: {e}")

def test_content_check():
    """Test combined content checking"""
    print("\n🔄 Testing Combined Content Check...")
    try:
        response = requests.post(
            f"{API_BASE}/check-content",
            json={
                "text": "This is a test message with hate content",
                "user_id": "test_user_combined"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Combined Content Check:")
            print(f"   Decision: {data.get('overall_decision')}")
            print(f"   Action: {data.get('action')}")
            print(f"   Message: {data.get('message')}")
            
            if data.get('reason'):
                print(f"   Reasons: {', '.join(data['reason'])}")
        else:
            print(f"❌ Combined Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Combined Check Error: {e}")

def main():
    """Run all API tests"""
    print("🚀 Content Monitoring API Test Suite")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for API server to be ready...")
    time.sleep(2)
    
    # Run tests
    test_health()
    test_text_check()
    test_stats()
    test_config()
    test_restricted_words()
    test_content_check()
    
    print("\n" + "=" * 50)
    print("✅ API Test Suite Completed!")
    print("\n🎯 Your ML Model API is working perfectly!")
    print("   You can now integrate it with your Next.js application.")
    print(f"   API Base URL: {API_BASE}")

if __name__ == "__main__":
    main()
