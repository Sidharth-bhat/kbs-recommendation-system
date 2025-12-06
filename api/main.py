"""
FastAPI application for Knowledge Base Recommendation System.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from contextlib import asynccontextmanager
from src.search import SearchService
from src.config import TOP_K


# Global search service instance
search_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize search service on startup."""
    global search_service
    search_service = SearchService()
    search_service.initialize()
    yield


app = FastAPI(
    title="Knowledge Base Recommendation System",
    description="Semantic search API for internal knowledge base documents",
    version="1.0.0",
    lifespan=lifespan
)


class SearchRequest(BaseModel):
    """Request model for search endpoint."""
    query: str = Field(..., description="Search query text", min_length=1)
    top_k: int = Field(default=TOP_K, description="Number of results to return", ge=1, le=20)


class DocumentResponse(BaseModel):
    """Response model for a single document."""
    id: str
    title: str
    content: str
    score: float


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    query: str
    results: List[DocumentResponse]
    count: int


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {"status": "healthy", "service": "Knowledge Base Recommendation System"}


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    Search for relevant documents based on query.
    
    Args:
        request: Search request containing query and top_k
        
    Returns:
        Search results with relevant documents and scores
    """
    try:
        results = search_service.search(request.query, request.top_k)
        
        return SearchResponse(
            query=request.query,
            results=results,
            count=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "service": "Knowledge Base Recommendation System",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "search": "/search (POST)"
        }
    }
