from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from ..models import Deck, Card, deck_card
from ..schemas import DeckCreate, DeckStats
from typing import List, Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class DeckRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, deck: DeckCreate) -> Deck:
        # Convertemos para dict para poder manipular
        deck_data = {
            "id": deck.id,
            "name": deck.name,
            "description": deck.description,
            "leader_id": deck.leader_id
        }
        
        # Criamos a instância do modelo
        db_deck = Deck(**deck_data)
        
        # Calculamos estatísticas
        stats = self._calculate_stats(deck)
        db_deck.stats = stats
        
        self.db.add(db_deck)
        self.db.commit()
        
        # Agora adicionamos as cartas ao deck
        self._update_deck_cards(db_deck.id, deck.cards)
        
        self.db.refresh(db_deck)
        return db_deck
    
    def get_by_id(self, deck_id: str) -> Optional[Deck]:
        return self.db.query(Deck).filter(Deck.id == deck_id).first()
    
    def get_all(self) -> List[Deck]:
        return self.db.query(Deck).order_by(Deck.name).all()
    
    def update(self, deck_id: str, deck_data: dict) -> Optional[Deck]:
        db_deck = self.get_by_id(deck_id)
        if db_deck:
            # Atualizar campos básicos do deck
            if "name" in deck_data:
                db_deck.name = deck_data["name"]
            if "description" in deck_data:
                db_deck.description = deck_data["description"]
            if "leader_id" in deck_data:
                db_deck.leader_id = deck_data["leader_id"]
            
            # Atualizar cartas se fornecidas
            if "cards" in deck_data:
                self._update_deck_cards(deck_id, deck_data["cards"])
                
                # Recalcular estatísticas
                stats = self._calculate_stats(deck_data)
                db_deck.stats = stats
            
            self.db.commit()
            self.db.refresh(db_deck)
        return db_deck
    
    def delete(self, deck_id: str) -> bool:
        db_deck = self.get_by_id(deck_id)
        if db_deck:
            # Remover associações de cartas
            self.db.execute(
                deck_card.delete().where(deck_card.c.deck_id == deck_id)
            )
            
            # Remover o deck
            self.db.delete(db_deck)
            self.db.commit()
            return True
        return False
    
    def _update_deck_cards(self, deck_id: str, cards: List[dict]) -> None:
        # Remover todas as cartas existentes
        self.db.execute(
            deck_card.delete().where(deck_card.c.deck_id == deck_id)
        )
        
        # Adicionar novas cartas
        for card in cards:
            self.db.execute(
                deck_card.insert().values(
                    deck_id=deck_id,
                    card_id=card["card_id"],
                    quantity=card["quantity"],
                    is_money=card.get("is_money", False),
                    is_heat=card.get("is_heat", False)
                )
            )
    
    def get_deck_cards(self, deck_id: str) -> List[Dict[str, Any]]:
        """Recupera todas as cartas de um deck com suas quantidades e detalhes"""
        query = self.db.query(
            Card,
            deck_card.c.quantity,
            deck_card.c.is_money,
            deck_card.c.is_heat
        ).join(
            deck_card, Card.id == deck_card.c.card_id
        ).filter(
            deck_card.c.deck_id == deck_id
        )
        
        result = []
        for card, quantity, is_money, is_heat in query:
            card_dict = {
                "id": card.id,
                "name": card.name,
                "card_type": card.card_type,
                "color": card.color,
                "cost": card.cost,
                "power": card.power,
                "rarity": card.rarity,
                "text": card.text,
                "image_url": card.image_url,
                "quantity": quantity,
                "is_money": is_money,
                "is_heat": is_heat
            }
            result.append(card_dict)
            
        return result
    
    def _calculate_stats(self, deck: Any) -> Dict[str, Any]:
        """Calcula estatísticas para o deck"""
        # Se for uma instância de DeckCreate
        if hasattr(deck, "cards"):
            cards = deck.cards
            card_ids = [card.card_id for card in cards]
            
            # Buscar detalhes das cartas
            db_cards = self.db.query(Card).filter(Card.id.in_(card_ids)).all()
            card_details = {card.id: card for card in db_cards}
            
            # Contadores
            main_count = sum(card.quantity for card in cards if not card.is_money and not card.is_heat)
            money_count = sum(card.quantity for card in cards if card.is_money)
            heat_count = sum(card.quantity for card in cards if card.is_heat)
            
            # Distribuição de mana/custo
            mana_curve = {}
            color_distribution = {}
            card_type_distribution = {}
            
            for card in cards:
                if card.card_id in card_details:
                    # Detalhes da carta
                    card_detail = card_details[card.card_id]
                    
                    # Curva de mana
                    cost = card_detail.cost or 0
                    if not card.is_money and not card.is_heat:  # Apenas para cartas principais
                        cost_key = str(cost)
                        if cost_key in mana_curve:
                            mana_curve[cost_key] += card.quantity
                        else:
                            mana_curve[cost_key] = card.quantity
                    
                    # Distribuição de cores
                    color = card_detail.color or "Colorless"
                    if not card.is_money and not card.is_heat:  # Apenas para cartas principais
                        if color in color_distribution:
                            color_distribution[color] += card.quantity
                        else:
                            color_distribution[color] = card.quantity
                    
                    # Distribuição de tipos
                    card_type = card_detail.card_type
                    if not card.is_money and not card.is_heat:  # Apenas para cartas principais
                        if card_type in card_type_distribution:
                            card_type_distribution[card_type] += card.quantity
                        else:
                            card_type_distribution[card_type] = card.quantity
            
            return {
                "card_count": main_count + money_count + heat_count,
                "main_count": main_count,
                "money_count": money_count,
                "heat_count": heat_count,
                "mana_curve": mana_curve,
                "color_distribution": color_distribution,
                "card_type_distribution": card_type_distribution
            }
        
        # Se for um dicionário
        elif isinstance(deck, dict) and "cards" in deck:
            # Lógica similar à acima, adaptada para dicionário
            pass
        
        # Fallback para estatísticas vazias
        return {
            "card_count": 0,
            "main_count": 0,
            "money_count": 0,
            "heat_count": 0,
            "mana_curve": {},
            "color_distribution": {},
            "card_type_distribution": {}
        }
    
    def validate_deck(self, deck_id: str) -> Dict[str, Any]:
        """Valida se um deck atende todas as regras do jogo"""
        cards = self.get_deck_cards(deck_id)
        
        # Contadores
        main_count = sum(card["quantity"] for card in cards if not card["is_money"] and not card["is_heat"])
        money_count = sum(card["quantity"] for card in cards if card["is_money"])
        heat_count = sum(card["quantity"] for card in cards if card["is_heat"])
        
        # Verificar limite de cópias
        card_counts = {}
        for card in cards:
            if card["id"] in card_counts:
                card_counts[card["id"]] += card["quantity"]
            else:
                card_counts[card["id"]] = card["quantity"]
        
        # Verificar se tem leader
        deck = self.get_by_id(deck_id)
        has_leader = deck is not None and deck.leader_id is not None
        
        # Verificar se o leader é válido (tipo Leader)
        leader_valid = False
        if has_leader:
            leader = self.db.query(Card).filter(Card.id == deck.leader_id).first()
            leader_valid = leader is not None and leader.card_type == "Leader"
        
        # Resultado da validação
        validation = {
            "valid": True,
            "errors": [],
            "stats": {
                "total_cards": main_count + money_count + heat_count,
                "main_deck": main_count,
                "money_deck": money_count,
                "heat_deck": heat_count
            }
        }
        
        # Checar regras específicas
        if main_count < 40 or main_count > 50:
            validation["valid"] = False
            validation["errors"].append(f"O deck principal deve ter entre 40 e 50 cartas. Atual: {main_count}")
        
        if money_count < 10 or money_count > 30:
            validation["valid"] = False
            validation["errors"].append(f"O deck deve ter entre 10 e 30 cartas de dinheiro. Atual: {money_count}")
        
        if heat_count != 5:
            validation["valid"] = False
            validation["errors"].append(f"O Heat Deck deve ter exatamente 5 cartas. Atual: {heat_count}")
        
        # Verificar limite de 3 cópias
        for card_id, count in card_counts.items():
            if count > 3:
                card_name = next((card["name"] for card in cards if card["id"] == card_id), card_id)
                validation["valid"] = False
                validation["errors"].append(f"Máximo de 3 cópias da carta '{card_name}' permitidas. Atual: {count}")
        
        # Verificar Leader
        if not has_leader:
            validation["valid"] = False
            validation["errors"].append("O deck precisa de um Leader.")
        elif not leader_valid:
            validation["valid"] = False
            validation["errors"].append("O Leader selecionado não é uma carta do tipo Leader.")
        
        return validation