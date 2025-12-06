# Knowledge Base Recommendation System

A production-ready semantic search system for internal knowledge base documents using Sentence-BERT embeddings and FAISS for fast similarity search.

## Overview

This system enables intelligent document retrieval from an internal knowledge base using natural language queries. It leverages state-of-the-art sentence embeddings to understand semantic meaning and returns the most relevant documents ranked by similarity score.

## Features

- **Semantic Search**: Uses Sentence-BERT (all-MiniLM-L6-v2) for understanding query intent
- **Fast Retrieval**: FAISS index enables sub-millisecond search across thousands of documents
- **REST API**: Clean FastAPI endpoints for easy integration
- **Production-Ready**: Proper error handling, type hints, and modular architecture
- **Normalized Scoring**: L2-normalized embeddings with inner product similarity
- **Scalable Design**: Efficient indexing and search operations

## Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  FastAPI Endpoint   │
│    (/search)        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Sentence-BERT      │
│  Embedding Model    │
│  (384-dim vector)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   FAISS Index       │
│ (Inner Product)     │
│  Similarity Search  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Ranked Results     │
│  (Top-K Documents)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   JSON Response     │
│ {id, title, score}  │
└─────────────────────┘
```

## Tech Stack

- **Python 3.8+**
- **FastAPI**: Modern web framework for building APIs
- **Sentence-Transformers**: Pre-trained SBERT models for embeddings
- **FAISS**: Facebook AI Similarity Search for efficient vector search
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment

## Project Structure

```
kbs-recommender/
│
├── api/
│   └── main.py                 # FastAPI application and endpoints
│
├── src/
│   ├── config.py              # Configuration constants
│   ├── embedder.py            # Sentence-BERT wrapper
│   ├── indexer.py             # FAISS indexing and search
│   ├── search.py              # High-level search service
│   └── utils.py               # Helper functions
│
├── data/
│   ├── documents.json         # Knowledge base documents
│   └── faiss_index.bin        # FAISS index (generated)
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                # Git ignore rules
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kbs-recommender
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API Server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Knowledge Base Recommendation System"
}
```

### Search Documents

**Endpoint**: `POST /search`

**Request Body**:
```json
{
  "query": "How do I reset my password?",
  "top_k": 5
}
```

**Response**:
```json
{
  "query": "How do I reset my password?",
  "results": [
    {
      "id": "KB001",
      "title": "Password Reset Guide",
      "content": "To reset your password, navigate to the login page...",
      "score": 0.8542
    },
    {
      "id": "KB005",
      "title": "Multi-Factor Authentication (MFA) Setup and Troubleshooting",
      "content": "MFA is required for all company accounts...",
      "score": 0.6231
    }
  ],
  "count": 2
}
```

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I connect to VPN?",
    "top_k": 3
  }'
```

### Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "How do I connect to VPN?",
        "top_k": 3
    }
)

results = response.json()
for doc in results["results"]:
    print(f"{doc['title']}: {doc['score']}")
```

### Using JavaScript Fetch

```javascript
fetch('http://localhost:8000/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'How do I connect to VPN?',
    top_k: 3
  })
})
.then(res => res.json())
.then(data => console.log(data.results));
```

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

Edit `src/config.py` to customize:

- `MODEL_NAME`: Sentence-BERT model (default: all-MiniLM-L6-v2)
- `EMBEDDING_DIM`: Embedding dimension (default: 384)
- `TOP_K`: Default number of results (default: 5)
- `INDEX_PATH`: FAISS index file location
- `DOCS_PATH`: Documents JSON file location

## Adding New Documents

Edit `data/documents.json` and add new entries:

```json
{
  "id": "KB007",
  "title": "Your Document Title",
  "content": "Your document content here..."
}
```

Restart the server to rebuild the index automatically.

## Performance

- **Embedding Generation**: ~10ms per query (CPU)
- **FAISS Search**: <1ms for 1000 documents
- **End-to-End Latency**: ~15-20ms per request
- **Scalability**: Handles 10K+ documents efficiently on CPU

## Future Improvements

- [ ] Add document upload endpoint for dynamic knowledge base updates
- [ ] Implement user feedback loop for relevance tuning
- [ ] Add caching layer (Redis) for frequent queries
- [ ] Support for multi-language documents
- [ ] Hybrid search combining semantic + keyword matching
- [ ] Document versioning and change tracking
- [ ] Analytics dashboard for search patterns
- [ ] GPU support for faster embedding generation
- [ ] Batch search endpoint for multiple queries
- [ ] Authentication and rate limiting
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests
- [ ] Monitoring and logging with Prometheus/Grafana

## License

MIT License

## Contact

For questions or support, contact the AI Engineering Team.
