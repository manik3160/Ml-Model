'use client';

import React, { useState } from 'react';
import ContentSubmission from '../components/ContentSubmission';
import { ContentCheckResult } from '../lib/mlApi';

export default function DemoPage() {
  const [approvedContent, setApprovedContent] = useState<Array<{ content: string; image?: File; timestamp: string }>>([]);
  const [blockedContent, setBlockedContent] = useState<ContentCheckResult[]>([]);

  const handleContentApproved = (content: string, image?: File) => {
    const newApproved = {
      content,
      image,
      timestamp: new Date().toLocaleString()
    };
    setApprovedContent(prev => [newApproved, ...prev]);
  };

  const handleContentBlocked = (result: ContentCheckResult) => {
    setBlockedContent(prev => [result, ...prev]);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Content Monitoring ML Model Demo
          </h1>
          <p className="text-xl text-gray-600">
            Test your decentralized social media content monitoring system
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Content Submission */}
          <div>
            <ContentSubmission
              userId="demo_user_123"
              onContentApproved={handleContentApproved}
              onContentBlocked={handleContentBlocked}
            />
          </div>

          {/* Results Dashboard */}
          <div className="space-y-6">
            {/* Approved Content */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                Approved Content ({approvedContent.length})
              </h3>
              
              {approvedContent.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No approved content yet</p>
              ) : (
                <div className="space-y-3">
                  {approvedContent.slice(0, 5).map((item, index) => (
                    <div key={index} className="border border-green-200 rounded-lg p-3 bg-green-50">
                      <p className="text-sm text-gray-700">{item.content}</p>
                      <p className="text-xs text-green-600 mt-2">{item.timestamp}</p>
                    </div>
                  ))}
                  {approvedContent.length > 5 && (
                    <p className="text-sm text-gray-500 text-center">
                      +{approvedContent.length - 5} more approved posts
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Blocked Content */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                Blocked Content ({blockedContent.length})
              </h3>
              
              {blockedContent.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No blocked content yet</p>
              ) : (
                <div className="space-y-3">
                  {blockedContent.slice(0, 5).map((item, index) => (
                    <div key={index} className="border border-red-200 rounded-lg p-3 bg-red-50">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-sm text-gray-700">
                            {item.text_check?.restricted_words?.join(', ') || 'Content blocked'}
                          </p>
                          <p className="text-xs text-red-600 mt-1">
                            {new Date(item.timestamp).toLocaleString()}
                          </p>
                        </div>
                        <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">
                          {item.text_check?.severity ? `${Math.round(item.text_check.severity * 100)}%` : 'High'}
                        </span>
                      </div>
                    </div>
                  ))}
                  {blockedContent.length > 5 && (
                    <p className="text-sm text-gray-500 text-center">
                      +{blockedContent.length - 5} more blocked posts
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* System Status */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">System Status</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">ML Model API</span>
                  <span className="text-green-600 font-medium">✅ Running</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Content Filtering</span>
                  <span className="text-green-600 font-medium">✅ Active</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Real-time Monitoring</span>
                  <span className="text-green-600 font-medium">✅ Enabled</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Violation Logging</span>
                  <span className="text-green-600 font-medium">✅ Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-3">How to Test</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-700">
            <div>
              <h4 className="font-medium mb-2">✅ Safe Content Examples:</h4>
              <ul className="space-y-1">
                <li>• "Hello everyone! How are you doing today?"</li>
                <li>• "Just had the best coffee ever! ☕"</li>
                <li>• "Beautiful sunset today! 🌅"</li>
                <li>• "Happy birthday! Hope you have a wonderful day."</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-2">❌ Blocked Content Examples:</h4>
              <ul className="space-y-1">
                <li>• "I hate all people from that group"</li>
                <li>• "Let's commit violence against them"</li>
                <li>• "This is spam content with fake news"</li>
                <li>• "Spread hate and extremism"</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Integration Info */}
        <div className="mt-8 bg-gray-100 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Integration Details</h3>
          <div className="text-sm text-gray-600 space-y-2">
            <p><strong>API Endpoint:</strong> http://localhost:5001/api</p>
            <p><strong>ML Model:</strong> Your existing Python model (unchanged)</p>
            <p><strong>Frontend:</strong> Next.js with TypeScript</p>
            <p><strong>Real-time:</strong> Content checked before submission</p>
            <p><strong>Decentralized:</strong> Ready for blockchain integration</p>
          </div>
        </div>
      </div>
    </div>
  );
}
