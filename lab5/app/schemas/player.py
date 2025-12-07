from typing import Optional
from pydantic import BaseModel, Field

class PlayerBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    level: int = Field(..., ge=1, le=100)
    rating: int = Field(..., ge=0)

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    level: Optional[int] = Field(None, ge=1, le=100)
    rating: Optional[int] = Field(None, ge=0)

class PlayerResponse(PlayerBase):
    id: int

    class Config:
        from_attributes = True
