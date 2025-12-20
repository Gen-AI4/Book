// Define TypeScript interfaces
export interface ChatRequest {
  message: string;
  session_id?: string;
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

// Get API base URL from environment or default
const getApiBaseUrl = (): string => {
  // For Docusaurus, we use NEXT_PUBLIC_API_URL equivalent or default
  return (
    process.env.REACT_APP_API_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    'http://localhost:8000'
  );
};

// Function to send a chat message to the backend
export const sendChatMessage = async (
  request: ChatRequest
): Promise<ChatResponse> => {
  try {
    const API_BASE_URL = getApiBaseUrl();
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData: ChatError = await response.json().catch(() => ({
        error: `HTTP Error: ${response.status}`,
        status: 'error',
        timestamp: new Date().toISOString(),
      }));

      throw new Error(errorData.error || `HTTP Error: ${response.status}`);
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      // Network error
      throw new Error('Connection Failed');
    }
    throw error;
  }
};