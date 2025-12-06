from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.player import Player
from app.repositories.player import PlayerRepository
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_data: PlayerCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = PlayerRepository(Player, db)

    existing = await repo.get_by_username(player_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Гравець з таким ім'ям вже існує"
        )

    player = Player(**player_data.model_dump())
    return await repo.create(player)

@router.get("/", response_model=List[PlayerResponse])
async def get_players(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    repo = PlayerRepository(Player, db)
    return await repo.get_all(skip=skip, limit=limit)

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = PlayerRepository(Player, db)
    player = await repo.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Гравця не знайдено"
        )
    return player

@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = PlayerRepository(Player, db)
    player = await repo.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Гравця не знайдено"
        )

    update_data = player_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(player, field, value)

    return await repo.update(player)

@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(
    player_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = PlayerRepository(Player, db)
    deleted = await repo.delete(player_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Гравця не знайдено"
        )
