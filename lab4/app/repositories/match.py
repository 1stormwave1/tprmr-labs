from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.match import Match
from app.repositories.base import BaseRepository

class MatchRepository(BaseRepository[Match]):
    async def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Match]:
        result = await self.db.execute(
            select(Match)
            .where(Match.status == status)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_player(self, player_id: int, skip: int = 0, limit: int = 100) -> List[Match]:
        result = await self.db.execute(
            select(Match)
            .join(Match.players)
            .where(Match.players.any(id=player_id))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
