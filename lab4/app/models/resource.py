from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    player = relationship("Player", back_populates="resources")
