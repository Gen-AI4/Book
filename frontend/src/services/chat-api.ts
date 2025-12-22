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
  return (window as any).API_BASE_URL || 'https://ahmedali021-the-book.hf.space';
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
