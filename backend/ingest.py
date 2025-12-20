import os
import uuid
import hashlib
import logging
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_all_urls(base_url: str) -> List[str]:
    """
    Retrieves all textbook page URLs from the deployed site.
    """
    logger.info(f"Fetching URLs from base URL: {base_url}")

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        urls = set()

        # Find all links in the navigation or content area
        # For Docusaurus sites, common patterns include:
        # - Links in the sidebar navigation
        # - Links in the main content area
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Convert relative URLs to absolute URLs
            if href.startswith('/'):
                full_url = base_url.rstrip('/') + href
            elif href.startswith(base_url):
                full_url = href
            else:
                continue  # Skip external links

            # Filter for textbook content pages (not navigation, etc.)
            if '/docs/' in full_url or full_url.endswith('.html') or full_url.count('/') >= 3:
                urls.add(full_url)

        logger.info(f"Found {len(urls)} URLs")
        return list(urls)

    except requests.RequestException as e:
        logger.error(f"Error fetching URLs from {base_url}: {e}")
        raise e

def extract_text_from_url(url: str) -> str:
    """
    Extracts clean text content from a specific URL, handling Docusaurus site structure.
    Includes handling for large content files and malformed text.
    """
    logger.info(f"Extracting text from URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find main content area in Docusaurus sites
        # Common selectors for Docusaurus content
        content_selectors = [
            'article',  # Main article content
            '.markdown',  # Markdown content
            '.main-content',  # Main content area
            '.doc-content',  # Documentation content
            '.container',  # Container that holds content
            'main',  # Main content area
        ]

        text_content = ""
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                text_content = content_element.get_text(separator=' ', strip=True)
                break

        # If no specific content area found, get all text
        if not text_content:
            text_content = soup.get_text(separator=' ', strip=True)

        # Clean up the text content
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = ' '.join(chunk for chunk in chunks if chunk)

        # Handle special characters and potential encoding issues
        # Remove null bytes and other problematic characters
        text_content = text_content.replace('\x00', '').strip()

        # Check if content is too large (over 10MB) and handle appropriately
        if len(text_content) > 10 * 1024 * 1024:  # 10MB in characters
            logger.warning(f"Content from {url} is very large ({len(text_content)} chars), consider streaming approach")
            # For now, we'll still process it, but in a real implementation we might want to use streaming
            # or process in smaller chunks to avoid memory issues

        logger.info(f"Extracted {len(text_content)} characters from {url}")
        return text_content

    except requests.RequestException as e:
        logger.error(f"Error extracting text from {url}: {e}")
        raise e
    except UnicodeDecodeError as e:
        logger.error(f"Unicode decode error extracting text from {url}: {e}")
        # Return empty string for malformed content
        return ""
    except MemoryError as e:
        logger.error(f"Memory error extracting text from {url} (content likely too large): {e}")
        # Return empty string for memory issues
        return ""
    except Exception as e:
        logger.error(f"Unexpected error extracting text from {url}: {e}")
        # For other parsing errors, return empty string rather than failing completely
        return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits text into manageable chunks with appropriate overlap.
    """
    logger.info(f"Chunking text of {len(text)} characters with chunk_size={chunk_size}, overlap={overlap}")

    # Use RecursiveCharacterTextSplitter for better text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_text(text)
    logger.info(f"Text split into {len(chunks)} chunks")

    return chunks

def get_embeddings(text_list: List[str]) -> List[List[float]]:
    """
    Generate vector embeddings using Cohere API with batch processing.
    Uses embed-english-v3.0 model with input_type="search_document" as specified.
    """
    logger.info(f"Generating embeddings for {len(text_list)} text chunks")

    # Initialize Cohere client
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY must be set in environment variables")

    co = cohere.Client(cohere_api_key)

    # Process in batches to respect API limits (up to 96 texts per request)
    batch_size = 96
    all_embeddings = []

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]

        # Add retry logic with exponential backoff for rate limits
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = co.embed(
                    texts=batch,
                    model="embed-english-v3.0",  # Using v3.0 as specified
                    input_type="search_document"  # As specified for document storage
                )

                batch_embeddings = response.embeddings
                all_embeddings.extend(batch_embeddings)
                logger.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(text_list)-1)//batch_size + 1}")
                break  # Success, exit retry loop

            except cohere.CohereAPIError as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff
                    logger.warning(f"Rate limit hit, retrying in {wait_time} seconds... (attempt {retry_count}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Cohere API error: {e}")
                    raise e
            except Exception as e:
                logger.error(f"Unexpected error during embedding: {e}")
                raise e

        if retry_count == max_retries:
            raise Exception(f"Failed to generate embeddings after {max_retries} retries")

    logger.info(f"Successfully generated embeddings for {len(all_embeddings)} text chunks")
    return all_embeddings

def save_chunk_to_qdrant(chunk: str, embedding: List[float], metadata: Dict) -> bool:
    """
    Store vectors with metadata in Qdrant.
    Uses deterministic UUIDs based on content hash to prevent duplicate entries.
    """
    logger.info(f"Saving chunk to Qdrant with metadata: {metadata.get('source_url', 'Unknown URL')}")

    # Validate embedding dimensions (must be exactly 1024 for Cohere embeddings)
    if len(embedding) != 1024:
        logger.error(f"Invalid embedding dimension: {len(embedding)}, expected 1024")
        return False

    # Initialize Qdrant client
    qdrant_host = os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_host or not qdrant_api_key:
        raise ValueError("QDRANT_HOST and QDRANT_API_KEY must be set in environment variables")

    client = QdrantClient(
        url="https://16b332a7-4011-462d-a698-10f2e3df8e6e.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.WDsCBIfwgPQSnM55VTDs1T8f_GihKGacXZ_mBxgSUP4",
    )

    # Generate deterministic UUID based on content hash
    content_to_hash = chunk + str(metadata)
    content_hash = hashlib.md5(content_to_hash.encode()).hexdigest()
    # Convert hex to a valid UUID format
    point_id = str(uuid.UUID(content_hash[:32]))

    # Prepare the payload with the raw text chunk in 'page_content' field
    payload = {
        "page_content": chunk,  # As specified to allow RAG agent to retrieve text later
        **metadata  # Include all other metadata
    }

    try:
        # Upsert the point to Qdrant
        client.upsert(
            collection_name="physical_ai_textbook",
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )
        logger.info(f"Successfully saved chunk to Qdrant with ID: {point_id}")
        return True

    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {e}")
        return False

def process_docs_folder(base_url: str = "https://the-book-iota.vercel.app/"):
    """
    Process all documents from the specified base URL, following the ingestion pipeline.
    Includes checkpointing mechanism for partial failure recovery and progress reporting.
    """
    logger.info(f"Starting ingestion process for base URL: {base_url}")

    # Get all URLs from the textbook site
    urls = get_all_urls(base_url)
    total_urls = len(urls)
    logger.info(f"Found {total_urls} URLs to process")

    total_processed = 0
    total_errors = 0

    # Checkpoint file to track progress
    checkpoint_file = "ingestion_checkpoint.txt"

    # Load checkpoint if it exists
    processed_urls = set()
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            processed_urls = set(line.strip() for line in f.readlines())
        logger.info(f"Loaded checkpoint: {len(processed_urls)} URLs already processed")

    # Calculate starting position for progress reporting
    start_index = len(processed_urls)

    for i, url in enumerate(urls):
        # Skip already processed URLs
        if url in processed_urls:
            # Report progress for skipped URLs
            progress = (i + 1) / total_urls * 100
            logger.info(f"Progress: {progress:.1f}% ({i + 1}/{total_urls}) - Skipping already processed: {url}")
            continue

        # Report progress
        progress = (i + 1) / total_urls * 100
        logger.info(f"Progress: {progress:.1f}% ({i + 1}/{total_urls}) - Processing URL: {url}")

        try:
            # Extract text content from the URL
            text_content = extract_text_from_url(url)

            if not text_content.strip():
                logger.warning(f"No content extracted from {url}, skipping...")
                # Mark as processed even if no content
                with open(checkpoint_file, 'a') as f:
                    f.write(f"{url}\n")
                continue

            # Chunk the text content
            text_chunks = chunk_text(text_content)

            # Generate embeddings for the chunks
            embeddings = get_embeddings(text_chunks)

            # Save each chunk with its embedding to Qdrant
            for j, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
                # Prepare metadata
                metadata = {
                    "source_url": url,
                    "chapter_title": url.split('/')[-1].replace('-', ' ').title(),  # Simple title extraction
                    "chunk_index": j,
                    "content_preview": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }

                success = save_chunk_to_qdrant(chunk, embedding, metadata)
                if success:
                    total_processed += 1
                else:
                    total_errors += 1
                    logger.error(f"Failed to save chunk {j} from {url}")

            # Mark URL as processed in checkpoint
            with open(checkpoint_file, 'a') as f:
                f.write(f"{url}\n")

        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            total_errors += 1

    logger.info(f"Ingestion process completed. Successfully processed: {total_processed} chunks, Errors: {total_errors}")
    return total_processed, total_errors

def main():
    """
    Main function to coordinate the entire ingestion process.
    """
    logger.info("Starting the textbook content ingestion pipeline...")

    try:
        # Ensure the collection exists before starting
        from init_db import create_collection_if_not_exists
        create_collection_if_not_exists("physical_ai_textbook")

        # Process the textbook content
        processed, errors = process_docs_folder()

        logger.info(f"Ingestion pipeline completed. Processed: {processed} chunks, Errors: {errors}")

        if errors == 0:
            logger.info("All content ingested successfully!")
        else:
            logger.warning(f"Completed with {errors} errors.")

    except Exception as e:
        logger.error(f"Critical error in ingestion pipeline: {e}")
        raise e

if __name__ == "__main__":
    main()