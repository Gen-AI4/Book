# Specification: Agent API Backend (The Brain)

## Overview
Build the FastAPI backend that serves as the "Mind" of the textbook. It uses OpenAI Agents SDK (or Chat Completions) to reason and Qdrant to retrieve context.

## User Scenarios & Testing

### Primary User Scenario
1. User sends a message through the chat interface
2. The system retrieves relevant context from Qdrant based on the user's message
3. The system constructs a system prompt with the retrieved context
4. The system calls the OpenAI API to generate a response
5. The system returns either a streaming response or JSON object with the answer

### Acceptance Scenarios
- Given a user sends a message with chat history, when the system processes the request, then it should retrieve relevant context and return an appropriate response
- Given a user sends a message with no relevant context, when the system processes the request, then it should return a response acknowledging the lack of context
- Given a user sends a malformed request, when the system receives it, then it should return an appropriate error message

### Edge Cases
- Network timeouts during API calls
- Invalid or malformed user input
- Empty chat history
- Very long user messages
- Qdrant service unavailable

## Functional Requirements

### FR1: API Structure
- The system shall provide a standard FastAPI application with CORS middleware enabled
- The system shall handle cross-origin requests appropriately
- The system shall provide proper error handling and logging

### FR2: RAG Endpoint
- The system shall provide a POST endpoint at `/chat` that accepts a JSON payload containing:
  - `message`: string representing the user's message
  - `history`: list representing the conversation history
- The system shall validate the input format and return appropriate error responses for invalid inputs
- The system shall return responses in JSON format or as a streaming response

### FR3: Agent Logic
- The system shall retrieve context from Qdrant based on the user's message
- The system shall construct a system prompt by injecting the retrieved context
- The system shall call the OpenAI API to generate the answer using the constructed prompt
- The system shall return the generated answer to the user

## Non-Functional Requirements

### Performance
- The system shall respond to chat requests within 5 seconds under normal load
- The system shall support up to 100 concurrent users

### Security
- The system shall implement proper authentication mechanisms
- The system shall protect against injection attacks
- The system shall securely handle API keys and sensitive data

### Availability
- The system shall be available 99.5% of the time
- The system shall gracefully degrade when external services are unavailable

## Success Criteria

### Quantitative Metrics
- 95% of chat requests return within 5 seconds
- Support for 100 concurrent users without performance degradation
- Less than 1% error rate in successful chat responses
- 99.5% uptime availability

### Qualitative Measures
- Users find the responses relevant and helpful
- The system provides contextual answers based on the retrieved information
- The system handles edge cases gracefully without crashing
- The system integrates seamlessly with the frontend application

## Key Entities

### Message Entity
- Contains the user's message content
- Associated with conversation history
- May trigger context retrieval from Qdrant

### Conversation Entity
- Contains the history of messages between user and system
- Maintains context across multiple interactions
- Used to provide continuity in conversations

### Context Entity
- Retrieved from Qdrant based on user input
- Injected into the system prompt for OpenAI
- Provides relevant information for response generation

## Assumptions

- OpenAI API is available and responsive
- Qdrant service contains relevant context for user queries
- User messages are in plain text format
- Chat history is stored in a compatible format
- Network connectivity is stable for external API calls

## Dependencies

- OpenAI API for language model access
- Qdrant for vector storage and retrieval
- Cohere for embedding generation
- FastAPI framework for API structure
- CORS middleware for cross-origin handling