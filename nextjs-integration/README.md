# Next.js Integration with Content Monitoring ML Model

This directory contains the Next.js integration files for your Content Monitoring ML Model API.

## 🚀 **What We've Built**

✅ **Python ML Model** - Your existing content monitoring system (unchanged)  
✅ **Flask API Server** - Wraps your ML model with HTTP endpoints  
✅ **Next.js Integration** - Frontend components to use the ML model  

## 📁 **Files Structure**

```
ML MODEL/
├── content_monitoring_system.py    # Your ML model (unchanged)
├── api_server.py                   # Flask API server
├── nextjs-integration/            # Next.js integration files
│   ├── README.md                  # This file
│   ├── lib/
│   │   └── mlApi.ts              # API client for Next.js
│   ├── components/
│   │   ├── ContentSubmission.tsx  # Content submission form
│   │   ├── ContentChecker.tsx     # Real-time content checker
│   │   └── ModerationDashboard.tsx # Admin dashboard
│   └── pages/
│       └── api/                   # Next.js API routes (optional)
└── requirements.txt               # Python dependencies
```

## 🔧 **Setup Instructions**

### **Step 1: Start the ML Model API Server**

```bash
cd "ML MODEL"
python api_server.py
```

The server will start on `http://localhost:5001`

### **Step 2: Copy Integration Files to Your Next.js App**

Copy the files from `nextjs-integration/` to your Next.js project:

```bash
# Copy to your Next.js project
cp -r nextjs-integration/* /path/to/your/nextjs-app/
```

### **Step 3: Install Dependencies**

```bash
npm install axios
# or
yarn add axios
```

### **Step 4: Update Environment Variables**

Create `.env.local` in your Next.js project:

```env
NEXT_PUBLIC_ML_API_URL=http://localhost:5001/api
```

## 🎯 **Available API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/check-content` | POST | Check text + image content |
| `/api/check-text-only` | POST | Check text content only |
| `/api/check-image-only` | POST | Check image content only |
| `/api/stats` | GET | Get monitoring statistics |
| `/api/config` | GET/PUT | Get/update configuration |
| `/api/restricted-words` | GET/POST | Get/add restricted words |

## 📱 **Usage Examples**

### **Basic Content Checking**

```tsx
import { checkContent } from '@/lib/mlApi';

const handleSubmit = async (content: string) => {
  try {
    const result = await checkContent(content);
    
    if (result.action === 'allow') {
      // Content is safe - proceed with posting
      console.log('Content approved');
    } else {
      // Content blocked - show warning
      console.log('Content blocked:', result.message);
    }
  } catch (error) {
    console.error('Error checking content:', error);
  }
};
```

### **Image Content Checking**

```tsx
import { checkContent } from '@/lib/mlApi';

const handleImageUpload = async (file: File) => {
  try {
    const result = await checkContent('', file);
    
    if (result.action === 'allow') {
      // Image is safe
      console.log('Image approved');
    } else {
      // Image blocked
      console.log('Image blocked:', result.message);
    }
  } catch (error) {
    console.error('Error checking image:', error);
  }
};
```

## 🌐 **Production Deployment**

### **Option 1: Same Server**

Deploy both Next.js and ML API on the same server:

```bash
# Start ML API on production port
python api_server.py --port 8000

# Update Next.js environment
NEXT_PUBLIC_ML_API_URL=http://yourdomain.com:8000/api
```

### **Option 2: Separate Servers**

Deploy ML API on a dedicated server:

```bash
# ML API server
NEXT_PUBLIC_ML_API_URL=https://ml-api.yourdomain.com/api

# Next.js app
NEXT_PUBLIC_ML_API_URL=https://yourdomain.com/api
```

### **Option 3: Docker Deployment**

```dockerfile
# Dockerfile for ML API
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "api_server.py"]
```

## 🔒 **Security Considerations**

- **Rate Limiting**: Implement rate limiting on your ML API
- **Authentication**: Add API key authentication for production
- **HTTPS**: Use HTTPS in production
- **Input Validation**: Validate all inputs before sending to ML model
- **Error Handling**: Don't expose internal ML model errors to users

## 📊 **Monitoring and Analytics**

### **Track API Usage**

```tsx
// Log content checks for analytics
const logContentCheck = async (content: string, result: any) => {
  await fetch('/api/analytics/log', {
    method: 'POST',
    body: JSON.stringify({
      content_length: content.length,
      decision: result.overall_decision,
      timestamp: new Date().toISOString()
    })
  });
};
```

### **Performance Metrics**

- Response time for content checks
- Accuracy of ML model predictions
- User satisfaction with moderation decisions
- False positive/negative rates

## 🚀 **Next Steps**

1. **Customize Components**: Adapt the components to your app's design
2. **Add Authentication**: Integrate with your user authentication system
3. **Implement Caching**: Cache repeated content checks for performance
4. **Add Analytics**: Track moderation effectiveness and user behavior
5. **Scale Up**: Deploy to production with proper monitoring

## 🆘 **Troubleshooting**

### **Common Issues**

1. **CORS Errors**: Ensure Flask-CORS is properly configured
2. **Port Conflicts**: Change port if 5001 is already in use
3. **ML Model Loading**: Check if all dependencies are installed
4. **Memory Issues**: Monitor memory usage for large ML models

### **Debug Mode**

Enable debug mode in Flask for development:

```python
# In api_server.py
app.run(debug=True, port=5001)
```

## 📞 **Support**

If you encounter issues:

1. Check the API server logs
2. Verify all dependencies are installed
3. Test individual API endpoints with curl
4. Check the ML model is working independently

---

**Your ML model is now fully integrated with Next.js! 🎉**
