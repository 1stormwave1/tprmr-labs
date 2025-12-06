from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.player import Player

# Таблиця для зв'язку багато-до-багатьох між матчами і гравцями
match_players = Table(
    "match_players",
    Base.metadata,
    Column("match_id", ForeignKey("matches.id"), primary_key=True),
    Column("player_id", ForeignKey("players.id"), primary_key=True)
)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)

    players = relationship(
        "Player",
        secondary=match_players,
        back_populates="matches"
    )
