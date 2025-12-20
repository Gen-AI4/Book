# Research: Frontend-Backend Connection

## Decision: API Client Implementation
**Rationale**: Need to create a utility function that can POST data to the backend endpoint at `http://localhost:8000/chat`
**Alternatives considered**:
- Using axios library vs native fetch API
- Using GraphQL vs REST API
- Decision: Use native fetch API as specified in requirements

## Decision: UI Feedback Mechanism
**Rationale**: Implement loading state to show "Typing..." indicator while waiting for backend response
**Alternatives considered**:
- Simple text indicator vs spinner animation
- Different loading states for different operations
- Decision: Implement "Typing..." text as specified in requirements

## Decision: Error Handling Approach
**Rationale**: Handle connection failures gracefully by displaying "Connection Failed" message
**Alternatives considered**:
- Different error message wording
- Additional retry mechanisms
- Decision: Display exact "Connection Failed" message as specified

## Decision: Markdown Rendering Solution
**Rationale**: Render bot responses with Markdown support for formatting (bold, italics, code blocks)
**Alternatives considered**:
- Using react-markdown library
- Using marked.js with custom renderer
- Using dangerouslySetInnerHTML with sanitization
- Decision: Use react-markdown with remark-gfm for comprehensive Markdown support

## Decision: State Management Pattern
**Rationale**: Use React Hooks (`useState`) for managing chat state as specified
**Alternatives considered**:
- Using Redux for state management
- Using Context API for global state
- Decision: Use React's built-in useState and useEffect hooks as specified

## Decision: Component Integration Point
**Rationale**: Update `src/components/ChatWidget` to replace mock data with real API calls
**Alternatives considered**:
- Creating a new component vs modifying existing
- Different component organization patterns
- Decision: Modify existing ChatWidget component to maintain consistency

## Decision: End-to-End Testing Approach
**Rationale**: Test integration by running both Docusaurus and FastAPI servers simultaneously
**Alternatives considered**:
- Mock backend for testing
- Integration tests vs manual testing
- Decision: Real server integration testing as specified in requirements