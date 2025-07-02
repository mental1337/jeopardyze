#!/bin/bash

# Create database tables first
echo "Creating database tables..."
python -m app.core.database --action create_tables

# Run the FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 3001

