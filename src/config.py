"""
Configuration settings for the Knowledge Base Recommendation System.
"""

# Model configuration
MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM: int = 384

# File paths
INDEX_PATH: str = "data/faiss_index.bin"
DOCS_PATH: str = "data/documents.json"

# Search configuration
TOP_K: int = 5
