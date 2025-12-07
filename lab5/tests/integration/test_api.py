import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.main import app
from app.database.session import Base, get_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def test_session_maker(test_engine):
    return async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
async def override_get_session(test_session_maker):
    async def _get_session():
        async with test_session_maker() as session:
            yield session
    app.dependency_overrides[get_session] = _get_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
async def client(override_get_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_player(client):
    response = await client.post(
        "/players/",
        json={"username": "TestPlayer", "level": 1, "rating": 100}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "TestPlayer"
    assert data["level"] == 1

@pytest.mark.asyncio
async def test_get_player(client):
    create_response = await client.post(
        "/players/",
        json={"username": "PlayerToGet", "level": 5, "rating": 200}
    )
    player_id = create_response.json()["id"]

    response = await client.get(f"/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == player_id
    assert data["username"] == "PlayerToGet"


@pytest.mark.asyncio
async def test_create_resource(client):

    create_player = await client.post(
        "/players/",
        json={"username": "ResPlayer", "level": 1, "rating": 50}
    )
    player_id = create_player.json()["id"]

    response = await client.post(
        "/resources/",
        json={"player_id": player_id, "name": "gold", "amount": 100}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["player_id"] == player_id
    assert data["name"] == "gold"
    assert data["amount"] == 100

@pytest.mark.asyncio
async def test_update_resource(client):

    create_player = await client.post(
        "/players/",
        json={"username": "UpdResPlayer", "level": 1, "rating": 50}
    )
    player_id = create_player.json()["id"]

    create_res = await client.post(
        "/resources/",
        json={"player_id": player_id, "name": "wood", "amount": 50}
    )
    res_id = create_res.json()["id"]

    response = await client.put(
        f"/resources/{res_id}",
        json={"name": "stone", "amount": 200}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "stone"
    assert data["amount"] == 200


@pytest.mark.asyncio
async def test_create_match(client):

    create_player = await client.post(
        "/players/",
        json={"username": "MatchPlayer", "level": 1, "rating": 50}
    )
    player_id = create_player.json()["id"]

    response = await client.post(
        "/matches/",
        json={"player_id": player_id, "status": "win", "duration": 30}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["player_id"] == player_id
    assert data["status"] == "win"
    assert data["duration"] == 30

@pytest.mark.asyncio
async def test_update_match(client):

    create_player = await client.post(
        "/players/",
        json={"username": "UpdMatchPlayer", "level": 1, "rating": 50}
    )
    player_id = create_player.json()["id"]

    create_match = await client.post(
        "/matches/",
        json={"player_id": player_id, "status": "lose", "duration": 15}
    )
    match_id = create_match.json()["id"]

    response = await client.put(
        f"/matches/{match_id}",
        json={"status": "win", "duration": 45}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "win"
    assert data["duration"] == 45
