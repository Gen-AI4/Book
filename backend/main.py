from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from services.chat_service import ChatService
from logging_config import setup_logging
from middleware import add_rate_limiting, limiter
from metrics import add_metrics_middleware, metrics_endpoint
import logging

# Setup logging
setup_logging()

app = FastAPI(title="Agent API Backend", description="The Brain of the textbook with RAG capabilities")

# Add metrics middleware
add_metrics_middleware(app)

# Add rate limiting
add_rate_limiting(app)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Docusaurus default port
        "http://localhost:3001",  # Alternative Docusaurus port
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://127.0.0.1:3001",  # Alternative localhost format
        "http://localhost:5173",  # Vite default port
        "http://localhost:3002",  # Additional common port
        "http://localhost:3003",  # Additional common port
        "http://localhost:3004",  # Additional common port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat service
chat_service = ChatService()

@app.get("/")
async def root():
    return {"message": "Agent API Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-12-20T00:00:00Z"}

@app.get("/metrics")
async def metrics():
    return await metrics_endpoint()

@app.post("/chat",
          summary="Chat with the Physical AI Teaching Assistant",
          description="Send a message to the AI assistant and receive a response based on the textbook content.",
          responses={
              200: {
                  "description": "Successful response from the AI assistant",
                  "content": {
                      "application/json": {
                          "example": {
                              "response": "The textbook explains quantum computing as...",
                              "context_retrieved": True,
                              "sources": ["chapter_1.md", "chapter_2.md"],
                              "timestamp": "2025-12-20T10:00:00Z"
                          }
                      }
                  }
              }
          })
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that processes user messages and returns AI-generated responses.

    Args:
        request (ChatRequest): The chat request containing the message and optional history

    Returns:
        ChatResponse: The AI-generated response with context information
    """
    try:
        # Process the chat request using the chat service
        response = await chat_service.process_chat_request(request)
        return response
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)