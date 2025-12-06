from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False, index=True)
    level = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

    resources = relationship("Resource", back_populates="player")
    matches = relationship(
        "Match",
        secondary="match_players",
        back_populates="players"
    )
