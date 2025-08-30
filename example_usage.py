#!/usr/bin/env python3
"""
Example Usage of Content Monitoring System

This script demonstrates how to use the content monitoring system
for your decentralized social media DApp.
"""

from content_monitoring_system import (
    ContentFilteringPipeline, 
    monitor_social_media_content,
    TextContentMonitor,
    ImageContentMonitor
)

def basic_content_checking():
    """Demonstrate basic content checking functionality"""
    print("🔍 Basic Content Checking Demo")
    print("=" * 40)
    
    # Initialize the pipeline
    pipeline = ContentFilteringPipeline()
    pipeline.text_monitor.load_restricted_words()
    
    # Test various content types
    test_content = [
        "Hello everyone! How are you doing today?",
        "I hate all people from that community",
        "Let's go to the park and have fun!",
        "We should commit violence against them",
        "This is spam content with fake news",
        "Happy birthday! Hope you have a wonderful day."
    ]
    
    for content in test_content:
        result = pipeline.check_content(text=content)
        status = "✅ SAFE" if result['overall_decision'] == 'safe' else "❌ BLOCKED"
        print(f"{status} | {content[:50]}...")
        
        if result['reason']:
            print(f"   Reason: {', '.join(result['reason'])}")
        print()

def social_media_simulation():
    """Simulate real social media posts"""
    print("📱 Social Media Post Simulation")
    print("=" * 40)
    
    # Simulate user posts
    posts = [
        {
            'user_id': 'alice123',
            'text': 'Just had the best coffee ever! ☕',
            'type': 'safe_post'
        },
        {
            'user_id': 'bob456',
            'text': 'I hate everyone from that group, they should be eliminated',
            'type': 'hate_speech'
        },
        {
            'user_id': 'charlie789',
            'text': 'Beautiful sunset today! 🌅',
            'type': 'safe_post'
        },
        {
            'user_id': 'dave101',
            'text': 'Let\'s spread fake news and misinformation',
            'type': 'misinformation'
        }
    ]
    
    for post in posts:
        print(f"👤 User: {post['user_id']}")
        print(f"📝 Post: {post['text']}")
        
        # Monitor content
        result = monitor_social_media_content(
            text_content=post['text'],
            user_id=post['user_id']
        )
        
        print(f"🎯 Action: {result['action']}")
        print(f"💬 Message: {result['message']}")
        
        if result.get('user_warning'):
            print("⚠️  User warned and content removed")
        
        print("-" * 40)

def custom_restricted_words():
    """Demonstrate customizing restricted words"""
    print("🔧 Custom Restricted Words Demo")
    print("=" * 40)
    
    # Create a custom text monitor
    custom_monitor = TextContentMonitor()
    
    # Add custom restricted words
    custom_words = [
        'spam', 'scam', 'fake_news', 'clickbait',
        'phishing', 'malware', 'virus', 'hack'
    ]
    custom_monitor.restricted_words.update(custom_words)
    
    print(f"Added {len(custom_words)} custom restricted words")
    print(f"Total restricted words: {len(custom_monitor.restricted_words)}")
    
    # Test with custom words
    test_text = "This is a spam message with fake news and clickbait"
    result = custom_monitor.simple_word_check(test_text)
    
    print(f"\nTest text: {test_text}")
    print(f"Contains restricted words: {result['is_restricted']}")
    print(f"Found words: {result['restricted_words']}")
    print(f"Severity: {result['severity']:.2f}")

def configuration_demo():
    """Demonstrate configuration options"""
    print("⚙️ Configuration Options Demo")
    print("=" * 40)
    
    pipeline = ContentFilteringPipeline()
    
    # Show default configuration
    print("Default configuration:")
    for key, value in pipeline.config.items():
        print(f"  {key}: {value}")
    
    # Update configuration for stricter filtering
    print("\nUpdating configuration for stricter filtering...")
    pipeline.update_config({
        'text_threshold': 0.3,      # Lower threshold = stricter
        'image_threshold': 0.5,     # Lower threshold = stricter
        'auto_block': True,         # Automatically block unsafe content
        'log_violations': True      # Log all violations
    })
    
    print("\nUpdated configuration:")
    for key, value in pipeline.config.items():
        print(f"  {key}: {value}")

def statistics_demo():
    """Demonstrate statistics and monitoring"""
    print("📊 Statistics and Monitoring Demo")
    print("=" * 40)
    
    pipeline = ContentFilteringPipeline()
    
    # Generate some test violations
    test_violations = [
        "I hate everyone",
        "Let's commit violence",
        "This is racist content",
        "Spread fake news"
    ]
    
    print("Generating test violations...")
    for violation in test_violations:
        pipeline.check_content(text=violation)
    
    # Get statistics
    stats = pipeline.get_statistics()
    
    print("\nContent Monitoring Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

def integration_example():
    """Show how to integrate with your DApp"""
    print("🌐 DApp Integration Example")
    print("=" * 40)
    
    print("""
To integrate with your decentralized social media DApp:

1. **Smart Contract Integration**:
   - Deploy content monitoring smart contract
   - Store content hashes and moderation results on-chain
   - Implement reputation system for users

2. **Frontend Integration**:
   - Check content before post submission
   - Show real-time content analysis
   - Display moderation decisions transparently

3. **Backend Integration**:
   - Run ML models on decentralized compute nodes
   - Use IPFS for content storage
   - Implement decentralized content moderation

4. **User Experience**:
   - Clear content guidelines
   - Transparent moderation process
   - Appeal mechanism for blocked content
    """)

def main():
    """Run all demos"""
    print("🚀 Content Monitoring System - Example Usage")
    print("=" * 60)
    print()
    
    try:
        # Run all demonstrations
        basic_content_checking()
        print()
        
        social_media_simulation()
        print()
        
        custom_restricted_words()
        print()
        
        configuration_demo()
        print()
        
        statistics_demo()
        print()
        
        integration_example()
        
        print("\n✅ All demonstrations completed successfully!")
        print("\n🎯 Next steps:")
        print("1. Customize the restricted word lists for your use case")
        print("2. Train the models with your specific data")
        print("3. Integrate with your blockchain infrastructure")
        print("4. Deploy to production with proper monitoring")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Make sure you have installed all dependencies:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
