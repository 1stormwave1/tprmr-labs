from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import players, resources, matches
from app.infrastructure.database.models import PlayerModel, ResourceModel, MatchModel
from app.database.session import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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

