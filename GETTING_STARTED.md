# Getting Started with Knowledge Base Recommendation System

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Sentence-Transformers (embeddings)
- FAISS (vector search)
- Pydantic (validation)

### Step 2: Start the Server

**Windows:**
```bash
run_server.bat
```

**macOS/Linux:**
```bash
chmod +x run_server.sh
./run_server.sh
```

**Or manually:**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Test the API

Open a new terminal and run:

```bash
python test_api.py
```

Or test manually:

```bash
curl http://localhost:8000/health
```

## 📖 Understanding the System

### What Happens on First Run?

1. **Model Download** (~90MB): Sentence-BERT model downloads automatically
2. **Document Loading**: Reads 6 documents from `data/documents.json`
3. **Embedding Generation**: Converts documents to 384-dim vectors (~2 seconds)
4. **Index Building**: Creates FAISS index for fast search
5. **Index Saving**: Saves to `data/faiss_index.bin` for future use

### What Happens on Subsequent Runs?

1. **Fast Startup**: Loads pre-built index from disk (~100ms)
2. **Ready to Search**: API is immediately available

## 🔍 Using the API

### Interactive Documentation

Visit: http://localhost:8000/docs

This provides a beautiful Swagger UI where you can:
- See all endpoints
- Try requests directly in the browser
- View request/response schemas

### Example Queries

**1. Password Reset:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "I forgot my password", "top_k": 2}'
```

**2. VPN Issues:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Cannot connect to company network remotely", "top_k": 3}'
```

**3. New Employee:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "First day at work setup", "top_k": 2}'
```

### Python Client Example

```python
import requests

def search_kb(query: str, top_k: int = 5):
    response = requests.post(
        "http://localhost:8000/search",
        json={"query": query, "top_k": top_k}
    )
    return response.json()

# Use it
results = search_kb("How do I reset my password?")
for doc in results["results"]:
    print(f"{doc['title']}: {doc['score']:.4f}")
```

### JavaScript/TypeScript Example

```javascript
async function searchKB(query, topK = 5) {
  const response = await fetch('http://localhost:8000/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK })
  });
  return await response.json();
}

// Use it
const results = await searchKB('VPN connection help');
console.log(results);
```

## 🎯 Understanding the Results

### Response Format

```json
{
  "query": "How do I reset my password?",
  "results": [
    {
      "id": "KB001",
      "title": "Password Reset Guide",
      "content": "To reset your password...",
      "score": 0.8542
    }
  ],
  "count": 1
}
```

### Score Interpretation

- **0.8 - 1.0**: Highly relevant (exact match)
- **0.6 - 0.8**: Very relevant (strong semantic match)
- **0.4 - 0.6**: Moderately relevant (related topic)
- **0.0 - 0.4**: Weakly relevant (tangential)

Scores are normalized cosine similarities (inner product of L2-normalized vectors).

## 🔧 Customization

### Adding New Documents

Edit `data/documents.json`:

```json
{
  "id": "KB007",
  "title": "Your New Document",
  "content": "Your content here..."
}
```

Then restart the server to rebuild the index.

### Changing Configuration

Edit `src/config.py`:

```python
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Change model
EMBEDDING_DIM = 384  # Must match model dimension
TOP_K = 5  # Default number of results
```

### Using a Different Model

Popular alternatives:
- `all-mpnet-base-v2` (768-dim, more accurate, slower)
- `all-MiniLM-L12-v2` (384-dim, balanced)
- `paraphrase-multilingual-MiniLM-L12-v2` (multi-language)

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Run from project root directory

### Issue: "Port 8000 already in use"
**Solution**: 
```bash
uvicorn api.main:app --port 8001
```

### Issue: "FAISS index not found"
**Solution**: Normal on first run - index will be created automatically

### Issue: Slow first request
**Solution**: Normal - model loads on first request (~2-3 seconds)

### Issue: Out of memory
**Solution**: Reduce batch size or use smaller model

## 📊 Performance Tips

### For Faster Startup
- Keep the generated `data/faiss_index.bin` file
- Don't delete it between runs

### For Better Results
- Use more descriptive document content
- Add more documents (system scales to 10K+ easily)
- Use a larger model (e.g., all-mpnet-base-v2)

### For Production
- Use GPU for faster embedding generation
- Add Redis caching for frequent queries
- Implement batch search endpoint
- Add monitoring and logging

## 🎓 Next Steps

1. **Explore the Code**: Start with `api/main.py` and follow the imports
2. **Add Your Documents**: Replace sample data with real knowledge base
3. **Customize**: Adjust configuration for your use case
4. **Deploy**: Containerize with Docker, deploy to cloud
5. **Enhance**: Add features from the "Future Improvements" section

## 📚 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Sentence-Transformers**: https://www.sbert.net/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Vector Search**: https://www.pinecone.io/learn/vector-search/

## 💬 Common Questions

**Q: Can I use this for production?**
A: Yes! Add authentication, monitoring, and proper error handling.

**Q: How many documents can it handle?**
A: 10K+ on CPU, millions with GPU and optimized FAISS indices.

**Q: Does it support multiple languages?**
A: Use a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2`.

**Q: Can I deploy this to AWS/GCP/Azure?**
A: Yes! It's a standard FastAPI app - deploy like any Python web service.

**Q: How do I add authentication?**
A: Add FastAPI security dependencies (OAuth2, API keys, etc.).

---

**Need Help?** Check the README.md for detailed documentation or open an issue.
