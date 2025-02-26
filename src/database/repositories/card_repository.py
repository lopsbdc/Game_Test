from sqlalchemy.orm import Session
from ..models import Card
from ..schemas import CardCreate
from typing import List, Optional



class CardRepository:
    def __init__(self, db: Session):
        self.db = db
    

    def create(self, card: CardCreate) -> Card:
        # Convertemos para dict para poder manipular
        card_data = card.dict()
        
        # Log para debug
        print("Dados recebidos para criar carta:", card_data)
        
        # Criamos a instância do modelo
        db_card = Card(**card_data)
        
        # Log para debug
        print("Dados da carta antes de salvar:", {
            "id": db_card.id,
            "name": db_card.name,
            "image_url": db_card.image_url
        })
        
        self.db.add(db_card)
        self.db.commit()
        self.db.refresh(db_card)
        
        # Log após salvar
        print("Dados da carta após salvar:", {
            "id": db_card.id,
            "name": db_card.name,
            "image_url": db_card.image_url
        })
        
        return db_card

    def get_by_id(self, card_id: str) -> Optional[Card]:
        return self.db.query(Card).filter(Card.id == card_id).first()

    def get_all(self) -> List[Card]:
        return self.db.query(Card).order_by(Card.name).all()

    def update(self, card_id: str, card_data: dict) -> Optional[Card]:
        db_card = self.get_by_id(card_id)
        if db_card:
            for key, value in card_data.items():
                setattr(db_card, key, value)
            self.db.commit()
            self.db.refresh(db_card)
        return db_card

    def delete(self, card_id: str) -> bool:
        db_card = self.get_by_id(card_id)
        if db_card:
            self.db.delete(db_card)
            self.db.commit()
            return True
        return False
    
    def check_exists(self, id: str = None, name: str = None) -> dict:
        """Verifica se existe carta com mesmo ID ou nome"""
        exists = {
            'id': False,
            'name': False
        }
        
        if id:
            exists['id'] = self.db.query(Card).filter(Card.id == id).first() is not None
        
        if name:
            exists['name'] = self.db.query(Card).filter(Card.name == name).first() is not None
        
        return exists