from fastapi import APIRouter, Depends
from typing import List
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.core.dependencies import get_resource_service

router = APIRouter()

@router.post("/", response_model=ResourceResponse, status_code=201)
async def create_resource(data: ResourceCreate, service=Depends(get_resource_service)):
    return await service.create_resource(data)

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, service=Depends(get_resource_service)):
    return await service.get_resource(resource_id)

@router.get("/", response_model=List[ResourceResponse])
async def get_all_resources(service=Depends(get_resource_service)):
    return await service.get_all_resources()

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, data: ResourceUpdate, service=Depends(get_resource_service)):
    return await service.update_resource(resource_id, data)

@router.delete("/{resource_id}", status_code=204)
async def delete_resource(resource_id: int, service=Depends(get_resource_service)):
    await service.delete_resource(resource_id)
    return {}
