from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CardBase(BaseModel):
    name: str
    card_type: str
    color: Optional[str] = None
    cost: Optional[int] = None
    power: Optional[int] = None
    rarity: Optional[str] = None
    text: Optional[str] = None
    heat_effect: Optional[str] = None
    heat_cost: Optional[int] = None
    flavor_text: Optional[str] = None
    image_url: Optional[str] = None  

class CardCreate(CardBase):
    id: str

class Card(CardBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True