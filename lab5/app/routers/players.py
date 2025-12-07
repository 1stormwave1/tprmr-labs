
from fastapi import APIRouter, Depends
from typing import List
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerResponse
from app.core.dependencies import get_player_service

router = APIRouter()

@router.post("/", response_model=PlayerResponse, status_code=201)
async def create_player(player: PlayerCreate, service=Depends(get_player_service)):
    return await service.create_player(player)

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: int, service=Depends(get_player_service)):
    return await service.get_player(player_id)

@router.get("/", response_model=List[PlayerResponse])
async def get_all_players(service=Depends(get_player_service)):
    return await service.get_all_players()

@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(player_id: int, player: PlayerUpdate, service=Depends(get_player_service)):
    return await service.update_player(player_id, player)

@router.delete("/{player_id}", status_code=204)
async def delete_player(player_id: int, service=Depends(get_player_service)):
    await service.delete_player(player_id)
    return {}
