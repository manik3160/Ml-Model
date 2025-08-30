# Bad Words API Integration Guide

This guide explains how to use the new Bad Words API integration in your Content Monitoring ML Model for Decentralized Social Media DApp.

## 🚀 Overview

The system now integrates with the **API-Ninjas Bad Words API** using your API key `kADcC1YMTjR636KcjnMVtdQ2l4yewM2J` to provide enhanced content filtering capabilities.

## 🔑 API Configuration

Your API key is configured in the `TextContentMonitor` class:

```python
self.bad_words_api_key = "kADcC1YMTjR636KcjnMVtdQ2l4yewM2J"
self.bad_words_api_url = "https://api.api-ninjas.com/v1/profanityfilter"
```

## 🆕 New Features

### 1. Dynamic Restricted Words Loading
- Automatically fetches and updates restricted words from the Bad Words API
- Falls back to a comprehensive local list if API is unavailable
- Combines API results with local word checking for better accuracy

### 2. Enhanced Text Checking
- Real-time validation using the Bad Words API
- Combines API results with local ML model predictions
- Provides confidence levels and detailed analysis

### 3. New API Endpoints
- `/api/restricted-words/update-from-api` - Update words from Bad Words API
- `/api/check-text-with-api` - Enhanced text checking with API integration

## 📋 API Endpoints

### Update Restricted Words from API
```bash
POST /api/restricted-words/update-from-api
```

**Request Body:**
```json
{
  "words_to_test": [
    "test", "hello", "fuck", "shit", "damn", "kill", "hate",
    "violence", "abuse", "racism", "sexism", "spam", "scam"
  ]
}
```

**Response:**
```json
{
  "message": "Restricted words updated from Bad Words API",
  "api_confirmed_words": ["fuck", "shit", "damn", "kill", "hate"],
  "total_count": 45,
  "method": "api_enhanced"
}
```

### Enhanced Text Check with API
```bash
POST /api/check-text-with-api
```

**Request Body:**
```json
{
  "text": "This is a test message with inappropriate content",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "api_result": {
    "has_profanity": true,
    "api_confidence": "high"
  },
  "local_check": {
    "is_restricted": true,
    "restricted_words": ["inappropriate"],
    "severity": 0.2,
    "method": "word_check"
  },
  "combined_decision": true,
  "method": "api_enhanced",
  "user_id": "user123",
  "action": "block",
  "message": "Content blocked due to policy violation",
  "overall_decision": "unsafe"
}
```

## 🧪 Testing the Integration

### 1. Start the API Server
```bash
python api_server.py
```

### 2. Run the Test Script
```bash
python test_bad_words_api.py
```

This will test:
- ✅ API server connectivity
- ✅ Restricted words update from Bad Words API
- ✅ Enhanced text checking
- ✅ Current restricted words retrieval
- ✅ Direct Bad Words API testing

## 🔧 How It Works

### 1. Initialization
When the system starts, it:
1. Attempts to load restricted words from the Bad Words API
2. Falls back to a comprehensive local list if needed
3. Logs the number of words loaded

### 2. Text Checking Process
For each text check:
1. **Local Check**: Uses the local restricted words list
2. **API Check**: Sends text to Bad Words API for validation
3. **Combined Decision**: Merges both results for final decision
4. **Response**: Returns detailed analysis with confidence levels

### 3. Dynamic Updates
You can update the restricted words list by:
- Testing specific words against the API
- Adding new words manually
- Loading from external files

## 📊 Benefits

### Enhanced Accuracy
- **Real-time Validation**: Uses current API data
- **Combined Approach**: Local + API checking
- **Fallback Protection**: Works even if API is down

### Better Performance
- **Cached Results**: Stores API-confirmed words locally
- **Efficient Checking**: Combines multiple validation methods
- **Rate Limiting**: Respects API usage limits

### Flexibility
- **Customizable Lists**: Add/remove words as needed
- **Multiple Sources**: File, API, or manual input
- **Easy Updates**: Simple API calls to refresh lists

## 🚨 Rate Limiting

The Bad Words API has rate limits. The system includes:
- **Delays between requests**: 0.5-1 second intervals
- **Error handling**: Graceful fallback on API failures
- **Caching**: Stores results to minimize API calls

## 🔒 Security Considerations

- **API Key Protection**: Store keys in environment variables for production
- **Input Validation**: All text inputs are sanitized
- **Error Handling**: No sensitive information in error logs
- **Fallback Security**: Local checking continues if API fails

## 🛠️ Customization

### Modify Word Lists
```python
# In content_monitoring_system.py
custom_words = [
    'your_custom_word_1',
    'your_custom_word_2',
    # Add more words...
]

# Update the system
pipeline.text_monitor.restricted_words.update(custom_words)
```

### Change API Configuration
```python
# Use environment variables for production
self.bad_words_api_key = os.environ.get("BAD_WORDS_API_KEY", "default_key")
self.bad_words_api_url = os.environ.get("BAD_WORDS_API_URL", "default_url")
```

### Custom Validation Logic
```python
# Override the validation method
def custom_validation(self, text: str) -> Dict:
    # Your custom logic here
    pass
```

## 📈 Monitoring and Logging

The system provides comprehensive logging:
- **API Calls**: Track API usage and responses
- **Word Updates**: Monitor restricted words changes
- **Performance**: Track response times and accuracy
- **Errors**: Log API failures and fallbacks

## 🚀 Production Deployment

### Environment Variables
```bash
export BAD_WORDS_API_KEY="your_api_key_here"
export BAD_WORDS_API_URL="https://api.api-ninjas.com/v1/profanityfilter"
```

### Docker Configuration
```dockerfile
ENV BAD_WORDS_API_KEY=your_api_key_here
ENV BAD_WORDS_API_URL=https://api.api-ninjas.com/v1/profanityfilter
```

### Health Checks
Monitor API health with:
```bash
curl http://localhost:5001/api/health
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Invalid**
   - Check your API key in the configuration
   - Verify API key permissions

2. **Rate Limiting**
   - Increase delays between API calls
   - Implement request queuing

3. **API Unavailable**
   - System falls back to local checking
   - Check API status and network connectivity

4. **High Response Times**
   - Optimize API call frequency
   - Implement caching strategies

### Debug Mode
Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Additional Resources

- [API-Ninjas Documentation](https://api-ninjas.com/)
- [Bad Words API Endpoint](https://api.api-ninjas.com/v1/profanityfilter)
- [Content Monitoring System](content_monitoring_system.py)
- [API Server](api_server.py)

## 🎯 Next Steps

1. **Test the Integration**: Run `test_bad_words_api.py`
2. **Customize Word Lists**: Add domain-specific terms
3. **Monitor Performance**: Track API usage and accuracy
4. **Scale Up**: Implement caching and optimization
5. **Deploy**: Move to production with proper security

---

**Your decentralized social media DApp now has enterprise-grade content filtering powered by the Bad Words API! 🚀**
