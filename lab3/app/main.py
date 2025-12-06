from fastapi import FastAPI
from app.routers import players, resources, matches

app = FastAPI(
    title="Game API",
    description="API для управління гравцями, ресурсами та матчами",
    version="1.0.0"
)

# Підключення роутерів
app.include_router(players.router)
app.include_router(resources.router)
app.include_router(matches.router)

# Кореневий маршрут
@app.get("/")
async def root():
    return {"message": "Game API"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
