from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Optional, Any

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

# Esquema para representar uma carta no deck com sua quantidade
class DeckCardBase(BaseModel):
    card_id: str
    quantity: int = 1
    is_money: bool = False
    is_heat: bool = False

# Esquema para criação de um deck
class DeckCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    leader_id: str
    cards: List[DeckCardBase]
    
    @validator('cards')
    def validate_deck_rules(cls, cards):
        # Contadores para as validações
        main_count = 0
        money_count = 0
        heat_count = 0
        card_counts = {}
        
        for card in cards:
            # Contar cartas por tipo
            if card.is_heat:
                heat_count += card.quantity
            elif card.is_money:
                money_count += card.quantity
            else:
                main_count += card.quantity
                
            # Verificar limite de 3 cópias por carta
            if card.card_id in card_counts:
                card_counts[card.card_id] += card.quantity
            else:
                card_counts[card.card_id] = card.quantity
                
            if card_counts[card.card_id] > 3:
                raise ValueError(f"Máximo de 3 cópias da carta {card.card_id} permitidas")
        
        # Validar regras do deck
        if main_count < 40 or main_count > 50:
            raise ValueError(f"O deck principal deve ter entre 40 e 50 cartas. Atual: {main_count}")
            
        if money_count < 10 or money_count > 30:
            raise ValueError(f"O deck deve ter entre 10 e 30 cartas de dinheiro. Atual: {money_count}")
            
        if heat_count != 5:
            raise ValueError(f"O Heat Deck deve ter exatamente 5 cartas. Atual: {heat_count}")
            
        # Total de cartas entre 50 e 80
        total = main_count + money_count + heat_count
        if total < 50 or total > 80:
            raise ValueError(f"O total de cartas deve ser entre 50 e 80. Atual: {total}")
            
        return cards

# Esquema para resposta de um deck
class Deck(BaseModel):
    id: str
    name: str
    description: Optional[str]
    leader_id: str
    cards: List[DeckCardBase]
    created_at: datetime
    updated_at: Optional[datetime]
    stats: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

# Esquema para estatísticas do deck
class DeckStats(BaseModel):
    card_count: int
    main_count: int
    money_count: int
    heat_count: int
    mana_curve: Dict[str, int]
    color_distribution: Dict[str, int]
    card_type_distribution: Dict[str, int]


class ZoneBase(BaseModel):
    x: int
    y: int
    width: int
    height: int
    type: str  # "text", "image", "rectangle", "circle", "icon", etc.
    z_index: Optional[int] = 1  # Ordem de camada
    opacity: Optional[float] = 1.0  # Opacidade do elemento (0.0 a 1.0)
    background_color: Optional[str] = None  # Cor de fundo do elemento
    border_color: Optional[str] = None  # Cor da borda
    border_width: Optional[int] = 0  # Largura da borda
    
    # Apenas para zonas de texto
    font_size: Optional[int] = None
    font_family: Optional[str] = None
    text_align: Optional[str] = None
    text_color: Optional[str] = None
    field_name: Optional[str] = None  # Campo da carta a ser usado (name, text, etc.)
    
    # Para círculos
    border_radius: Optional[int] = None  # Para cantos arredondados em retângulos ou raio de círculos

# Esquema base para CardTemplate
class CardTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    background_type: str = "color_based"
    overlay_opacity: int = 80  # 0-100
    width_mm: int = 63
    height_mm: int = 88
    zones: Optional[Dict[str, Any]] = None

# Esquema para criação de CardTemplate
class CardTemplateCreate(CardTemplateBase):
    id: str

# Esquema completo para CardTemplate
class CardTemplate(CardTemplateBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        background_image_url: Optional[str] = None