// TypeScript interfaces
export interface ChatRequest {
  message: string;
  session_id?: string; // optional for multi-turn sessions
  timestamp?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  status: string;
  timestamp: string;
}

export interface ChatError {
  error: string;
  status: string;
  timestamp: string;
}

// Browser-safe API URL
const getApiBaseUrl = (): string => {
  // Check if we're in a browser environment and if API_BASE_URL is defined
  if (typeof window !== 'undefined' && (window as any).API_BASE_URL) {
    return (window as any).API_BASE_URL;
  }

  // For production, use your deployed backend URL
  // For Vercel deployment, you may need to set this to your actual backend URL
  // Or use relative paths if your backend is properly configured with your frontend
  if (typeof window !== 'undefined') {
    const currentOrigin = window.location.origin;

    // If we're on localhost, use local backend
    if (currentOrigin.includes('localhost') || currentOrigin.includes('127.0.0.1')) {
      return 'http://localhost:8000'; // Your local FastAPI backend
    }

    // For production deployment, use environment variable if available
    if (process.env.REACT_APP_API_URL) {
      return process.env.REACT_APP_API_URL;
    }

    // Check for common deployment patterns
    if (currentOrigin.includes('vercel.app')) {
      // If on Vercel, you might need to deploy backend separately
      // Try to use the Hugging Face Space as fallback, but also consider other options
      return 'https://ahmedali021-the-book.hf.space';
    } else if (currentOrigin.includes('netlify.app')) {
      // If on Netlify, use appropriate backend URL
      return 'https://ahmedali021-the-book.hf.space';
    } else if (currentOrigin.includes('github.io')) {
      // If on GitHub Pages, use appropriate backend URL
      return 'https://ahmedali021-the-book.hf.space';
    }

    // Fallback to the original URL
    const backendUrl = 'https://ahmedali021-the-book.hf.space';

    // Log the backend URL being used for debugging
    console.log('Using backend URL:', backendUrl);

    return backendUrl;
  }

  // Fallback for server-side rendering
  return 'https://ahmedali021-the-book.hf.space';
};

// Check if backend is accessible
export const checkBackendHealth = async (): Promise<boolean> => {
  const API_BASE_URL = getApiBaseUrl();

  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
};

// Send chat message to backend
export const sendChatMessage = async (
  request: ChatRequest,
  timeout = 20000 // Increased timeout for backend processing
): Promise<ChatResponse> => {
  const API_BASE_URL = getApiBaseUrl();
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    console.log('Making request to:', `${API_BASE_URL}/chat`, 'with data:', request);

    // Check if we're trying to reach the backend
    if (!API_BASE_URL || API_BASE_URL === '') {
      throw new Error('No backend API URL configured');
    }

    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    clearTimeout(id);
    console.log('Response received:', response.status, response);

    // If server returns error, read full text for debugging
    if (!response.ok) {
      const text = await response.text().catch(() => '');
      console.error('Server Response (raw):', text);

      let errorMessage = `HTTP Error: ${response.status}`;
      try {
        const errorData: ChatError = JSON.parse(text);
        errorMessage = errorData.error || errorMessage;
      } catch {
        // response is not JSON, keep default message
      }

      throw new Error(errorMessage);
    }

    // Parse response JSON
    const data: ChatResponse = await response.json();
    console.log('Response data:', data);
    return data;

  } catch (error: any) {
    clearTimeout(id);
    console.error('API call failed:', error);

    // Provide more specific error messages based on error type
    if (error.name === 'AbortError') {
      throw new Error('Request timed out - Backend may be slow to respond');
    }
    if (error instanceof TypeError) {
      throw new Error('Connection failed - Backend service may be down. Please ensure the backend service is running and accessible. If running locally, make sure the backend is started on http://localhost:8000.');
    }
    throw error;
  }
};
