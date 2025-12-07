from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session


from app.infrastructure.repositories.player_repository import PlayerRepository
from app.infrastructure.repositories.resource_repository import ResourceRepository
from app.infrastructure.repositories.match_repository import MatchRepository


from app.application.player_service import PlayerService
from app.application.resource_service import ResourceService
from app.application.match_service import MatchService



async def get_player_repository(
    session: AsyncSession = Depends(get_session)
) -> PlayerRepository:
    return PlayerRepository(session)

async def get_player_service(
    repository: PlayerRepository = Depends(get_player_repository)
) -> PlayerService:
    return PlayerService(repository)



async def get_resource_repository(
    session: AsyncSession = Depends(get_session)
) -> ResourceRepository:
    return ResourceRepository(session)

async def get_resource_service(
    repository: ResourceRepository = Depends(get_resource_repository)
) -> ResourceService:
    return ResourceService(repository)


async def get_match_repository(
    session: AsyncSession = Depends(get_session)
) -> MatchRepository:
    return MatchRepository(session)

async def get_match_service(
    repository: MatchRepository = Depends(get_match_repository)
) -> MatchService:
    return MatchService(repository)
