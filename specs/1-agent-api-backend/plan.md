# Implementation Plan: Agent API Backend (The Brain)

## Technical Context

### Current State
- FastAPI backend needed to serve as the "Mind" of the textbook
- Requires integration with OpenAI for reasoning capabilities
- Needs Qdrant for context retrieval (RAG system)
- Must accept user messages and conversation history
- Should return streaming responses or JSON objects

### Architecture Overview
- **Framework**: FastAPI with Uvicorn server
- **LLM**: OpenAI (GPT-4o or GPT-3.5-Turbo)
- **Retrieval**: Cohere embeddings + Qdrant vector store
- **API Structure**: Standard FastAPI app with CORS middleware
- **Endpoint**: POST /chat with message and history parameters

### Dependencies
- FastAPI framework
- Uvicorn ASGI server
- OpenAI Python library
- Qdrant client library
- Cohere embedding library
- CORS middleware
- Pydantic for request/response models

### Integration Points
- Connects to Qdrant for context retrieval
- Calls OpenAI API for response generation
- Expects to receive message and history from frontend
- May integrate with existing ingestion pipeline from Spec 2

## Constitution Check

### Sim-to-Real Transfer Focus
- The API will be designed to handle real-time queries efficiently
- Response times will be optimized for interactive use
- Hardware constraints around API latency will be considered

### Multi-Modal Learning Approach
- The API will support text-based interactions with the textbook content
- Integration with existing Docusaurus frontend planned
- Compatible with ROS 2, Gazebo, NVIDIA Isaac, and VLA documentation systems

### Test-First for Educational Content
- All API endpoints will have comprehensive test coverage
- Integration tests will verify RAG functionality
- Example usage will be documented with runnable code snippets

### Hardware-Aware Implementation
- API will be optimized for server deployment on target hardware
- Resource usage will be monitored and optimized
- Performance benchmarks will be established for API response times

### Interactive Learning Experience
- The RAG chatbot will be embedded in the Docusaurus textbook
- Context-aware Q&A functionality will be provided
- Real-time interaction capabilities will be supported

### Modular Curriculum Design
- The API will be designed as a standalone module
- Clear interfaces will allow for independent development
- Integration points with other modules will be well-defined

## Phase 0: Research & Unknowns Resolution

### Research Tasks

#### 1. FastAPI with Streaming Response Implementation
**Decision**: How to implement streaming responses in FastAPI
**Rationale**: Need to determine the best approach for streaming OpenAI responses
**Alternatives considered**:
- Using StreamingResponse with async generator
- Server-Sent Events (SSE)
- WebSocket connections
**Chosen approach**: StreamingResponse with async generator for simplicity and compatibility

#### 2. Qdrant Integration Pattern
**Decision**: How to integrate Qdrant for context retrieval
**Rationale**: Need to establish the most efficient way to retrieve context based on user queries
**Alternatives considered**:
- Direct Qdrant client integration
- Service layer abstraction
- Repository pattern
**Chosen approach**: Service layer abstraction for better testability and maintainability

#### 3. OpenAI API Integration Strategy
**Decision**: How to structure OpenAI API calls with retrieved context
**Rationale**: Need to determine the best way to inject context into system prompts
**Alternatives considered**:
- Using ChatCompletions API directly
- OpenAI Assistant API
- Custom prompt engineering
**Chosen approach**: ChatCompletions API with system prompt injection for maximum control

#### 4. Error Handling Strategy
**Decision**: How to handle failures in external services (OpenAI, Qdrant)
**Rationale**: Need robust error handling for production use
**Alternatives considered**:
- Fail silently with fallback responses
- Return explicit error messages
- Graceful degradation
**Chosen approach**: Graceful degradation with appropriate HTTP status codes

## Phase 1: Design & Contracts

### Data Models

#### Message Entity
```python
class Message(BaseModel):
    """
    Represents a single message in a conversation
    """
    role: str  # "user", "assistant", or "system"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

#### ChatRequest Entity
```python
class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    message: str
    history: List[Message] = []
    context_window: int = 5  # Number of previous messages to consider
    temperature: float = 0.7  # OpenAI temperature parameter
