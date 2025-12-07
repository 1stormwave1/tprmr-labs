from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.domain.repositories import IMatchRepository
from app.domain.entities import MatchEntity
from app.infrastructure.database.models import MatchModel


class MatchRepository(IMatchRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, match: MatchEntity) -> MatchEntity:
        db_match = MatchModel(
            player_id=match.player_id,
            status=match.status,
            duration=match.duration
        )
        self.session.add(db_match)
        await self.session.commit()
        await self.session.refresh(db_match)
        return self._to_entity(db_match)

    async def get_by_id(self, match_id: int) -> Optional[MatchEntity]:
        status = await self.session.execute(
            select(MatchModel).where(MatchModel.id == match_id)
        )
        db_match = status.scalar_one_or_none()
        return self._to_entity(db_match) if db_match else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[MatchEntity]:
        status = await self.session.execute(
            select(MatchModel).offset(skip).limit(limit)
        )
        db_matches = status.scalars().all()
        return [self._to_entity(m) for m in db_matches]

    async def update(self, match: MatchEntity) -> MatchEntity:
        status = await self.session.execute(
            select(MatchModel).where(MatchModel.id == match.id)
        )
        db_match = status.scalar_one_or_none()
        if not db_match:
            raise ValueError(f"Match з ID {match.id} не знайдено")

        db_match.status = match.status
        db_match.duration = match.duration

        await self.session.commit()
        await self.session.refresh(db_match)
        return self._to_entity(db_match)

    async def delete(self, match_id: int) -> None:
        status = await self.session.execute(
            select(MatchModel).where(MatchModel.id == match_id)
        )
        db_match = status.scalar_one_or_none()
        if db_match:
            await self.session.delete(db_match)
            await self.session.commit()

    @staticmethod
    def _to_entity(model: MatchModel) -> MatchEntity:
        return MatchEntity(
            id=model.id,
            player_id=model.player_id,
            status=model.status,
            duration=model.duration,
        )
