from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.match import Match
from app.repositories.match import MatchRepository
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_data: MatchCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = MatchRepository(Match, db)
    match = Match(**match_data.model_dump())
    return await repo.create(match)

@router.get("/", response_model=List[MatchResponse])
async def get_matches(
    skip: int = 0,
    limit: int = 100,
    status_filter: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    repo = MatchRepository(Match, db)
    return await repo.get_by_status(status_filter, skip=skip, limit=limit) if status_filter else await repo.get_all(skip=skip, limit=limit)

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = MatchRepository(Match, db)
    match = await repo.get_by_id(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Матч не знайдено"
        )
    return match

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int,
    match_data: MatchUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = MatchRepository(Match, db)
    match = await repo.get_by_id(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Матч не знайдено"
        )

    update_data = match_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(match, field, value)

    return await repo.update(match)

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = MatchRepository(Match, db)
    deleted = await repo.delete(match_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Матч не знайдено"
        )
