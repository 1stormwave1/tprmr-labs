from typing import List
from fastapi import APIRouter, Depends
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate
from app.core.dependencies import get_player_service
from app.services.player_service import PlayerService

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=PlayerResponse)
async def create_player(
    player_data: PlayerCreate,
    service: PlayerService = Depends(get_player_service)
):
    return await service.create_player(player_data)

@router.get("/", response_model=List[PlayerResponse])
async def get_players(
    skip: int = 0,
    limit: int = 100,
    service: PlayerService = Depends(get_player_service)
):
    return await service.get_all_players(skip=skip, limit=limit)

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: int,
    service: PlayerService = Depends(get_player_service)
):
    return await service.get_player(player_id)

@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    service: PlayerService = Depends(get_player_service)
):
    return await service.update_player(player_id, player_data)

@router.delete("/{player_id}", status_code=204)
async def delete_player(
    player_id: int,
    service: PlayerService = Depends(get_player_service)
):
    await service.delete_player(player_id)