```

#### ChatResponse Entity
```python
class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    response: str
    context_retrieved: bool
    sources: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### API Contracts

#### POST /chat
- **Purpose**: Main RAG endpoint for chat interactions
- **Request**: `application/json` with ChatRequest schema
- **Response**: `application/json` with ChatResponse schema or streaming text/event-stream
- **Status Codes**:
  - 200: Successful response
  - 400: Invalid request format
  - 422: Validation error
  - 500: Internal server error
  - 503: External service unavailable

#### Request Schema
```json
{
  "message": "string (required)",
  "history": [
    {
      "role": "string (user|assistant|system)",
      "content": "string"
    }
  ],
  "context_window": "integer (optional, default: 5)",
  "temperature": "float (optional, default: 0.7)"
}
```

#### Response Schema
```json
{
  "response": "string",
  "context_retrieved": "boolean",
  "sources": ["string"],
  "timestamp": "ISO 8601 datetime"
}
```

### Architecture Components

#### 1. FastAPI Application Structure
- Main application with CORS middleware
- Health check endpoint
- OpenAPI documentation at /docs
- Custom exception handlers

#### 2. Context Retrieval Service
- Interface with Qdrant for vector search
- Embedding generation using Cohere
- Context ranking and filtering
- Caching for performance optimization

#### 3. OpenAI Service
- Interface with OpenAI API
- Prompt construction with retrieved context
- Response streaming capability
- Error handling and retry logic

#### 4. Chat Service
- Coordinates context retrieval and OpenAI calls
- Manages conversation history
- Handles response formatting
- Implements business logic

## Phase 2: Implementation Plan

### Task 1: Server Scaffold
- [ ] Create `backend/main.py` with FastAPI app
- [ ] Add CORS middleware configuration
- [ ] Implement basic health check endpoint
- [ ] Set up logging configuration
- [ ] Configure environment variables

### Task 2: Data Models and Validation
- [ ] Define Pydantic models for requests/responses
- [ ] Implement request validation
- [ ] Add custom validators where needed
- [ ] Create API documentation models

### Task 3: Qdrant Integration
- [ ] Create Qdrant client configuration
- [ ] Implement context retrieval service
- [ ] Add embedding generation with Cohere
- [ ] Implement context ranking logic
- [ ] Add caching mechanism

### Task 4: OpenAI Integration
- [ ] Create OpenAI client configuration
- [ ] Implement OpenAI service
- [ ] Add prompt construction with context
- [ ] Implement response streaming
- [ ] Add error handling and retry logic

### Task 5: Chat Endpoint
- [ ] Create the main /chat endpoint
- [ ] Integrate context retrieval and OpenAI services
- [ ] Implement conversation history management
- [ ] Add response formatting
- [ ] Implement streaming response option

### Task 6: Testing and Validation
- [ ] Write unit tests for all services
- [ ] Create integration tests for the API
- [ ] Implement end-to-end tests
- [ ] Add performance benchmarks
- [ ] Test error handling scenarios

### Task 7: Documentation and Deployment
- [ ] Update API documentation
- [ ] Create deployment configuration
- [ ] Add environment-specific configurations
- [ ] Create README with setup instructions
- [ ] Document API usage examples

## Risk Assessment

### High-Risk Areas
1. **External Service Dependencies**: OpenAI and Qdrant APIs may have availability issues
2. **Performance**: Vector search and LLM calls may introduce latency
3. **Cost Management**: OpenAI API usage can become expensive at scale

### Mitigation Strategies
1. **Caching**: Implement context caching to reduce API calls
2. **Timeouts**: Set appropriate timeouts for external services
3. **Fallbacks**: Provide graceful degradation when external services are unavailable
4. **Monitoring**: Implement comprehensive logging and monitoring

## Success Criteria

### Technical Metrics
- API response time under 5 seconds for 95% of requests
- Support for 100 concurrent users
- Less than 1% error rate in production
- 99.5% uptime availability

### Quality Metrics
- 90% code coverage for critical paths
- All API endpoints documented with examples
- Performance benchmarks established
- Error handling covers all external service failures