from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate, MatchOut
from app.core.dependencies import get_match_service
from app.database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.match_service import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/", response_model=MatchOut)
async def create_match(match_data: MatchCreate, session: AsyncSession = Depends(get_session)):
    service = MatchService(session)
    match = await service.create_match(match_data)
    return match

@router.get("/", response_model=List[MatchResponse])
async def get_matches(
    skip: int = 0,
    limit: int = 100,
    status_filter: str | None = None,
    service: MatchService = Depends(get_match_service)
):
    return await service.get_all_matches(skip=skip, limit=limit, status=status_filter)

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    service: MatchService = Depends(get_match_service)
):
    return await service.get_match(match_id)

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int,
    match_data: MatchUpdate,
    service: MatchService = Depends(get_match_service)
):
    return await service.update_match(match_id, match_data)

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match_id: int,
    service: MatchService = Depends(get_match_service)
):
    await service.delete_match(match_id)
