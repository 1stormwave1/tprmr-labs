import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.application.match_service import MatchService
from app.domain.entities import MatchEntity
from app.schemas.match import MatchCreate, MatchUpdate

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def match_service(mock_repository):
    return MatchService(mock_repository)

@pytest.fixture
def sample_match():
    return MatchEntity(
        id=1,
        player_id=1,
        status="win",
        duration=30
    )


@pytest.mark.asyncio
async def test_create_match_success(match_service, mock_repository):
    mock_repository.create.return_value = MatchEntity(
        id=1, player_id=1, status="lose", duration=15
    )

    data = MatchCreate(player_id=1, status="lose", duration=15)
    match = await match_service.create_match(data)

    assert match.status == "lose"
    assert match.duration == 15
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_match_success(match_service, mock_repository, sample_match):
    mock_repository.get_by_id.return_value = sample_match

    result = await match_service.get_match(1)

    assert result.id == 1
    assert result.status == "win"
    mock_repository.get_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_match_not_found(match_service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await match_service.get_match(999)

    assert exc_info.value.status_code == 404



@pytest.mark.asyncio
async def test_update_match_success(match_service, mock_repository, sample_match):
    mock_repository.get_by_id.return_value = sample_match
    mock_repository.update.return_value = sample_match

    update_data = MatchUpdate(status="lose", duration=45)
    result = await match_service.update_match(1, update_data)

    assert result.status == "lose"
    assert result.duration == 45
    mock_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_delete_match_success(match_service, mock_repository, sample_match):
    mock_repository.get_by_id.return_value = sample_match

    await match_service.delete_match(1)
    mock_repository.delete.assert_called_once_with(1)
