from typing import List
from fastapi import APIRouter, Depends
from app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate
from app.core.dependencies import get_resource_service
from app.services.resource_service import ResourceService

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/", response_model=ResourceResponse)
async def create_resource(
    resource_data: ResourceCreate,
    service: ResourceService = Depends(get_resource_service)
):
    return await service.create_resource(resource_data)

@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    skip: int = 0,
    limit: int = 100,
    player_id: int | None = None,
    service: ResourceService = Depends(get_resource_service)
):
    return await service.get_resources(skip=skip, limit=limit, player_id=player_id)

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    service: ResourceService = Depends(get_resource_service)
):
    return await service.get_resource(resource_id)

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    service: ResourceService = Depends(get_resource_service)
):
    return await service.update_resource(resource_id, resource_data)

@router.delete("/{resource_id}", status_code=204)
async def delete_resource(
    resource_id: int,
    service: ResourceService = Depends(get_resource_service)
):
    await service.delete_resource(resource_id)
