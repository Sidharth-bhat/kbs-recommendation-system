"""
Simple test script to verify the API is working correctly.
Run this after starting the server with: uvicorn api.main:app --reload
"""

import requests
import json


def test_health():
    """Test the health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_search(query: str, top_k: int = 3):
    """Test the search endpoint."""
    print(f"Testing /search endpoint with query: '{query}'...")
    response = requests.post(
        "http://localhost:8000/search",
        json={"query": query, "top_k": top_k}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Query: {data['query']}")
        print(f"Found {data['count']} results:\n")
        
        for i, result in enumerate(data['results'], 1):
            print(f"{i}. {result['title']} (Score: {result['score']})")
            print(f"   ID: {result['id']}")
            print(f"   Content: {result['content'][:100]}...\n")
    else:
        print(f"Error: {response.text}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Knowledge Base Recommendation System - API Test")
    print("=" * 60 + "\n")
    
    # Test health endpoint
    test_health()
    
    # Test search with different queries
    test_queries = [
        "How do I reset my password?",
        "VPN connection issues",
        "New employee setup",
        "backup and recovery"
    ]
    
    for query in test_queries:
        test_search(query, top_k=2)
        print("-" * 60 + "\n")
