# Data Model: Chat Widget

## Entities

### Chat Message
- **id**: Unique identifier for the message
- **content**: Text content of the message (string)
- **sender**: Who sent the message - "user" or "bot" (string)
- **timestamp**: When the message was sent (datetime)
- **status**: Message status - "sent", "pending", "delivered", "error" (string, optional)

### Chat Session
- **id**: Unique identifier for the session
- **messages**: Array of Chat Message entities
- **createdAt**: When the session was started (datetime)
- **lastActive**: When the last message was sent (datetime)

## Validation Rules

### Chat Message
- Content must not be empty or exceed 1000 characters
- Sender must be either "user" or "bot"
- Timestamp must be in ISO 8601 format
- Status must be one of the allowed values if present

### Chat Session
- Must contain at least one message
- Maximum of 100 messages per session
- Session must be active within the last 24 hours

## State Transitions

### Message State Transitions
- `pending` → `delivered` (when successfully sent/received)
- `pending` → `error` (when sending/receiving fails)
- `delivered` → `read` (when user views the message)

### Session State Transitions
- New session starts with first user message
- Session remains active for 24 hours of inactivity
- Session can be explicitly closed by user