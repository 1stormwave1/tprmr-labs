from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException, status

from app.models import Player
from app.schemas.player import PlayerCreate, PlayerUpdate

class PlayerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_player(self, player_data: PlayerCreate) -> Player:
        existing_player = await self._get_by_username(player_data.username)
        if existing_player:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Гравець з username '{player_data.username}' вже існує"
            )

        new_player = Player(**player_data.model_dump())
        self.session.add(new_player)
        await self.session.commit()
        await self.session.refresh(new_player)
        return new_player

    async def get_player(self, player_id: int) -> Player:
        result = await self.session.execute(
            select(Player).where(Player.id == player_id)
        )
        player = result.scalar_one_or_none()
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Гравця з ID {player_id} не знайдено"
            )
        return player

    async def get_all_players(self, skip: int = 0, limit: int = 100) -> List[Player]:
        result = await self.session.execute(
            select(Player).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update_player(self, player_id: int, player_data: PlayerUpdate) -> Player:
        player = await self.get_player(player_id)
        update_data = player_data.model_dump(exclude_unset=True)

        if "username" in update_data:
            existing = await self._get_by_username(update_data["username"])
            if existing and existing.id != player_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Гравець з username '{update_data['username']}' вже існує"
                )

        for field, value in update_data.items():
            setattr(player, field, value)

        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def delete_player(self, player_id: int) -> None:
        player = await self.get_player(player_id)
        await self.session.delete(player)
        await self.session.commit()

    async def _get_by_username(self, username: str) -> Player | None:
        result = await self.session.execute(
            select(Player).where(Player.username == username)
        )
        return result.scalar_one_or_none()
