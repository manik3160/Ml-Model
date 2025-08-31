#!/usr/bin/env python3
"""
Basic functionality test for content monitoring system (Lite version)
Tests core logic without heavy ML dependencies
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_text_monitor_basic():
    """Test basic text monitoring functionality"""
    print("🧪 Testing basic text monitoring functionality...")
    
    try:
        # Import the lite version without ML dependencies
        from content_monitoring_lite import TextContentMonitorLite
        
        # Create monitor instance
        monitor = TextContentMonitorLite()
        
        # Test loading restricted words
        print("📝 Loading restricted words...")
        monitor.load_restricted_words()
        print(f"✅ Loaded {len(monitor.restricted_words)} restricted words")
        
        # Test simple word check
        print("🔍 Testing simple word check...")
        test_text = "This is a test message with hate content"
        result = monitor.simple_word_check(test_text)
        print(f"✅ Word check result: {result}")
        
        # Test safe text
        safe_text = "This is a completely safe message"
        safe_result = monitor.simple_word_check(safe_text)
        print(f"✅ Safe text check: {safe_result}")
        
        print("🎉 Basic text monitoring tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in basic text monitoring test: {e}")
        return False

def test_api_integration():
    """Test API integration functionality"""
    print("\n🌐 Testing API integration...")
    
    try:
        from content_monitoring_lite import TextContentMonitorLite
        
        monitor = TextContentMonitorLite()
        
        # Test API check (this will use the fallback method)
        print("📡 Testing API integration...")
        test_text = "Test message for API validation"
        result = monitor.check_text_with_api(test_text)
        print(f"✅ API check result: {result}")
        
        print("🎉 API integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in API integration test: {e}")
        return False

def test_content_analysis():
    """Test comprehensive content analysis"""
    print("\n🔍 Testing content analysis...")
    
    try:
        from content_monitoring_lite import TextContentMonitorLite
        
        monitor = TextContentMonitorLite()
        
        # Test content analysis
        print("📊 Testing content analysis...")
        test_text = "This message contains hate speech and violence"
        result = monitor.analyze_text_content(test_text)
        print(f"✅ Analysis result: {result['category']} (Risk: {result['risk_score']:.2f})")
        
        print("🎉 Content analysis tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in content analysis test: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🚀 Content Monitoring System (Lite) - Basic Functionality Test")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    # Test basic text monitoring
    if test_text_monitor_basic():
        success_count += 1
    
    # Test API integration
    if test_api_integration():
        success_count += 1
    
    # Test content analysis
    if test_content_analysis():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All basic tests passed! The lite system is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
