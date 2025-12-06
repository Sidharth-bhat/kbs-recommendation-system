"""
Embedding module using Sentence-BERT for text encoding.
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import MODEL_NAME


class Embedder:
    """Wrapper for Sentence-BERT model to generate text embeddings."""
    
    def __init__(self, model_name: str = MODEL_NAME):
        """
        Initialize the embedder with a pre-trained model.
        
        Args:
            model_name: Name of the Sentence-BERT model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def encode(self, texts: List[str], normalize: bool = True) -> np.ndarray:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            normalize: Whether to L2-normalize embeddings
            
        Returns:
            NumPy array of shape (n_texts, embedding_dim)
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        
        if normalize:
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        return embeddings
    
    def encode_single(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Encode a single text into an embedding.
        
        Args:
            text: Text string to encode
            normalize: Whether to L2-normalize embedding
            
        Returns:
            NumPy array of shape (embedding_dim,)
        """
        return self.encode([text], normalize=normalize)[0]
