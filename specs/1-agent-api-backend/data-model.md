# Data Model: Agent API Backend

## Entity: Message
- **Purpose**: Represents a single message in a conversation
- **Fields**:
  - `role`: string (user|assistant|system) - The role of the message sender
  - `content`: string - The actual message content
  - `timestamp`: datetime - When the message was created
  - `id`: string (optional) - Unique identifier for the message

## Entity: ChatRequest
- **Purpose**: Represents the input to the chat endpoint
- **Fields**:
  - `message`: string (required) - The user's current message
  - `history`: list[Message] (optional, default: []) - Previous conversation history
  - `context_window`: integer (optional, default: 5) - Number of previous messages to consider
  - `temperature`: float (optional, default: 0.7) - OpenAI temperature parameter
  - `max_tokens`: integer (optional, default: 1000) - Maximum tokens in response

## Entity: ChatResponse
- **Purpose**: Represents the output from the chat endpoint
- **Fields**:
  - `response`: string - The generated response from the LLM
  - `context_retrieved`: boolean - Whether relevant context was retrieved from Qdrant
  - `sources`: list[string] (optional) - List of source documents used for context
  - `timestamp`: datetime - When the response was generated
  - `id`: string (optional) - Unique identifier for the response

## Entity: ContextItem
- **Purpose**: Represents a piece of context retrieved from Qdrant
- **Fields**:
  - `id`: string - Unique identifier for the context item
  - `content`: string - The actual content of the context
  - `score`: float - Relevance score from Qdrant search
  - `source`: string - Source document or location
  - `metadata`: dict - Additional metadata about the context item

## Entity: Conversation
- **Purpose**: Represents an entire conversation session
- **Fields**:
  - `id`: string - Unique identifier for the conversation
  - `messages`: list[Message] - All messages in the conversation
  - `created_at`: datetime - When the conversation started
  - `updated_at`: datetime - When the conversation was last updated
  - `user_id`: string (optional) - Identifier for the user (if authentication is implemented)

## Entity: Embedding
- **Purpose**: Represents an embedding vector for semantic search
- **Fields**:
  - `id`: string - Unique identifier for the embedding
  - `vector`: list[float] - The actual embedding vector
  - `text`: string - The original text that was embedded
  - `source_document`: string - The document this embedding was derived from
  - `created_at`: datetime - When the embedding was created

## Relationships

### Message → Conversation
- A Message belongs to one Conversation
- A Conversation contains many Messages
- Cardinality: Many-to-One

### ContextItem → ChatResponse
- A ChatResponse may reference multiple ContextItems
- A ContextItem may be referenced by multiple ChatResponses
- Cardinality: Many-to-Many (through response metadata)

## Validation Rules

### ChatRequest Validation
- `message` must be between 1 and 10000 characters
- `history` length must not exceed 50 messages
- `temperature` must be between 0.0 and 2.0
- `context_window` must be between 1 and 20
- `max_tokens` must be between 1 and 4000

### Message Validation
- `role` must be one of: "user", "assistant", "system"
- `content` must not be empty
- `timestamp` defaults to current time if not provided

### ContextItem Validation
- `score` must be between 0.0 and 1.0
- `content` must not be empty
- `source` must be a valid identifier

## State Transitions

### Conversation State Transitions
- `active` → `inactive` (after 30 minutes of inactivity)
- `inactive` → `archived` (after 30 days of inactivity)
- `active` → `archived` (manually by user)

## Indexes

### Conversation Indexes
- Index on `user_id` for efficient user conversation retrieval
- Index on `updated_at` for chronological ordering

### ContextItem Indexes
- Index on `source` for efficient source-based queries
- Index on `score` for relevance-based sorting