from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.resource import Resource
from app.repositories.base import BaseRepository

class ResourceRepository(BaseRepository[Resource]):
    async def get_by_name(self, name: str) -> Optional[Resource]:
        result = await self.db.execute(
            select(Resource).where(Resource.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_player(self, player_id: int, skip: int = 0, limit: int = 100) -> List[Resource]:
        result = await self.db.execute(
            select(Resource)
            .where(Resource.player_id == player_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
