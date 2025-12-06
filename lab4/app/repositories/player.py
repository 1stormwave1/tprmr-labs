from typing import Optional
from sqlalchemy import select
from app.models.player import Player
from app.repositories.base import BaseRepository

class PlayerRepository(BaseRepository[Player]):
    async def get_by_username(self, username: str) -> Optional[Player]:
        result = await self.db.execute(
            select(Player).where(Player.username == username)
        )
        return result.scalar_one_or_none()
