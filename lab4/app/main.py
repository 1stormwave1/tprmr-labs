from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import players, resources, matches
from app.database.session import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Створення всіх таблиць при старті додатку
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закриття з'єднання при завершенні роботи додатку
    await engine.dispose()

app = FastAPI(
    title="Game API",
    description="API для управління гравцями, ресурсами та матчами з service layer",
    version="1.0.0",
    lifespan=lifespan
)

# Підключення роутерів
app.include_router(players.router, prefix="/routers/players")
app.include_router(resources.router, prefix="/routers/resources")
app.include_router(matches.router, prefix="/routers/matches")

@app.get("/")
async def root():
    return {"message": "Game API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
