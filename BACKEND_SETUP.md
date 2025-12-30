# Backend Setup and Configuration Guide

## Running the Backend Service

To run the backend service locally, follow these steps:

### 1. Navigate to the backend directory:
```bash
cd backend
```

### 2. Install dependencies (if not already installed):
```bash
pip install -r requirements.txt
# Or if no requirements.txt exists:
pip install fastapi uvicorn python-dotenv
```

### 3. Start the backend server:
```bash
# Using uvicorn directly:
uvicorn main:app --reload --port 8000

# Or using the provided script:
python -c "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')"
```

### 4. Verify the backend is running:
- Visit `http://localhost:8000/health` to check if the service is healthy
- You should see a response like: `{"status": "healthy", "timestamp": "..."}`

## Environment Variables

Make sure your environment variables are properly configured:

### Backend (.env in backend directory):
```env
COHERE_API_KEY="your-cohere-api-key"
QDRANT_HOST="your-qdrant-host"
QDRANT_API_KEY="your-qdrant-api-key"
QDRANT_COLLECTION_NAME="textbook_content"
OPENROUTER_API_KEY="your-openrouter-api-key"
BASE_URL="https://the-book-iota.vercel.app"
```

### Frontend (.env in frontend directory):
```env
REACT_APP_API_URL=http://localhost:8000
```

## Frontend Configuration

The frontend will automatically detect the environment and use the appropriate backend URL:

- **Local development**: Uses `http://localhost:8000`
- **Production**: Uses the URL specified in `REACT_APP_API_URL` environment variable, falling back to `https://ahmedali021-the-book.hf.space`

## Troubleshooting

### Common Issues:

1. **Connection Failed Error**:
   - Make sure the backend service is running on the expected port (8000)
   - Check that your firewall isn't blocking the connection
   - Verify CORS settings in the backend

2. **CORS Errors**:
   - The backend has CORS configured for common development origins
   - If deploying to a custom domain, add it to the CORS allowlist in `backend/main.py`

3. **API Key Issues**:
   - Ensure all required API keys are set in your environment variables
   - Check that the keys are valid and have the necessary permissions

### Testing the Connection:

1. Test the health endpoint: `curl http://localhost:8000/health`
2. Test the chat endpoint:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello"}'
   ```

## Production Deployment

For production deployment:

1. Ensure your backend is deployed and accessible at a public URL
2. Update the `REACT_APP_API_URL` environment variable in your frontend deployment to point to your backend URL
3. Update CORS settings in the backend to allow requests from your frontend domain