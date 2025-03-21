from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Boolean, JSON
from sqlalchemy.orm import relationship
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
    
    # Adicionar referência ao template
    template_id = Column(String, ForeignKey('card_templates.id'), nullable=True)
    template = relationship("CardTemplate")

# Tabela de associação para relacionamento muitos-para-muitos entre Deck e Card
deck_card = Table('deck_cards', Base.metadata,
    Column('deck_id', String, ForeignKey('decks.id')),
    Column('card_id', String, ForeignKey('cards.id')),
    Column('quantity', Integer, default=1),
    Column('is_money', Boolean, default=False),
    Column('is_heat', Boolean, default=False)
)

class Deck(Base):
    __tablename__ = "decks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    leader_id = Column(String, ForeignKey('cards.id'), nullable=False)
    
    # Statistics and metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    leader = relationship("Card", foreign_keys=[leader_id])
    cards = relationship("Card", secondary=deck_card, backref="decks")
    
    # Optional statistics stored as JSON
    stats = Column(JSON, nullable=True)

class CardTemplate(Base):
    __tablename__ = "card_templates"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    background_image_url = Column(String, nullable=True)

    # Configurações visuais básicas
    background_type = Column(String, default="color_based")  # color_based, image, gradient
    overlay_opacity = Column(Integer, default=80)  # Valor de 0-100 para opacidade
    
    # Dimensões (padrão Magic)
    width_mm = Column(Integer, default=63)  # 63mm (padrão Magic)
    height_mm = Column(Integer, default=88)  # 88mm (padrão Magic)
    
    # Zonas em formato JSON
    zones = Column(JSON, nullable=True)  # Armazenado como JSON com definições de zonas
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())