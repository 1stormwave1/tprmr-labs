from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import players, resources, matches
from app.infrastructure.database.models import PlayerModel, ResourceModel, MatchModel
from app.database.session import engine, Base
from sqlalchemy.exc import OperationalError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Чекаємо, поки база стане доступною
    for _ in range(10):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("Таблиці створені")
            break
        except OperationalError:
            print("База недоступна, чекаємо 2 секунди...")
            await asyncio.sleep(2)
    yield
    await engine.dispose()


app = FastAPI(
    title="Game API",
    description="API для управління гравцями, ресурсами та матчами",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(resources.router, prefix="/resources", tags=["resources"])
app.include_router(matches.router, prefix="/matches", tags=["matches"])

@app.get("/")
async def root():
    return {"message": "Game API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

