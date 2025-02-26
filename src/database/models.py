from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from .connection import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    color = Column(String)
    cost = Column(Integer)
    power = Column(Integer)
    rarity = Column(String)
    text = Column(String)
    heat_effect = Column(String)
    heat_cost = Column(Integer)
    flavor_text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    image_url = Column(String, nullable=True)