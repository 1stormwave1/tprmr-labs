from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.domain.repositories import IPlayerRepository
from app.domain.entities import PlayerEntity
from app.infrastructure.database.models import PlayerModel


class PlayerRepository(IPlayerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, player: PlayerEntity) -> PlayerEntity:
        db_player = PlayerModel(
            username=player.username,
            level=player.level,
            rating=player.rating
        )
        self.session.add(db_player)
        await self.session.commit()
        await self.session.refresh(db_player)
        return self._to_entity(db_player)

    async def get_by_id(self, player_id: int) -> Optional[PlayerEntity]:
        result = await self.session.execute(
            select(PlayerModel).where(PlayerModel.id == player_id)
        )
        db_player = result.scalar_one_or_none()
        return self._to_entity(db_player) if db_player else None

    async def get_by_username(self, username: str) -> Optional[PlayerEntity]:
        result = await self.session.execute(
            select(PlayerModel).where(PlayerModel.username == username)
        )
        db_player = result.scalar_one_or_none()
        return self._to_entity(db_player) if db_player else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[PlayerEntity]:
        result = await self.session.execute(
            select(PlayerModel).offset(skip).limit(limit)
        )
        db_players = result.scalars().all()
        return [self._to_entity(p) for p in db_players]

    async def update(self, player: PlayerEntity) -> PlayerEntity:
        result = await self.session.execute(
            select(PlayerModel).where(PlayerModel.id == player.id)
        )
        db_player = result.scalar_one_or_none()
        if not db_player:
            raise ValueError(f"Player з ID {player.id} не знайдено")

        db_player.username = player.username
        db_player.level = player.level
        db_player.rating = player.rating

        await self.session.commit()
        await self.session.refresh(db_player)
        return self._to_entity(db_player)

    async def delete(self, player_id: int) -> None:
        result = await self.session.execute(
            select(PlayerModel).where(PlayerModel.id == player_id)
        )
        db_player = result.scalar_one_or_none()
        if db_player:
            await self.session.delete(db_player)
            await self.session.commit()

    @staticmethod
    def _to_entity(model: PlayerModel) -> PlayerEntity:
        return PlayerEntity(
            id=model.id,
            username=model.username,
            level=model.level,
            rating=model.rating,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
