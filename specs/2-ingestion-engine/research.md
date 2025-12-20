# Research: Ingestion Engine Backend

**Feature**: 2-ingestion-engine
**Created**: 2025-12-20

## Qdrant Cloud Setup

### Decision: Qdrant Cloud Configuration
- **Rationale**: Qdrant Cloud provides managed vector database service with appropriate vector dimensions for Cohere embeddings
- **Vector Dimensions**: Cohere's embed-english-v3.0 model produces 1024-dimensional vectors
- **Collection Setup**: Need to create collection with 1024 vector size and appropriate distance metric (usually cosine)

### Required Configuration
- QDRANT_HOST: Cloud endpoint URL
- QDRANT_API_KEY: Authentication key
- Collection name: "textbook_embeddings"
- Vector size: 1024 (for Cohere embeddings)
- Distance metric: Cosine (most common for text embeddings)

## Cohere Embeddings

### Decision: Cohere API Usage
- **Model**: embed-english-v3.0 (recommended for text content)
- **Input Type**: "search_document" for textbook content
- **Batch Processing**: Cohere API supports up to 96 texts per request
- **Rate Limits**: Need to implement appropriate delays to respect API limits

### Embedding Parameters
- model: "embed-english-v3.0"
- texts: Array of text chunks
- input_type: "search_document" (optimized for search applications)

## Web Scraping Strategy

### Decision: Text Extraction from Deployed Site
- **Method**: Use requests + BeautifulSoup for reliable text extraction
- **Target**: Extract content from the deployed textbook at https://the-book-iota.vercel.app/
- **Selectors**: Need to identify the main content areas in the Docusaurus site structure

### Content Identification
- Docusaurus sites typically use .markdown or .mdx class containers
- Main content is usually within article or main tags
- Need to exclude navigation, headers, footers from extraction

## Text Chunking Strategy

### Decision: Recursive Character Splitting
- **Method**: RecursiveCharacterTextSplitter (common in LangChain)
- **Chunk Size**: 1000 characters (balance between context and API limits)
- **Overlap**: 100 characters (to maintain context across splits)
- **Separators**: ["\n\n", "\n", " ", ""] (hierarchical splitting)

### Chunking Considerations
- Maintain semantic coherence within chunks
- Avoid breaking up important concepts across chunks
- Respect document structure (sections, paragraphs)

## Environment Variables

### Required Variables
- COHERE_API_KEY: For authentication with Cohere API
- QDRANT_HOST: Qdrant Cloud endpoint
- QDRANT_API_KEY: Qdrant Cloud authentication
- BASE_URL: The textbook site URL (https://the-book-iota.vercel.app/)

## Error Handling Strategy

### Decision: Robust Error Handling
- Network timeout handling with retries
- API rate limit detection and backoff
- Partial failure recovery (checkpointing)
- Comprehensive logging for debugging