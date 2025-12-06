"""
FAISS indexing module for fast similarity search.
"""

from typing import List, Tuple, Dict, Any
import json
import numpy as np
import faiss
from src.config import EMBEDDING_DIM, DOCS_PATH, INDEX_PATH
from src.embedder import Embedder


class FAISSIndexer:
    """FAISS-based indexer for document similarity search."""
    
    def __init__(self, embedding_dim: int = EMBEDDING_DIM):
        """
        Initialize the FAISS indexer.
        
        Args:
            embedding_dim: Dimension of the embeddings
        """
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.documents: List[Dict[str, Any]] = []
        self.embedder = Embedder()
    
    def load_documents(self, docs_path: str = DOCS_PATH) -> None:
        """
        Load documents from JSON file.
        
        Args:
            docs_path: Path to the documents JSON file
        """
        with open(docs_path, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
    
    def build_index(self) -> None:
        """Build FAISS index from loaded documents."""
        if not self.documents:
            raise ValueError("No documents loaded. Call load_documents() first.")
        
        texts = [doc['content'] for doc in self.documents]
        embeddings = self.embedder.encode(texts, normalize=True)
        self.index.add(embeddings.astype('float32'))
    
    def save_index(self, index_path: str = INDEX_PATH) -> None:
        """
        Save FAISS index to disk.
        
        Args:
            index_path: Path to save the index
        """
        faiss.write_index(self.index, index_path)
    
    def load_index(self, index_path: str = INDEX_PATH) -> None:
        """
        Load FAISS index from disk.
        
        Args:
            index_path: Path to the saved index
        """
        self.index = faiss.read_index(index_path)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for similar documents given a query.
        
        Args:
            query: Query text
            top_k: Number of top results to return
            
        Returns:
            List of (document, score) tuples sorted by relevance
        """
        query_embedding = self.embedder.encode_single(query, normalize=True)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        scores, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(score)))
        
        return results
