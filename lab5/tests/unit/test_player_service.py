import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException

from app.application.player_service import PlayerService
from app.domain.entities import PlayerEntity
from app.schemas.player import PlayerCreate, PlayerUpdate


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def player_service(mock_session):
    return PlayerService(mock_session)


@pytest.fixture
def sample_player():
    return PlayerEntity(
        id=1,
        username="TestPlayer",
        level=5,
        rating=120
    )



@pytest.mark.asyncio
async def test_create_player_success(player_service, mock_session):
    mock_session.get_by_username.return_value = None

    player_data = PlayerCreate(
        username="NewPlayer",
        level=1,
        rating=0
    )


    mock_session.create.return_value = PlayerEntity(
        id=1,
        username="NewPlayer",
        level=1,
        rating=0
    )

    result = await player_service.create_player(player_data)

    assert isinstance(result, PlayerEntity)
    assert result.username == "NewPlayer"
    mock_session.create.assert_called_once()



@pytest.mark.asyncio
async def test_get_player_success(player_service, mock_session, sample_player):
    mock_session.get_by_id.return_value = sample_player

    result = await player_service.get_player(1)

    assert result.id == 1
    assert result.username == "TestPlayer"
    mock_session.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_player_not_found(player_service, mock_session):
    mock_session.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await player_service.get_player(99)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_player_success(player_service, mock_session, sample_player):

    mock_session.get_by_id.return_value = sample_player
    mock_session.update.return_value = sample_player

    update_data = PlayerUpdate(level=10)

    result = await player_service.update_player(1, update_data)

    assert result.level == 10
    mock_session.update.assert_called_once()


@pytest.mark.asyncio
async def test_delete_player_success(player_service, mock_session, sample_player):

    mock_session.get_by_id.return_value = sample_player

    await player_service.delete_player(1)

    mock_session.delete.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_delete_player_not_found(player_service, mock_session):
    mock_session.get_by_id.return_value = None

    with pytest.raises(HTTPException):
        await player_service.delete_player(123)