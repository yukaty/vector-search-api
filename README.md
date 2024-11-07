<!-- 🚧 **Work in Progress** 🚧 -->

# Vector Search API

A FastAPI application implementing vector similarity search.

## Overview

This project demonstrates how to build a vector similarity search system using:
- PostgreSQL with pgvector extension for vector operations
- OpenAI Embedding models for text vectorization
- FastAPI for the REST API interface
- Docker for containerization

## Quick Start

1. Create `.env` in the root directory
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

2. Start the services
   ```bash
   docker compose up --build
   ```

## API Endpoints

Visit http://localhost:8000/docs for the Swagger UI.

## Development
- Update database schema: Edit `postgres/schema.sql`
- Modify API: Edit files in `api/app/`
- Add data: Use `scripts/load_data.py`

