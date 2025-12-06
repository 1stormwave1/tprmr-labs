from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException, status

from app.models import Match
from app.schemas.match import MatchCreate, MatchUpdate

from app.models import Player

class MatchService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_match(self, match_data: MatchCreate) -> Match:
        players = [await self.session.get(Player, pid) for pid in match_data.players]

        new_match = Match(
            status=match_data.status,
            duration=match_data.duration,
            players=players
        )

        self.session.add(new_match)
        await self.session.commit()
        await self.session.refresh(new_match)

        # Явно завантажуємо players, щоб не було lazy load поза сесією
        await self.session.refresh(new_match, attribute_names=["players"])

        return new_match

    async def get_match(self, match_id: int) -> Match:
        result = await self.session.execute(
            select(Match).where(Match.id == match_id)
        )
        match = result.scalar_one_or_none()
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Матч з ID {match_id} не знайдено"
            )
        return match

    async def get_all_matches(self, skip: int = 0, limit: int = 100, status: str | None = None) -> List[Match]:
        result = await self.session.execute(
            select(Match).offset(skip).limit(limit)
        )
        matches = list(result.scalars().all())
        if status:
            matches = [m for m in matches if m.status == status]
        return matches

    async def update_match(self, match_id: int, match_data: MatchUpdate) -> Match:
        match = await self.get_match(match_id)
        update_data = match_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(match, field, value)

        await self.session.commit()
        await self.session.refresh(match)
        return match

    async def delete_match(self, match_id: int) -> None:
        match = await self.get_match(match_id)
        await self.session.delete(match)
        await self.session.commit()
