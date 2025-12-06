# Quick Setup Guide

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test the API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Search Example:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How do I reset my password?\", \"top_k\": 3}"
```

## Access Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## First Run

On first startup, the system will:
1. Load documents from `data/documents.json`
2. Generate embeddings using Sentence-BERT
3. Build FAISS index
4. Save index to `data/faiss_index.bin`

Subsequent runs will load the pre-built index for faster startup.

## Troubleshooting

**Issue**: Module not found errors
**Solution**: Make sure you're running from the project root directory

**Issue**: Port already in use
**Solution**: Change port: `uvicorn api.main:app --port 8001`

**Issue**: Slow first request
**Solution**: Normal - model loads on first request (takes ~2-3 seconds)
