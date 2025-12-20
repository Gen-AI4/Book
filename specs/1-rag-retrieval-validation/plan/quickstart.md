# Quickstart Guide: RAG Retrieval Validation

**Feature**: RAG Retrieval Validation
**Created**: 2025-12-20
**Status**: Complete

## Prerequisites

Before running the RAG retrieval validation script, ensure you have:

1. **Python Environment**
   - Python 3.8 or higher
   - pip package manager

2. **API Access**
   - Cohere API key with embedding permissions
   - Qdrant Cloud instance with populated text chunks

3. **Environment Variables**
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_HOST`: Your Qdrant Cloud host URL
   - `QDRANT_API_KEY`: Your Qdrant Cloud API key
   - `QDRANT_COLLECTION`: Name of the collection to search (default: "text_chunks")

## Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install cohere qdrant-client python-dotenv
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_HOST=your_qdrant_host_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION=text_chunks
```

## Usage

### 1. Run the Validation Script
```bash
cd backend
python test_retrieval.py
```

### 2. Using the retrieve() Function
```python
from test_retrieval import retrieve

# Test with a sample query
results = retrieve("What is the hardware requirement?")
print(results)
```

### 3. Expected Output
The script will output the top 3 most relevant text chunks with their distance scores:

```
Query: "What is the hardware requirement?"

Result 1:
Distance: 0.1234
Content: "The minimum hardware requirement for this system is an RTX 40-series GPU..."

Result 2:
Distance: 0.2345
Content: "For optimal performance, use NVIDIA Jetson hardware with at least 8GB VRAM..."

Result 3:
Distance: 0.3456
Content: "Unitree platforms require specific drivers compatible with ROS 2..."
```

## Testing Examples

### Example Queries to Test
```python
# Test various types of queries
retrieve("What is the hardware requirement?")
retrieve("Explain the ROS 2 integration")
retrieve("How does the VLA system work?")
retrieve("What are the performance benchmarks?")
```

### Validation Process
1. Run your query through the validation script
2. Examine the distance scores (lower is more relevant)
3. Verify that the content matches the expected textbook content
4. Ensure the top 3 results are relevant to your query

## Troubleshooting

### Common Issues

#### API Connection Errors
- Verify your API keys are correct
- Check that your QDRANT_HOST URL is properly formatted
- Ensure your network allows connections to Cohere and Qdrant

#### No Results Returned
- Verify the QDRANT_COLLECTION name is correct
- Check that your vector database has been populated with text chunks
- Confirm the embedding model matches the one used for the stored vectors

#### High Distance Scores
- This may indicate the query doesn't match any stored content well
- Try rephrasing the query or checking the content in your vector database

## Next Steps

1. Integrate the validation script into your development workflow
2. Use it to test queries before deploying changes to the main RAG pipeline
3. Monitor the relevance of results over time to ensure quality