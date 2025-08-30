# Content Monitoring ML Model for Decentralized Social Media DApp

A comprehensive content monitoring system using TensorFlow to ensure content safety without centralized moderation. This system is designed specifically for decentralized social media applications where traditional account banning isn't possible.

## 🚀 Features

- **Text Classification**: ML-based model for detecting inappropriate text content, hate speech, and restricted words
- **Image Classification**: CNN-based model for detecting inappropriate images, violence, nudity, and hate symbols
- **Real-time Filtering**: Immediate content analysis and moderation decisions
- **Customizable Rules**: Configurable thresholds and restricted word lists
- **Decentralized Ready**: Designed for integration with blockchain-based systems
- **Comprehensive Logging**: Track violations and system performance for transparency

## 🏗️ Architecture

The system consists of three main components:

1. **TextContentMonitor**: Handles text content analysis using BERT-based models
2. **ImageContentMonitor**: Manages image content analysis using CNN models
3. **ContentFilteringPipeline**: Orchestrates both monitors and provides unified API

## 📦 Installation

1. **Clone or download the files**:
   ```bash
   # Make sure you have the following files:
   # - content_monitoring_system.py
   # - requirements.txt
   # - README.md
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python content_monitoring_system.py
   ```

## 🎯 Quick Start

### Basic Usage

```python
from content_monitoring_system import ContentFilteringPipeline, monitor_social_media_content

# Initialize the system
pipeline = ContentFilteringPipeline()
pipeline.text_monitor.load_restricted_words()

# Check text content
result = pipeline.check_content(text="Hello, how are you?")
print(f"Content safe: {result['overall_decision'] == 'safe'}")

# Check image content
result = pipeline.check_content(image_path="path/to/image.jpg")
print(f"Image safe: {result['overall_decision'] == 'safe'}")

# Real-time monitoring for social media posts
result = monitor_social_media_content(
    text_content="Your post content here",
    user_id="user123"
)
print(f"Action: {result['action']}")
```

### Customizing Restricted Words

```python
# Load custom restricted words from file
pipeline.text_monitor.load_restricted_words("custom_restricted_words.txt")

# Or add words programmatically
pipeline.text_monitor.restricted_words.update(['spam', 'scam', 'fake_news'])
```

### Configuration

```python
# Update filtering configuration
pipeline.update_config({
    'text_threshold': 0.3,      # Stricter text filtering
    'image_threshold': 0.5,     # Stricter image filtering
    'auto_block': True,         # Automatically block unsafe content
    'log_violations': True      # Log all violations
})
```

## 🔧 Model Training

### Text Model Training

```python
# Prepare training data
texts = ["safe text 1", "safe text 2", "inappropriate text 1"]
labels = [0, 0, 1]  # 0 = safe, 1 = inappropriate

# Train the model
pipeline.text_monitor.build_text_model()
history = pipeline.text_monitor.train_text_model(texts, labels, epochs=5)

# Save the trained model
pipeline.text_monitor.save_model("text_model.h5")
```

### Image Model Training

```python
# Build image model
pipeline.image_monitor.build_image_model()

# For production, use real training data
# history = pipeline.image_monitor.train_image_model(image_paths, labels, epochs=10)

# Save the trained model
pipeline.image_monitor.save_model("image_model.h5")
```

## 🌐 DApp Integration

### Smart Contract Integration

```solidity
// Example Solidity contract for content monitoring
contract ContentMonitor {
    mapping(bytes32 => bool) public contentApproved;
    mapping(bytes32 => string) public contentHash;
    
    function submitContent(string memory content, bytes32 hash) public {
        // Submit content for monitoring
        contentHash[hash] = content;
        // Trigger ML model analysis
    }
    
    function approveContent(bytes32 hash) public {
        contentApproved[hash] = true;
    }
}
```

### Frontend Integration

```javascript
// Example React component for content submission
import { monitorContent } from './contentMonitoring';

const PostForm = () => {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    // Check content before posting
    const result = await monitorContent(content);
    
    if (result.action === 'allow') {
      // Post content to blockchain
      await postToBlockchain(content);
    } else {
      // Show moderation message
      alert('Content blocked: ' + result.message);
    }
    
    setIsSubmitting(false);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <textarea 
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What's on your mind?"
      />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Checking...' : 'Post'}
      </button>
    </form>
  );
};
```

### Backend Integration

```python
# Example Flask API for content monitoring
from flask import Flask, request, jsonify
from content_monitoring_system import monitor_social_media_content

app = Flask(__name__)

@app.route('/api/check-content', methods=['POST'])
def check_content():
    data = request.json
    text_content = data.get('text', '')
    image_data = data.get('image', None)
    user_id = data.get('user_id', None)
    
    # Monitor content
    result = monitor_social_media_content(
        text_content=text_content,
        image_path=image_data,
        user_id=user_id
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

## 📊 Monitoring and Analytics

### View System Statistics

```python
# Get filtering statistics
stats = pipeline.get_statistics()
print(f"Total violations: {stats['total_violations']}")
print(f"Text violations: {stats['text_violations']}")
print(f"Image violations: {stats['image_violations']}")
print(f"Recent violations (24h): {stats['recent_violations']}")
```

### Violation Logs

The system automatically logs all content violations to `content_violations.log`:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "decision": "unsafe",
  "reasons": ["Text contains restricted words: hate, violence"],
  "text_check": {
    "is_restricted": true,
    "restricted_words": ["hate", "violence"],
    "severity": 0.2
  },
  "image_check": null
}
```

## ⚙️ Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `text_threshold` | 0.5 | Confidence threshold for text content blocking |
| `image_threshold` | 0.7 | Confidence threshold for image content blocking |
| `auto_block` | true | Automatically block unsafe content |
| `log_violations` | true | Log all content violations |
| `violation_log_file` | 'content_violations.log' | File path for violation logs |

## 🛡️ Security Considerations

### Model Protection
- Implement model versioning and A/B testing
- Add adversarial training for robustness
- Use federated learning for privacy protection

### Privacy Protection
- Encrypt content during analysis
- Implement differential privacy
- Use secure multi-party computation

### Attack Prevention
- Detect model poisoning attempts
- Monitor for adversarial inputs
- Implement rate limiting for API calls

## 🚀 Production Deployment

### Model Optimization
```python
# Convert to TensorFlow Lite for mobile deployment
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save optimized model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

### Scalability
- Use model serving frameworks (TensorFlow Serving)
- Implement caching for repeated content
- Use distributed computing for high throughput

### Monitoring
- Track model performance metrics
- Monitor false positive/negative rates
- Implement alerting for system issues

## 📝 Customization

### Adding New Content Types
```python
class VideoContentMonitor:
    """Monitor video content for inappropriate material"""
    
    def __init__(self):
        self.model = None
        self.frame_rate = 1  # Check 1 frame per second
    
    def check_video(self, video_path):
        # Extract frames and analyze
        # Return safety assessment
        pass
```

### Custom Categories
```python
# Define custom content categories
pipeline.text_monitor.categories = [
    'safe', 'hate_speech', 'violence', 'spam', 
    'fake_news', 'harassment', 'discrimination'
]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the example code

## 🔮 Future Enhancements

- **Multi-language Support**: Detect inappropriate content in multiple languages
- **Context Awareness**: Better understanding of context and sarcasm
- **Real-time Learning**: Continuous model improvement from user feedback
- **Blockchain Integration**: Store moderation results on-chain for transparency
- **Decentralized Training**: Collaborative model training across nodes

---

**Built with ❤️ for the decentralized web**

Your decentralized social media DApp is now equipped with enterprise-grade content monitoring that respects user privacy and decentralization principles!
