from typing import List
from fastapi import HTTPException, status

from app.domain.repositories import IMatchRepository
from app.domain.entities import MatchEntity
from app.schemas.match import MatchCreate, MatchUpdate


class MatchService:
    def __init__(self, repository: IMatchRepository):
        self.repository = repository

    async def create_match(self, data: MatchCreate) -> MatchEntity:
        match = MatchEntity(
            id=None,
            player_id=data.player_id,
            status=data.status,
            duration=data.duration
        )
        return await self.repository.create(match)

    async def get_match(self, match_id: int) -> MatchEntity:
        match = await self.repository.get_by_id(match_id)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Матч з ID {match_id} не знайдено"
            )
        return match

    async def get_all_matches(self, skip: int = 0, limit: int = 100) -> List[MatchEntity]:
        return await self.repository.get_all(skip, limit)

    async def update_match(self, match_id: int, data: MatchUpdate) -> MatchEntity:
        match = await self.get_match(match_id)

        if data.status is not None:
            match.status = data.status

        if data.duration is not None:
            match.duration = data.duration

        return await self.repository.update(match)

    async def delete_match(self, match_id: int) -> None:
        await self.get_match(match_id)
        await self.repository.delete(match_id)
