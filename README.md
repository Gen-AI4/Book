# The Book - AI Teaching Assistant Backend

This is the backend service for The Book AI Teaching Assistant, a Physical AI system with RAG capabilities. This FastAPI backend serves as the "Mind" of the textbook. It uses OpenAI Chat Completions for reasoning and Qdrant for context retrieval (RAG system).

## Prerequisites

- Python 3.9 or higher
- Access to OpenAI API key
- Access to Qdrant Cloud or local Qdrant instance
- Access to Cohere API key (for embeddings)

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_COLLECTION_NAME=textbook_content
   ```

## Running the Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat` - Main chat endpoint for RAG functionality
- `GET /docs` - Interactive API documentation (Swagger UI)

## Usage

### Chat Endpoint

The main endpoint is `POST /chat` which accepts a JSON payload:

```json
{
  "message": "What does the textbook say about quantum computing?",
  "history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help you with the textbook?"
    }
  ]
}
```

The response will be in the format:

```json
{
  "response": "The textbook explains quantum computing as...",
  "context_retrieved": true,
  "sources": ["chapter_1.md", "chapter_2.md"],
  "timestamp": "2025-12-20T10:00:00Z"
}
```

## Architecture

The system follows a service-oriented architecture:

- `main.py`: FastAPI application with endpoints
- `models.py`: Pydantic models for request/response validation
- `services/`: Business logic services
  - `context_retrieval_service.py`: Qdrant integration and context retrieval
  - `openai_service.py`: OpenAI API integration
  - `chat_service.py`: Orchestrates the RAG flow
- `config.py`: Configuration and environment variables
- `utils.py`: Utility functions
- `middleware.py`: Rate limiting and other middleware

## Features

- **RAG Implementation**: Retrieves relevant context from Qdrant before generating responses
- **Caching**: Implements caching for context retrieval to improve performance
- **Error Handling**: Graceful degradation when external services are unavailable
- **Rate Limiting**: Protects the API with rate limiting
- **Validation**: Comprehensive request/response validation
- **Logging**: Structured logging for monitoring and debugging
- **Streaming**: Supports streaming responses (not implemented in this version but the service is prepared for it)

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL to your Qdrant instance
- `QDRANT_API_KEY`: Qdrant API key (if using cloud)
- `QDRANT_COLLECTION_NAME`: Name of the collection to query
- `COHERE_API_KEY`: Your Cohere API key
- `ENVIRONMENT`: Environment (development, staging, production) - defaults to "development"

## Hugging Face Space Deployment

This backend is configured to run on Hugging Face Spaces. The following files are used for deployment:

- `app.py`: Main entry point for the Hugging Face Space
- `requirements.txt`: Python dependencies
- `backend/`: Directory containing the main backend application

## Endpoints

When deployed on Hugging Face Spaces, the API endpoints are available at:
- `GET /` - Health check
- `GET /health` - Health status
- `GET /docs` - Interactive API documentation (Swagger UI)
- `POST /chat` - Main chat endpoint for RAG functionality