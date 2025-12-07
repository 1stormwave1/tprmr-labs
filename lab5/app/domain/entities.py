
from datetime import datetime
from typing import Optional, List


class PlayerEntity:
    def __init__(
        self,
        id: Optional[int],
        username: str,
        level: int,
        rating: int,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.level = level
        self.rating = rating
        self.created_at = created_at
        self.updated_at = updated_at

    def increase_level(self, amount: int = 1):
        if amount <= 0:
            raise ValueError("Кількість рівнів має бути > 0")
        self.level += amount

    def change_rating(self, delta: int):
        self.rating += delta


class ResourceEntity:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        amount: int,
        player_id: int
    ):
        self.id = id
        self.name = name
        self.amount = amount
        self.player_id = player_id

    def add_amount(self, value: int):
        if value <= 0:
            raise ValueError("Значення має бути > 0")
        self.amount += value

    def remove_amount(self, value: int):
        if value <= 0:
            raise ValueError("Значення має бути > 0")
        if value > self.amount:
            raise ValueError("Недостатньо ресурсу")
        self.amount -= value


class MatchEntity:
    def __init__(
        self,
        id: Optional[int],
        status: str,
        duration: Optional[int],
        player_id: Optional[int] = None
    ):
        self.id = id
        self.status = status
        self.duration = duration
        self.player_id = player_id
