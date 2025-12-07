from fastapi import APIRouter, Depends
from typing import List
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse
from app.core.dependencies import get_match_service

router = APIRouter()

@router.post("/", response_model=MatchResponse, status_code=201)
async def create_match(data: MatchCreate, service=Depends(get_match_service)):
    return await service.create_match(data)

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: int, service=Depends(get_match_service)):
    return await service.get_match(match_id)

@router.get("/", response_model=List[MatchResponse])
async def get_all_matches(service=Depends(get_match_service)):
    return await service.get_all_matches()

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(match_id: int, data: MatchUpdate, service=Depends(get_match_service)):
    return await service.update_match(match_id, data)

@router.delete("/{match_id}", status_code=204)
async def delete_match(match_id: int, service=Depends(get_match_service)):
    await service.delete_match(match_id)
    return {}
