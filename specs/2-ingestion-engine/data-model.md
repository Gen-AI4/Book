# Data Model: Ingestion Engine Backend

**Feature**: 2-ingestion-engine
**Created**: 2025-12-20

## Entities

### Textbook Content
- **Description**: Represents a section/chapter from the Physical AI textbook
- **Fields**:
  - `id` (string): Unique identifier for the content chunk
  - `source_url` (string): URL where the content was extracted from
  - `chapter_title` (string): Title of the textbook chapter/section
  - `content_text` (string): The actual text content
  - `vector_embedding` (array[float]): 1024-dimensional vector representation
  - `metadata` (object): Additional information including section, timestamp
  - `created_at` (datetime): Timestamp of when the content was processed

### Vector Database Record
- **Description**: Represents a stored vector in Qdrant with associated metadata
- **Fields**:
  - `id` (string): Unique identifier for the vector record
  - `vector` (array[float]): 1024-dimensional embedding vector
  - `payload` (object): Metadata object containing:
    - `source_url` (string): Origin URL of the content
    - `chapter_title` (string): Title of the chapter
    - `content_text` (string): Original text chunk
    - `section` (string): Section identifier if applicable
    - `processed_at` (datetime): When the content was ingested

## Relationships

### Content to Vector Mapping
- One `Textbook Content` entity maps to one `Vector Database Record`
- The `content_text` is transformed into `vector` via embedding process
- Original content metadata is preserved in `payload`

## Validation Rules

### Textbook Content Validation
- `source_url` must be a valid URL format
- `content_text` must not exceed 10MB in size
- `vector_embedding` must be exactly 1024 dimensions
- `chapter_title` must not be empty

### Vector Database Record Validation
- `vector` array must have exactly 1024 elements
- `payload` must contain required metadata fields
- `id` must be unique within the collection

## State Transitions

### Content Processing Flow
1. **Raw Content**: Retrieved from textbook URL
2. **Chunked Content**: Split into manageable text chunks
3. **Embedded Content**: Vector embedding generated
4. **Stored Content**: Saved to Qdrant with metadata