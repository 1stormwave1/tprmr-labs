import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.application.resource_service import ResourceService
from app.domain.entities import ResourceEntity
from app.schemas.resource import ResourceCreate, ResourceUpdate

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def resource_service(mock_repository):
    return ResourceService(mock_repository)

@pytest.fixture
def sample_resource():
    return ResourceEntity(
        id=1,
        player_id=1,
        name="gold",
        amount=100
    )


@pytest.mark.asyncio
async def test_create_resource_success(resource_service, mock_repository):
    mock_repository.create.return_value = ResourceEntity(
        id=1, player_id=1, name="wood", amount=50
    )

    data = ResourceCreate(player_id=1, name="wood", amount=50)
    result = await resource_service.create_resource(data)

    assert result.name == "wood"
    assert result.amount == 50
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_resource_success(resource_service, mock_repository, sample_resource):
    mock_repository.get_by_id.return_value = sample_resource

    result = await resource_service.get_resource(1)

    assert result.id == 1
    assert result.name == "gold"
    mock_repository.get_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_resource_not_found(resource_service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await resource_service.get_resource(999)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_resource_success(resource_service, mock_repository, sample_resource):
    mock_repository.get_by_id.return_value = sample_resource
    mock_repository.update.return_value = sample_resource

    update_data = ResourceUpdate(name="stone", amount=200)
    result = await resource_service.update_resource(1, update_data)

    assert result.name == "stone"
    assert result.amount == 200
    mock_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_delete_resource_success(resource_service, mock_repository, sample_resource):
    mock_repository.get_by_id.return_value = sample_resource

    await resource_service.delete_resource(1)
    mock_repository.delete.assert_called_once_with(1)
