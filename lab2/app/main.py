from fastapi import FastAPI, HTTPException, status, Query
from typing import List
from app.schemas import Player, PlayerCreate, PlayerUpdate
from app.schemas import Resource, ResourceCreate, ResourceUpdate
from app.schemas import Match, MatchCreate, MatchUpdate
from app.models import players_db, resources_db, matches_db

app = FastAPI(
    title="Multiplayer Client API",
    description="API для управління гравцями, ресурсами та матчами",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Ласкаво просимо до Multiplayer Client API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.post("/players/", response_model=Player, status_code=status.HTTP_201_CREATED, tags=["Players"])
async def create_player(player: PlayerCreate):
    new_player = players_db.create(
        username=player.username,
        level=player.level,
        rating=player.rating
    )
    return new_player

@app.get("/players/", response_model=list[Player], tags=["Players"])
async def get_players(
    skip: int = Query(default=0, ge=0, description="Кількість гравців для пропуску"),
    limit: int = Query(default=50, ge=1, le=100, description="Максимальна кількість гравців у відповіді")
):
    return players_db.get_all(skip=skip, limit=limit)

@app.get("/players/{player_id}", response_model=Player, tags=["Players"])
async def get_player(player_id: int):
    player = players_db.get(player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Гравець з ID {player_id} не знайдено")
    return player

@app.put("/players/{player_id}", response_model=Player, tags=["Players"])
async def update_player(player_id: int, player_update: PlayerUpdate):
    player = players_db.update(
        player_id,
        username=player_update.username,
        level=player_update.level,
        rating=player_update.rating
    )
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Гравець з ID {player_id} не знайдено")
    return player

@app.delete("/players/{player_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Players"])
async def delete_player(player_id: int):
    success = players_db.delete(player_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Гравець з ID {player_id} не знайдено")
    return None


@app.post("/resources/", response_model=Resource, status_code=status.HTTP_201_CREATED, tags=["Resources"])
async def create_resource(resource: ResourceCreate):
    new_resource = resources_db.create(
        name=resource.name,
        amount=resource.amount,
        player_id=resource.player_id
    )
    return new_resource

@app.get("/resources/", response_model=list[Resource], tags=["Resources"])
async def get_resources(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    player_id: int | None = Query(default=None, description="Фільтр за ID гравця")
):
    return resources_db.get_all(skip=skip, limit=limit, player_id=player_id)

@app.get("/resources/{resource_id}", response_model=Resource, tags=["Resources"])
async def get_resource(resource_id: int):
    resource = resources_db.get(resource_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ресурс з ID {resource_id} не знайдено")
    return resource

@app.put("/resources/{resource_id}", response_model=Resource, tags=["Resources"])
async def update_resource(resource_id: int, resource_update: ResourceUpdate):
    resource = resources_db.update(
        resource_id,
        name=resource_update.name,
        amount=resource_update.amount
    )
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ресурс з ID {resource_id} не знайдено")
    return resource

@app.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Resources"])
async def delete_resource(resource_id: int):
    success = resources_db.delete(resource_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ресурс з ID {resource_id} не знайдено")
    return None


@app.post("/matches/", response_model=Match, status_code=status.HTTP_201_CREATED, tags=["Matches"])
async def create_match(match: MatchCreate):
    new_match = matches_db.create(
        status=match.status,
        players=match.players,
        duration=match.duration
    )
    return new_match

@app.get("/matches/", response_model=list[Match], tags=["Matches"])
async def get_matches(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    status: str | None = Query(default=None, description="Фільтр за статусом матчу")
):
    return matches_db.get_all(skip=skip, limit=limit, status=status)

@app.get("/matches/{match_id}", response_model=Match, tags=["Matches"])
async def get_match(match_id: int):
    match = matches_db.get(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Матч з ID {match_id} не знайдено")
    return match

@app.get("/matches/stats/summary", tags=["Statistics"])
async def get_match_statistics():
    all_matches = matches_db.get_all()
    finished = [m for m in all_matches if m.status == "finished"]
    active = [m for m in all_matches if m.status == "active"]

    return {
        "total": len(all_matches),
        "active": len(active),
        "finished": len(finished),
        "average_duration": (
            sum(m.duration for m in all_matches) / len(all_matches)
            if all_matches else 0
        ),
        "completion_rate": (
            len(finished) / len(all_matches) * 100
            if all_matches else 0
        )
    }

@app.put("/matches/{match_id}", response_model=Match, tags=["Matches"])
async def update_match(match_id: int, match_update: MatchUpdate):
    match = matches_db.update(
        match_id,
        status=match_update.status,
        duration=match_update.duration
    )
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Матч з ID {match_id} не знайдено")
    return match

@app.delete("/matches/{match_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Matches"])
async def delete_match(match_id: int):
    success = matches_db.delete(match_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Матч з ID {match_id} не знайдено")
    return None