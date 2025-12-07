
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import PlayerEntity, ResourceEntity, MatchEntity

class IPlayerRepository(ABC):

    @abstractmethod
    async def create(self, player: PlayerEntity) -> PlayerEntity:
        pass

    @abstractmethod
    async def get_by_id(self, player_id: int) -> Optional[PlayerEntity]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[PlayerEntity]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[PlayerEntity]:
        pass

    @abstractmethod
    async def update(self, player: PlayerEntity) -> PlayerEntity:
        pass

    @abstractmethod
    async def delete(self, player_id: int) -> None:
        pass


class IResourceRepository(ABC):

    @abstractmethod
    async def create(self, resource: ResourceEntity) -> ResourceEntity:
        pass

    @abstractmethod
    async def get_by_id(self, resource_id: int) -> Optional[ResourceEntity]:
        pass

    @abstractmethod
    async def get_by_player(self, player_id: int) -> List[ResourceEntity]:
        pass

    @abstractmethod
    async def update(self, resource: ResourceEntity) -> ResourceEntity:
        pass

    @abstractmethod
    async def delete(self, resource_id: int) -> None:
        pass



class IMatchRepository(ABC):

    @abstractmethod
    async def create(self, match: MatchEntity) -> MatchEntity:
        pass

    @abstractmethod
    async def get_by_id(self, match_id: int) -> Optional[MatchEntity]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[MatchEntity]:
        pass

    @abstractmethod
    async def update(self, match: MatchEntity) -> MatchEntity:
        pass

    @abstractmethod
    async def delete(self, match_id: int) -> None:
        pass
