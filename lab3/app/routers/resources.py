from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.resource import Resource
from app.repositories.resource import ResourceRepository
from app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_data: ResourceCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = ResourceRepository(Resource, db)
    resource = Resource(**resource_data.model_dump())
    return await repo.create(resource)

@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    skip: int = 0,
    limit: int = 100,
    player_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    repo = ResourceRepository(Resource, db)
    return await repo.get_by_player(player_id) if player_id else await repo.get_all(skip=skip, limit=limit)

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = ResourceRepository(Resource, db)
    resource = await repo.get_by_id(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ресурс не знайдено"
        )
    return resource

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = ResourceRepository(Resource, db)
    resource = await repo.get_by_id(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ресурс не знайдено"
        )

    update_data = resource_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)

    return await repo.update(resource)

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = ResourceRepository(Resource, db)
    deleted = await repo.delete(resource_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ресурс не знайдено"
        )
