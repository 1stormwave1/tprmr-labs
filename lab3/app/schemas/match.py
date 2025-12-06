from typing import Optional, List
from pydantic import BaseModel, Field

class MatchBase(BaseModel):
    status: str
    duration: Optional[int] = Field(None, ge=0)

class MatchCreate(MatchBase):
    players: List[int]  # ID гравців

class MatchUpdate(BaseModel):
    status: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)

class MatchResponse(MatchBase):
    id: int
    players: List[int]

    class Config:
        from_attributes = True
