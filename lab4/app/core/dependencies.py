from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.services.player_service import PlayerService
from app.services.resource_service import ResourceService
from app.services.match_service import MatchService

async def get_player_service(
    session: AsyncSession = Depends(get_session)
) -> PlayerService:
    return PlayerService(session)

async def get_resource_service(
    session: AsyncSession = Depends(get_session)
) -> ResourceService:
    return ResourceService(session)

async def get_match_service(
    session: AsyncSession = Depends(get_session)
) -> MatchService:
    return MatchService(session)
