"""
Search service for formatting and managing search operations.
"""

from typing import List, Dict, Any
from src.indexer import FAISSIndexer
from src.config import TOP_K, DOCS_PATH, INDEX_PATH


class SearchService:
    """High-level search service for the recommendation system."""
    
    def __init__(self):
        """Initialize the search service with a FAISS indexer."""
        self.indexer = FAISSIndexer()
    
    def initialize(self, docs_path: str = DOCS_PATH, index_path: str = INDEX_PATH, rebuild: bool = False) -> None:
        """
        Initialize the search service by loading documents and index.
        
        Args:
            docs_path: Path to documents JSON file
            index_path: Path to FAISS index file
            rebuild: Whether to rebuild the index from scratch
        """
        self.indexer.load_documents(docs_path)
        
        if rebuild:
            self.indexer.build_index()
            self.indexer.save_index(index_path)
        else:
            try:
                self.indexer.load_index(index_path)
            except Exception:
                self.indexer.build_index()
                self.indexer.save_index(index_path)
    
    def search(self, query: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
        """
        Search for relevant documents and format results.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of formatted document dictionaries with scores
        """
        results = self.indexer.search(query, top_k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"],
                "score": round(score, 4)
            })
        
        return formatted_results
