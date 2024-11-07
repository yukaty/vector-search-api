from pydantic import BaseModel
from typing import List, Optional, Dict


# Pydantic models: Define how data enters and leaves your API


class SearchQuery(BaseModel):
    query: str
    limit: int = 3  # Optional limit with default value of 3


class ItemResponse(BaseModel):
    id: int
    name: str
    item_metadata: Dict
    similarity: float

    class Config:
        from_attributes = (
            True  # Allows conversion from SQLAlchemy model to Pydantic model
        )
