from typing import List
from fastapi import HTTPException, status

from app.domain.repositories import IResourceRepository
from app.domain.entities import ResourceEntity
from app.schemas.resource import ResourceCreate, ResourceUpdate


class ResourceService:
    def __init__(self, repository: IResourceRepository):
        self.repository = repository

    async def create_resource(self, data: ResourceCreate) -> ResourceEntity:
        resource = ResourceEntity(
            id=None,
            player_id=data.player_id,
            name=data.name,
            amount=data.amount
        )
        return await self.repository.create(resource)

    async def get_resource(self, resource_id: int) -> ResourceEntity:
        resource = await self.repository.get_by_id(resource_id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ресурс з ID {resource_id} не знайдено"
            )
        return resource

    async def get_all_resources(self, skip: int = 0, limit: int = 100) -> List[ResourceEntity]:
        return await self.repository.get_all(skip, limit)

    async def update_resource(self, resource_id: int, data: ResourceUpdate) -> ResourceEntity:
        resource = await self.get_resource(resource_id)

        if data.name is not None:
            resource.name = data.name

        if data.amount is not None:
            resource.amount = data.amount

        return await self.repository.update(resource)

    async def delete_resource(self, resource_id: int) -> None:
        await self.get_resource(resource_id)
        await self.repository.delete(resource_id)
