'use client';

import React, { useState, useCallback } from 'react';
import { checkContent, checkTextOnly, ContentCheckResult } from '../lib/mlApi';

interface ContentSubmissionProps {
  userId?: string;
  onContentApproved?: (content: string, image?: File) => void;
  onContentBlocked?: (result: ContentCheckResult) => void;
  className?: string;
}

export default function ContentSubmission({
  userId = 'anonymous',
  onContentApproved,
  onContentBlocked,
  className = ''
}: ContentSubmissionProps) {
  const [content, setContent] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [result, setResult] = useState<ContentCheckResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  // Handle image selection
  const handleImageChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  // Remove image
  const removeImage = useCallback(() => {
    setImage(null);
    setImagePreview(null);
  }, []);

  // Handle form submission
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!content.trim() && !image) {
      setError('Please provide text content or an image');
      return;
    }

    setIsChecking(true);
    setError(null);
    setResult(null);

    try {
      let checkResult: ContentCheckResult;

      if (image && content.trim()) {
        // Check both text and image
        checkResult = await checkContent(content, image, userId);
      } else if (image) {
        // Check image only
        checkResult = await checkContent('', image, userId);
      } else {
        // Check text only (faster)
        checkResult = await checkTextOnly(content, userId);
      }

      setResult(checkResult);

      if (checkResult.action === 'allow') {
        // Content is safe - notify parent component
        onContentApproved?.(content, image || undefined);
        
        // Reset form
        setContent('');
        setImage(null);
        setImagePreview(null);
      } else {
        // Content blocked - notify parent component
        onContentBlocked?.(checkResult);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check content');
      console.error('Content check error:', err);
    } finally {
      setIsChecking(false);
    }
  }, [content, image, userId, onContentApproved, onContentBlocked]);

  // Real-time content checking (optional)
  const handleContentChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
    setError(null);
    setResult(null);
  }, []);

  return (
    <div className={`max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg ${className}`}>
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Submit Content</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Text Content */}
        <div>
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
            Content
          </label>
          <textarea
            id="content"
            value={content}
            onChange={handleContentChange}
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={4}
            placeholder="What's on your mind?"
            disabled={isChecking}
          />
        </div>
        
        {/* Image Upload */}
        <div>
          <label htmlFor="image" className="block text-sm font-medium text-gray-700 mb-2">
            Image (optional)
          </label>
          
          {imagePreview ? (
            <div className="relative">
              <img
                src={imagePreview}
                alt="Preview"
                className="w-full h-48 object-cover rounded-lg border border-gray-300"
              />
              <button
                type="button"
                onClick={removeImage}
                className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
                disabled={isChecking}
              >
                ×
              </button>
            </div>
          ) : (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
              <input
                id="image"
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="hidden"
                disabled={isChecking}
              />
              <label htmlFor="image" className="cursor-pointer">
                <div className="text-gray-500">
                  <svg className="mx-auto h-12 w-12 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <p className="text-lg">Click to upload an image</p>
                  <p className="text-sm">PNG, JPG, GIF up to 10MB</p>
                </div>
              </label>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isChecking || (!content.trim() && !image)}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {isChecking ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Checking Content...
            </div>
          ) : (
            'Submit for Review'
          )}
        </button>
      </form>

      {/* Result Display */}
      {result && (
        <div className={`mt-6 p-4 rounded-lg border ${
          result.action === 'allow' 
            ? 'bg-green-50 border-green-200 text-green-800' 
            : 'bg-red-50 border-red-200 text-red-800'
        }`}>
          <div className="flex items-start">
            <div className="flex-shrink-0">
              {result.action === 'allow' ? (
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              )}
            </div>
            <div className="ml-3">
              <h3 className="text-lg font-medium">
                {result.action === 'allow' ? '✅ Content Approved' : '❌ Content Blocked'}
              </h3>
              <p className="mt-1">{result.message}</p>
              
              {result.reason && result.reason.length > 0 && (
                <div className="mt-3">
                  <p className="text-sm font-medium">Reasons:</p>
                  <ul className="mt-1 text-sm list-disc list-inside">
                    {result.reason.map((reason, index) => (
                      <li key={index}>{reason}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.text_check && result.text_check.restricted_words && result.text_check.restricted_words.length > 0 && (
                <div className="mt-3">
                  <p className="text-sm font-medium">Restricted words found:</p>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {result.text_check.restricted_words.map((word, index) => (
                      <span key={index} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        {word}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {result.user_warning && (
                <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-sm text-yellow-800">
                    ⚠️ This content violates our community guidelines. Please review and try again.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Content Guidelines */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Content Guidelines</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Be respectful and kind to others</li>
          <li>• No hate speech, harassment, or discrimination</li>
          <li>• No violent or inappropriate content</li>
          <li>• No spam or misleading information</li>
          <li>• Content is automatically reviewed before posting</li>
        </ul>
      </div>
    </div>
  );
}
