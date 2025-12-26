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

    // For production Vercel deployment, use the backend URL
    // Update this with your actual deployed backend URL
    // For now, using the Hugging Face Space URL as a fallback
    return 'https://ahmedali021-the-book.hf.space';
  }

  // Fallback for server-side rendering
  return 'https://ahmedali021-the-book.hf.space';
};

// Send chat message to backend
export const sendChatMessage = async (
  request: ChatRequest,
  timeout = 10000
): Promise<ChatResponse> => {
  const API_BASE_URL = getApiBaseUrl();
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    clearTimeout(id);

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
    return data;

  } catch (error: any) {
    clearTimeout(id);
    if (error.name === 'AbortError') throw new Error('Request timed out');
    if (error instanceof TypeError) throw new Error('Connection Failed');
    throw error;
  }
};
