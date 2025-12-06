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


from pydantic import BaseModel
from typing import List

class PlayerOut(BaseModel):
    id: int
    username: str
    level: int
    rating: int

    class Config:
        orm_mode = True

class MatchOut(BaseModel):
    id: int
    status: str
    duration: int
    players: List[PlayerOut]

    class Config:
        orm_mode = True
