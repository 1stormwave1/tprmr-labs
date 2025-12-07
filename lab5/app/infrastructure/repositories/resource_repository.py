from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.domain.repositories import IResourceRepository
from app.domain.entities import ResourceEntity
from app.infrastructure.database.models import ResourceModel


class ResourceRepository(IResourceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, resource: ResourceEntity) -> ResourceEntity:
        db_resource = ResourceModel(
            player_id=resource.player_id,
            name=resource.name,
            amount=resource.amount
        )
        self.session.add(db_resource)
        await self.session.commit()
        await self.session.refresh(db_resource)
        return self._to_entity(db_resource)

    async def get_by_id(self, resource_id: int) -> Optional[ResourceEntity]:
        result = await self.session.execute(
            select(ResourceModel).where(ResourceModel.id == resource_id)
        )
        db_resource = result.scalar_one_or_none()
        return self._to_entity(db_resource) if db_resource else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ResourceEntity]:
        result = await self.session.execute(
            select(ResourceModel).offset(skip).limit(limit)
        )
        db_resources = result.scalars().all()
        return [self._to_entity(r) for r in db_resources]

    async def update(self, resource: ResourceEntity) -> ResourceEntity:
        result = await self.session.execute(
            select(ResourceModel).where(ResourceModel.id == resource.id)
        )
        db_resource = result.scalar_one_or_none()
        if not db_resource:
            raise ValueError(f"Resource з ID {resource.id} не знайдено")

        db_resource.name = resource.name
        db_resource.amount = resource.amount

        await self.session.commit()
        await self.session.refresh(db_resource)
        return self._to_entity(db_resource)

    async def delete(self, resource_id: int) -> None:
        result = await self.session.execute(
            select(ResourceModel).where(ResourceModel.id == resource_id)
        )
        db_resource = result.scalar_one_or_none()
        if db_resource:
            await self.session.delete(db_resource)
            await self.session.commit()
    
    async def get_by_player(self, player_id: int) -> List[ResourceEntity]:
        result = await self.session.execute(
            select(ResourceModel).where(ResourceModel.player_id == player_id)
        )
        db_resources = result.scalars().all()
        return [self._to_entity(r) for r in db_resources]

    @staticmethod
    def _to_entity(model: ResourceModel) -> ResourceEntity:
        return ResourceEntity(
            id=model.id,
            player_id=model.player_id,
            name=model.name,
            amount=model.amount
        )
