/**
 * ML Model API Client for Next.js
 * 
 * This client provides easy access to your Content Monitoring ML Model API
 * without changing any code in your Python ML model.
 */

// API base URL - update this in your .env.local
const ML_API_BASE = process.env.NEXT_PUBLIC_ML_API_URL || 'http://localhost:5001/api';

// Types for API responses
export interface ContentCheckResult {
  action: 'allow' | 'block';
  message: string;
  overall_decision: 'safe' | 'unsafe';
  block_content: boolean;
  reason: string[];
  text_check?: {
    is_restricted: boolean;
    restricted_words: string[];
    severity: number;
    method: string;
    confidence?: number;
  };
  image_check?: {
    category: string;
    confidence: number;
    is_safe: boolean;
    all_predictions?: Record<string, number>;
  };
  user_id?: string;
  user_warning?: boolean;
  content_removed?: boolean;
  timestamp: string;
}

export interface HealthCheckResult {
  status: 'healthy' | 'unhealthy';
  message: string;
  ml_model_ready: boolean;
  endpoints: string[];
}

export interface StatsResult {
  total_violations: number;
  text_violations: number;
  image_violations: number;
  recent_violations: number;
}

export interface ConfigResult {
  text_threshold: number;
  image_threshold: number;
  auto_block: boolean;
  log_violations: boolean;
  violation_log_file: string;
}

export interface RestrictedWordsResult {
  restricted_words: string[];
  count: number;
}

// Utility function to convert file to base64
const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = error => reject(error);
  });
};

// Main content checking function
export const checkContent = async (
  text: string = '',
  image?: File,
  userId?: string
): Promise<ContentCheckResult> => {
  try {
    let imageBase64: string | undefined;
    
    if (image) {
      imageBase64 = await fileToBase64(image);
    }
    
    const response = await fetch(`${ML_API_BASE}/check-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        image: imageBase64,
        user_id: userId,
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error checking content:', error);
    throw error;
  }
};

// Check text content only (faster for text-only posts)
export const checkTextOnly = async (
  text: string,
  userId?: string
): Promise<ContentCheckResult> => {
  try {
    const response = await fetch(`${ML_API_BASE}/check-text-only`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        user_id: userId,
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error checking text content:', error);
    throw error;
  }
};

// Check image content only
export const checkImageOnly = async (
  image: File,
  userId?: string
): Promise<ContentCheckResult> => {
  try {
    const imageBase64 = await fileToBase64(image);
    
    const response = await fetch(`${ML_API_BASE}/check-image-only`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image: imageBase64,
        user_id: userId,
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error checking image content:', error);
    throw error;
  }
};

// Health check
export const checkHealth = async (): Promise<HealthCheckResult> => {
  try {
    const response = await fetch(`${ML_API_BASE}/health`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

// Get statistics
export const getStats = async (): Promise<StatsResult> => {
  try {
    const response = await fetch(`${ML_API_BASE}/stats`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting stats:', error);
    throw error;
  }
};

// Get configuration
export const getConfig = async (): Promise<ConfigResult> => {
  try {
    const response = await fetch(`${ML_API_BASE}/config`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting config:', error);
    throw error;
  }
};

// Update configuration
export const updateConfig = async (config: Partial<ConfigResult>): Promise<{ message: string; config: ConfigResult }> => {
  try {
    const response = await fetch(`${ML_API_BASE}/config`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error updating config:', error);
    throw error;
  }
};

// Get restricted words
export const getRestrictedWords = async (): Promise<RestrictedWordsResult> => {
  try {
    const response = await fetch(`${ML_API_BASE}/restricted-words`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting restricted words:', error);
    throw error;
  }
};

// Add restricted words
export const addRestrictedWords = async (words: string | string[]): Promise<{ message: string; total_count: number }> => {
  try {
    const response = await fetch(`${ML_API_BASE}/restricted-words`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        words: Array.isArray(words) ? words : [words],
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error adding restricted words:', error);
    throw error;
  }
};

// Real-time content monitoring hook (for React components)
export const useContentMonitoring = () => {
  const checkContentRealtime = async (
    text: string,
    image?: File,
    userId?: string
  ): Promise<ContentCheckResult> => {
    // For real-time checking, use text-only endpoint if no image
    if (!image) {
      return await checkTextOnly(text, userId);
    }
    
    // If both text and image, use combined endpoint
    return await checkContent(text, image, userId);
  };

  const isContentSafe = (result: ContentCheckResult): boolean => {
    return result.overall_decision === 'safe';
  };

  const getContentSeverity = (result: ContentCheckResult): 'low' | 'medium' | 'high' => {
    if (result.text_check?.severity) {
      if (result.text_check.severity > 0.5) return 'high';
      if (result.text_check.severity > 0.2) return 'medium';
      return 'low';
    }
    return 'low';
  };

  return {
    checkContentRealtime,
    isContentSafe,
    getContentSeverity,
    checkContent,
    checkTextOnly,
    checkImageOnly,
    checkHealth,
    getStats,
    getConfig,
    updateConfig,
    getRestrictedWords,
    addRestrictedWords,
  };
};

// Error handling utilities
export class MLAPIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public endpoint?: string
  ) {
    super(message);
    this.name = 'MLAPIError';
  }
}

// Retry utility for failed requests
export const withRetry = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> => {
  let lastError: Error;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
      }
    }
  }
  
  throw lastError!;
};

// Batch content checking for multiple items
export const checkMultipleContent = async (
  items: Array<{ text?: string; image?: File; userId?: string }>
): Promise<ContentCheckResult[]> => {
  const results: ContentCheckResult[] = [];
  
  for (const item of items) {
    try {
      if (item.image) {
        const result = await checkContent(item.text || '', item.image, item.userId);
        results.push(result);
      } else if (item.text) {
        const result = await checkTextOnly(item.text, item.userId);
        results.push(result);
      }
    } catch (error) {
      console.error('Error checking content item:', error);
      // Add error result
      results.push({
        action: 'block',
        message: 'Error checking content',
        overall_decision: 'unsafe',
        block_content: true,
        reason: ['Content check failed'],
        timestamp: new Date().toISOString(),
      });
    }
  }
  
  return results;
};

export default {
  checkContent,
  checkTextOnly,
  checkImageOnly,
  checkHealth,
  getStats,
  getConfig,
  updateConfig,
  getRestrictedWords,
  addRestrictedWords,
  useContentMonitoring,
  withRetry,
  checkMultipleContent,
};
