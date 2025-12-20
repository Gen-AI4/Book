# API Contract: Chat Endpoint

## Endpoint: POST /chat

### Description
Handles chat messages from the frontend and returns appropriate responses from the backend service.

### Request

#### URL
`http://localhost:8000/chat`

#### Method
`POST`

#### Headers
- `Content-Type: application/json`
- `Accept: application/json`

#### Request Body
```json
{
  "message": "string (required)",
  "session_id": "string (optional)",
  "timestamp": "ISO 8601 datetime string (optional)"
}
```

**Request Body Fields:**
- `message`: The user's message content (required)
- `session_id`: Unique identifier for the chat session (optional, server will generate if not provided)
- `timestamp`: Client-side timestamp (optional, server will set if not provided)

### Response

#### Success Response (200 OK)
```json
{
  "response": "string (required)",
  "session_id": "string (required)",
  "status": "success",
  "timestamp": "ISO 8601 datetime string (required)"
}
```

**Success Response Fields:**
- `response`: The chatbot's response message (required)
- `session_id`: The session identifier (required)
- `status`: Always "success" for successful responses (required)
- `timestamp`: Server timestamp for the response (required)

#### Error Response (400 Bad Request)
```json
{
  "error": "string (required)",
  "status": "error",
  "timestamp": "ISO 8601 datetime string (required)"
}
```

#### Server Error Response (500 Internal Server Error)
```json
{
  "error": "string (required)",
  "status": "error",
  "timestamp": "ISO 8601 datetime string (required)"
}
```

### Error Codes
- `400`: Invalid request format or missing required fields
- `500`: Server error processing the request
- `503`: Backend service unavailable (when FastAPI can't reach the underlying service)

### Example Request
```json
{
  "message": "Hello, how can you help me?",
  "session_id": "abc123xyz"
}
```

### Example Response
```json
{
  "response": "Hello! I can help you with information about our robotics curriculum. **Bold text** and `code blocks` are supported.",
  "session_id": "abc123xyz",
  "status": "success",
  "timestamp": "2025-12-20T10:30:00Z"
}
```