from sqlalchemy.orm import Session
from ..models import CardTemplate
from ..schemas import CardTemplateCreate
from typing import List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class TemplateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, template: CardTemplateCreate) -> CardTemplate:
        # Convertemos para dict para poder manipular
        template_data = template.dict()
        
        # Log para debug
        logger.debug(f"Dados recebidos para criar template: {template_data}")
        
        # Criamos a instância do modelo
        db_template = CardTemplate(**template_data)
        
        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        
        return db_template

    def get_by_id(self, template_id: str) -> Optional[CardTemplate]:
        return self.db.query(CardTemplate).filter(CardTemplate.id == template_id).first()

    def get_all(self) -> List[CardTemplate]:
        return self.db.query(CardTemplate).order_by(CardTemplate.name).all()

    def update(self, template_id: str, template_data: dict) -> Optional[CardTemplate]:
        db_template = self.get_by_id(template_id)
        if db_template:
            for key, value in template_data.items():
                setattr(db_template, key, value)
            self.db.commit()
            self.db.refresh(db_template)
        return db_template

    def delete(self, template_id: str) -> bool:
        db_template = self.get_by_id(template_id)
        if db_template:
            self.db.delete(db_template)
            self.db.commit()
            return True
        return False
    
    def check_exists(self, id: str = None, name: str = None) -> dict:
        """Verifica se existe template com mesmo ID ou nome"""
        exists = {
            'id': False,
            'name': False
        }
        
        if id:
            exists['id'] = self.db.query(CardTemplate).filter(CardTemplate.id == id).first() is not None
        
        if name:
            exists['name'] = self.db.query(CardTemplate).filter(CardTemplate.name == name).first() is not None
        
        return exists