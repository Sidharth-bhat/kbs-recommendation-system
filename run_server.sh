#!/bin/bash

echo "========================================"
echo "Knowledge Base Recommendation System"
echo "========================================"
echo ""
echo "Starting FastAPI server..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
