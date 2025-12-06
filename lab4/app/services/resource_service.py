from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException, status

from app.models import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate

class ResourceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_resource(self, resource_data: ResourceCreate) -> Resource:
        new_resource = Resource(**resource_data.model_dump())
        self.session.add(new_resource)
        await self.session.commit()
        await self.session.refresh(new_resource)
        return new_resource

    async def get_resource(self, resource_id: int) -> Resource:
        result = await self.session.execute(
            select(Resource).where(Resource.id == resource_id)
        )
        resource = result.scalar_one_or_none()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ресурс з ID {resource_id} не знайдено"
            )
        return resource

    async def get_all_resources(self, skip: int = 0, limit: int = 100, player_id: int | None = None) -> List[Resource]:
        result = await self.session.execute(
            select(Resource).offset(skip).limit(limit)
        )
        resources = list(result.scalars().all())
        if player_id is not None:
            resources = [r for r in resources if r.player_id == player_id]
        return resources

    async def update_resource(self, resource_id: int, resource_data: ResourceUpdate) -> Resource:
        resource = await self.get_resource(resource_id)
        update_data = resource_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(resource, field, value)

        await self.session.commit()
        await self.session.refresh(resource)
        return resource

    async def delete_resource(self, resource_id: int) -> None:
        resource = await self.get_resource(resource_id)
        await self.session.delete(resource)
        await self.session.commit()
