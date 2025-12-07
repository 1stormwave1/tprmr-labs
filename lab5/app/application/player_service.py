from typing import List
from fastapi import HTTPException, status

from app.domain.repositories import IPlayerRepository
from app.domain.entities import PlayerEntity
from app.schemas.player import PlayerCreate, PlayerUpdate


class PlayerService:
    def __init__(self, repository: IPlayerRepository):
        self.repository = repository

    async def create_player(self, data: PlayerCreate) -> PlayerEntity:
        existing = await self.repository.get_by_username(data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Гравець з username '{data.username}' вже існує"
            )

        player = PlayerEntity(
            id=None,
            username=data.username,
            level=data.level,
            rating=data.rating
        )

        return await self.repository.create(player)

    async def get_player(self, player_id: int) -> PlayerEntity:
        player = await self.repository.get_by_id(player_id)
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Гравця з ID {player_id} не знайдено"
            )
        return player

    async def get_all_players(self, skip: int = 0, limit: int = 100) -> List[PlayerEntity]:
        return await self.repository.get_all(skip, limit)

    async def update_player(self, player_id: int, data: PlayerUpdate) -> PlayerEntity:
        player = await self.get_player(player_id)

        if data.username is not None:
            existing = await self.repository.get_by_username(data.username)
            if existing and existing.id != player_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Гравець з username '{data.username}' вже існує"
                )
            player.username = data.username

        if data.level is not None:
            player.level = data.level

        if data.rating is not None:
            player.rating = data.rating

        return await self.repository.update(player)

    async def delete_player(self, player_id: int) -> None:
        await self.get_player(player_id)
        await self.repository.delete(player_id)
