# ADR 1: Backend Framework Selection and RAG Architecture

## Status
Accepted

## Date
2025-12-20

## Context
We need to build a FastAPI backend that serves as the "Mind" of the textbook with RAG (Retrieval Augmented Generation) capabilities. The system needs to:
- Integrate with OpenAI for reasoning capabilities
- Use Qdrant for context retrieval
- Handle conversation history
- Return streaming responses
- Align with project constitution principles

Several architectural decisions need to be made regarding the technology stack and integration patterns that will significantly impact how engineers write and structure the software.

## Decision
We will use the following technology stack and architectural approach:

### Backend Framework
- **Framework**: FastAPI with Uvicorn ASGI server
- **Rationale**: FastAPI provides excellent performance, built-in async support, automatic API documentation, and strong typing with Pydantic

### RAG Architecture Components
- **LLM Integration**: OpenAI ChatCompletions API with system prompt injection
- **Vector Store**: Qdrant for context retrieval
- **Embedding Service**: Cohere for embedding generation
- **API Structure**: Standard FastAPI app with CORS middleware

### Integration Pattern
- **Service Layer Architecture**: Implement service layer abstraction for Qdrant integration to ensure testability
- **Streaming Response**: Use FastAPI's StreamingResponse with async generator for real-time responses
- **Error Handling**: Implement graceful degradation with appropriate HTTP status codes

## Alternatives Considered

### Backend Framework Alternatives
1. **Flask**: More mature but slower performance, no built-in async support, less typing support
2. **Django**: Overkill for API-only service, heavier framework with more boilerplate
3. **Express.js**: Would require switching to Node.js ecosystem, not aligned with Python focus

### RAG Architecture Alternatives
1. **OpenAI Assistant API**: More complex setup, less control over prompt construction, vendor lock-in
2. **Self-hosted embeddings**: More infrastructure complexity but better cost control and privacy
3. **Different vector stores**: Pinecone, Weaviate, or Vespa - would require different integration patterns

### Response Strategy Alternatives
1. **Server-Sent Events (SSE)**: More complex to implement, requires additional client-side handling
2. **WebSocket connections**: Overkill for chat interface, adds connection management complexity
3. **Regular HTTP response**: Would require waiting for complete response before sending to client

### Error Handling Alternatives
1. **Fail silently with fallback responses**: Could hide important issues from clients
2. **Return explicit error messages**: Might expose sensitive information about system internals
3. **Complete service shutdown**: Would make the entire API unavailable when external services fail

## Consequences

### Positive Consequences
- FastAPI provides excellent performance with async support for handling concurrent requests
- Built-in automatic API documentation (Swagger UI) for easy testing and integration
- Strong typing with Pydantic models reduces runtime errors
- Qdrant integration provides efficient vector search capabilities
- Streaming responses improve user experience with real-time output
- Service layer abstraction enables better testability and maintainability
- Cohere embeddings provide high-quality semantic search capabilities

### Negative Consequences
- Additional dependency on external services (OpenAI, Qdrant, Cohere) creates potential failure points
- Ongoing costs associated with external API usage
- Potential rate limiting from external services
- Learning curve for team members unfamiliar with FastAPI patterns
- Possible vendor lock-in with OpenAI and Qdrant APIs

## References
- specs/1-agent-api-backend/plan.md
- specs/1-agent-api-backend/research.md
- specs/1-agent-api-backend/data-model.md
- .specify/memory/constitution.md