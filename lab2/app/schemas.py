from pydantic import BaseModel, Field
from typing import Optional, List

class PlayerBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="Унікальне ім'я гравця")
    level: int = Field(..., ge=1, le=100, description="Рівень гравця")
    rating: int = Field(..., ge=0, description="Рейтинг гравця у матчах")

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    level: Optional[int] = Field(None, ge=1, le=100)
    rating: Optional[int] = Field(None, ge=0)

class Player(PlayerBase):
    id: int = Field(..., description="Унікальний ID гравця")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "DragonSlayer",
                "level": 12,
                "rating": 1450
            }
        }

class ResourceBase(BaseModel):
    name: str = Field(..., description="Назва ресурсу")
    amount: int = Field(..., ge=0, description="Кількість ресурсу")

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = Field(None, ge=0)

class Resource(ResourceBase):
    id: int = Field(..., description="Унікальний ID ресурсу")
    player_id: int = Field(..., description="ID гравця-власника")


class MatchBase(BaseModel):
    status: str = Field(..., description="Статус матчу: pending/active/finished")
    duration: Optional[int] = Field(None, ge=0, description="Тривалість матчу в секундах")

class MatchCreate(MatchBase):
    players: List[int] = Field(..., description="ID гравців, які беруть участь у матчі")

class MatchUpdate(BaseModel):
    status: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)

class Match(MatchBase):
    id: int
    players: List[int]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 10,
                "status": "finished",
                "duration": 540,
                "players": [1, 2]
            }
        }