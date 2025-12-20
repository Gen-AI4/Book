# OpenAPI Contract: Agent API Backend

## API: Chat Endpoint
- **Path**: `/chat`
- **Method**: `POST`
- **Purpose**: Main RAG endpoint for chat interactions with context retrieval

### Request Body
```
{
  "message": "string (required) - The user's message to process",
  "history": [
    {
      "role": "string (required) - One of: user, assistant, system",
      "content": "string (required) - The message content"
    }
  ],
  "context_window": "integer (optional, default: 5) - Number of previous messages to consider",
  "temperature": "float (optional, default: 0.7) - OpenAI temperature parameter",
  "max_tokens": "integer (optional, default: 1000) - Maximum tokens in response"
}
```

### Response Body (Success - 200)
```
{
  "response": "string - The generated response from the LLM",
  "context_retrieved": "boolean - Whether relevant context was retrieved from Qdrant",
  "sources": ["string"] - List of source documents used for context",
  "timestamp": "ISO 8601 datetime - When the response was generated",
  "id": "string (optional) - Unique identifier for the response"
}
```

### Response Body (Streaming - 200)
```
Content-Type: text/event-stream
Data format: Server-Sent Events with JSON payloads
Example:
data: {"response": "Hello", "done": false}
data: {"response": " World", "done": false}
data: {"response": "", "done": true}
```

### Error Responses
- **400 Bad Request**: Invalid request format
```
{
  "detail": "string - Error message explaining the validation issue"
}
```

- **422 Unprocessable Entity**: Validation error
```
{
  "detail": [
    {
      "loc": ["string", "path", "to", "field"],
      "msg": "string - Validation error message",
      "type": "string - Error type"
    }
  ]
}
```

- **500 Internal Server Error**: Unexpected server error
```
{
  "detail": "string - Error message"
}
```

- **503 Service Unavailable**: External service (OpenAI/Qdrant) unavailable
```
{
  "detail": "string - Service temporarily unavailable"
}
```

## API: Health Check Endpoint
- **Path**: `/health`
- **Method**: `GET`
- **Purpose**: Check the health status of the API

### Response Body (Success - 200)
```
{
  "status": "string - Health status (e.g., 'healthy')",
  "timestamp": "ISO 8601 datetime - When the check was performed"
}
```

## API: Documentation Endpoint
- **Path**: `/docs`
- **Method**: `GET`
- **Purpose**: Interactive API documentation (Swagger UI)

## Security Requirements
- No authentication required for basic functionality
- Rate limiting should be implemented at the infrastructure level
- API keys for external services (OpenAI, Qdrant, Cohere) should be configured via environment variables

## Performance Requirements
- Response time: < 5 seconds for 95% of requests
- Concurrency: Support for 100+ concurrent connections
- Throughput: Handle 1000+ requests per minute

## Data Validation
- All string inputs should be sanitized to prevent injection attacks
- Message length should be limited to prevent abuse
- History array should have maximum length limits