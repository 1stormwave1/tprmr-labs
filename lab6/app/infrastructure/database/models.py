from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class PlayerModel(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    level = Column(Integer, default=1)
    rating = Column(Float, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    resources = relationship("ResourceModel", back_populates="player")
    matches = relationship("MatchModel", back_populates="player")


class ResourceModel(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    name = Column(String, nullable=False)
    amount = Column(Integer, default=0)

    player = relationship("PlayerModel", back_populates="resources")


class MatchModel(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    status = Column(String, nullable=False)  
    duration = Column(Float) 

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("PlayerModel", back_populates="matches")
