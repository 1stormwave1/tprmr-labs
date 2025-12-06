from typing import Optional
from pydantic import BaseModel, Field

class ResourceBase(BaseModel):
    name: str
    amount: int = Field(..., ge=0)
    player_id: int

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = Field(None, ge=0)

class ResourceResponse(ResourceBase):
    id: int

    class Config:
        from_attributes = True
