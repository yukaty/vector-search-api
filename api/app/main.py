from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import openai


from . import models, schemas
from .database import get_db, engine


app = FastAPI(title="Vector Search API")
client = openai.OpenAI()


def get_embedding(text: str) -> List[float]:
    """Generate embedding using OpenAI API"""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


@app.post("/search/", response_model=List[schemas.ItemResponse])
async def search_items(query: schemas.SearchQuery, db: Session = Depends(get_db)):
    """Search for similar items using vector similarity"""
    try:
        # Generate embedding for search query
        query_embedding = get_embedding(query.query)

        # Perform vector similarity search
        results = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    item_metadata,
                    embedding <=> cast(:embedding as vector) as similarity
                FROM items
                ORDER BY embedding <=> cast(:embedding as vector)
                LIMIT :limit
            """),
            {
                "embedding": query_embedding,
                "limit": query.limit
            }
        )

        return [
            schemas.ItemResponse(
                id=row.id,
                name=row.name,
                item_metadata=row.item_metadata,
                similarity=row.similarity,
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
