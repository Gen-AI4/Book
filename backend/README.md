# Textbook Content Ingestion Pipeline

This pipeline processes "Physical AI" textbook content from the deployed site, generates vector embeddings using Cohere, and stores them in Qdrant Cloud with appropriate metadata.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_HOST`: Your Qdrant Cloud endpoint
   - `QDRANT_API_KEY`: Your Qdrant API key

3. Make sure you have a Qdrant collection named `physical_ai_textbook` with 1024-dimensional vectors and cosine distance. This will be created automatically if it doesn't exist.

## Usage

Run the ingestion pipeline:
```bash
python ingest.py
```

## Features

- **Web Scraping**: Automatically discovers and extracts content from the textbook site
- **Text Chunking**: Splits content into manageable chunks with overlap for context preservation
- **Embedding Generation**: Uses Cohere's `embed-english-v3.0` model with `input_type="search_document"`
- **Vector Storage**: Stores embeddings in Qdrant with metadata (source URL, chapter title, content preview)
- **Duplicate Prevention**: Uses deterministic UUIDs based on content hash to prevent duplicate entries
- **Error Handling**: Includes retry logic for Cohere API rate limits and comprehensive error logging
- **Checkpointing**: Tracks progress to enable resumption after failures
- **Embedding Validation**: Ensures all embeddings have exactly 1024 dimensions

## Architecture

The pipeline consists of the following key functions:

- `get_all_urls(base_url)`: Discovers all textbook page URLs
- `extract_text_from_url(url)`: Extracts clean text content from a URL
- `chunk_text(text, chunk_size=500, overlap=50)`: Splits text into chunks
- `get_embeddings(texts)`: Generates vector embeddings using Cohere API
- `save_chunk_to_qdrant(chunk, embedding, metadata)`: Stores vectors in Qdrant
- `process_docs_folder(base_url)`: Main processing function
- `main()`: Coordinates the entire pipeline

## Configuration

- Default base URL: `https://the-book-iota.vercel.app/`
- Chunk size: 500 characters with 50-character overlap
- Cohere model: `embed-english-v3.0` with `input_type="search_document"`
- Vector dimension: 1024 (for Cohere embeddings)
- Distance metric: Cosine (for Qdrant collection)

## Troubleshooting

- If you encounter rate limit errors, the system will automatically retry with exponential backoff
- Check the ingestion_checkpoint.txt file to see which URLs have been processed
- Monitor the logs for detailed information about the ingestion process
- Verify your API keys and Qdrant connection details in the .env file