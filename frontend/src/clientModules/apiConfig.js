// Client module to set API_BASE_URL based on environment
// This runs during the build process and sets the API URL globally

// Set the API base URL based on environment
if (typeof window !== 'undefined') {
  // For production, use the environment variable or fallback to the Hugging Face Space
  // For development, use localhost
  const isDevelopment = process.env.NODE_ENV === 'development' || window.location.hostname.includes('localhost');

  if (!window.API_BASE_URL) {
    // Check for REACT_APP_API_URL environment variable first
    const envApiUrl = process.env.REACT_APP_API_URL;

    window.API_BASE_URL = envApiUrl ||
                          (isDevelopment ? 'http://localhost:8000' : 'https://ahmedali021-the-book.hf.space');
  }
}

export default {};