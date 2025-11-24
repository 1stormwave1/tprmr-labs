from typing import Dict, List
from app.schemas import Player, Resource, Match

class PlayerDatabase:
    def __init__(self):
        self.players: Dict[int, Player] = {}
        self.current_id: int = 1

    def create(self, username: str, level: int, rating: int) -> Player:
        player = Player(
            id=self.current_id,
            username=username,
            level=level,
            rating=rating
        )
        self.players[self.current_id] = player
        self.current_id += 1
        return player

    def get(self, player_id: int) -> Player | None:
        return self.players.get(player_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Player]:
        players = list(self.players.values())
        return players[skip:skip + limit]

    def update(self, player_id: int, username: str | None = None,
               level: int | None = None, rating: int | None = None) -> Player | None:
        player = self.players.get(player_id)
        if not player:
            return None
        if username is not None:
            player.username = username
        if level is not None:
            player.level = level
        if rating is not None:
            player.rating = rating
        return player

    def delete(self, player_id: int) -> bool:
        if player_id in self.players:
            del self.players[player_id]
            return True
        return False


class ResourceDatabase:
    def __init__(self):
        self.resources: Dict[int, Resource] = {}
        self.current_id: int = 1

    def create(self, name: str, amount: int, player_id: int) -> Resource:
        resource = Resource(
            id=self.current_id,
            name=name,
            amount=amount,
            player_id=player_id
        )
        self.resources[self.current_id] = resource
        self.current_id += 1
        return resource

    def get(self, resource_id: int) -> Resource | None:
        return self.resources.get(resource_id)

    def get_all(self, skip: int = 0, limit: int = 100, player_id: int | None = None) -> List[Resource]:
        resources = list(self.resources.values())
        if player_id is not None:
            resources = [r for r in resources if r.player_id == player_id]
        return resources[skip:skip + limit]

    def update(self, resource_id: int, name: str | None = None, amount: int | None = None) -> Resource | None:
        resource = self.resources.get(resource_id)
        if not resource:
            return None
        if name is not None:
            resource.name = name
        if amount is not None:
            resource.amount = amount
        return resource

    def delete(self, resource_id: int) -> bool:
        if resource_id in self.resources:
            del self.resources[resource_id]
            return True
        return False


class MatchDatabase:
    def __init__(self):
        self.matches: Dict[int, Match] = {}
        self.current_id: int = 1

    def create(self, status: str, players: List[int], duration: int | None = None) -> Match:
        match = Match(
            id=self.current_id,
            status=status,
            players=players,
            duration=duration
        )
        self.matches[self.current_id] = match
        self.current_id += 1
        return match

    def get(self, match_id: int) -> Match | None:
        return self.matches.get(match_id)

    def get_all(self, skip: int = 0, limit: int = 100, status: str | None = None) -> List[Match]:
        matches = list(self.matches.values())
        if status:
            matches = [m for m in matches if m.status == status]
        return matches[skip:skip + limit]

    def update(self, match_id: int, status: str | None = None, duration: int | None = None) -> Match | None:
        match = self.matches.get(match_id)
        if not match:
            return None
        if status is not None:
            match.status = status
        if duration is not None:
            match.duration = duration
        return match

    def delete(self, match_id: int) -> bool:
        if match_id in self.matches:
            del self.matches[match_id]
            return True
        return False


players_db = PlayerDatabase()
resources_db = ResourceDatabase()
matches_db = MatchDatabase()