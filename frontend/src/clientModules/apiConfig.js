// Client module to set API_BASE_URL based on environment
// This runs during the build process and sets the API URL globally

// Set the API base URL based on environment
if (typeof window !== 'undefined') {
  // For production, use the environment variable or fallback to the Hugging Face Space
  // For development, use localhost
  const isDevelopment = process.env.NODE_ENV === 'development';

  if (!window.API_BASE_URL) {
    window.API_BASE_URL = isDevelopment
      ? 'http://localhost:8000'
      : process.env.API_BASE_URL || 'https://ahmedali021-the-book.hf.space';
  }
}

export default {};