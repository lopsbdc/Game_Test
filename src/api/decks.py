from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
import logging
import uuid

from ..database.connection import get_db
from ..database.repositories.card_repository import CardRepository
from ..database.repositories.deck_repository import DeckRepository
from ..database.schemas import DeckCreate, DeckCardBase

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Rota para listar decks
@router.get("/decks", response_class=HTMLResponse)
async def list_decks(request: Request, db: Session = Depends(get_db)):
    repository = DeckRepository(db)
    decks = repository.get_all()
    return templates.TemplateResponse("decks/list.html", {"request": request, "decks": decks})

# Rota para novo deck (formulário)
@router.get("/decks/new", response_class=HTMLResponse)
async def new_deck_form(request: Request, db: Session = Depends(get_db)):
    card_repo = CardRepository(db)
    cards = card_repo.get_all()
    
    # Separar líderes para facilitar a seleção
    leaders = [card for card in cards if card.card_type == "Leader"]
    
    return templates.TemplateResponse("decks/form.html", {
        "request": request,
        "deck": None,
        "cards": cards,
        "leaders": leaders
    })

# Rota para criar deck
@router.post("/decks/new")
async def create_deck(request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        deck_data = dict(form_data)
        
        # Gerar ID se não fornecido
        if not deck_data.get("id"):
            deck_data["id"] = str(uuid.uuid4())[:8]
        
        # Extrair cartas do formulário
        cards_data = json.loads(deck_data.get("cards_json", "[]"))
        
        # Converter para formato esperado
        cards = []
        for card in cards_data:
            deck_card = DeckCardBase(
                card_id=card["id"],
                quantity=card["quantity"],
                is_money=card.get("is_money", False),
                is_heat=card.get("is_heat", False)
            )
            cards.append(deck_card)
        
        # Criar objeto DeckCreate
        deck_create = DeckCreate(
            id=deck_data["id"],
            name=deck_data["name"],
            description=deck_data.get("description", ""),
            leader_id=deck_data["leader_id"],
            cards=cards
        )
        
        # Salvar no banco
        repository = DeckRepository(db)
        repository.create(deck_create)
        
        return RedirectResponse(url="/decks", status_code=303)
    
    except Exception as e:
        logger.error(f"Erro ao criar deck: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Rota para visualizar deck
@router.get("/decks/{deck_id}", response_class=HTMLResponse)
async def view_deck(request: Request, deck_id: str, db: Session = Depends(get_db)):
    repository = DeckRepository(db)
    deck = repository.get_by_id(deck_id)
    
    if not deck:
        raise HTTPException(status_code=404, detail="Deck não encontrado")
    
    # Buscar detalhes completos das cartas
    cards = repository.get_deck_cards(deck_id)
    
    # Buscar carta líder
    card_repo = CardRepository(db)
    leader = card_repo.get_by_id(deck.leader_id)
    
    # Validar deck
    validation = repository.validate_deck(deck_id)
    
    return templates.TemplateResponse("decks/view.html", {
        "request": request,
        "deck": deck,
        "cards": cards,
        "leader": leader,
        "validation": validation
    })

# Rota para editar deck (formulário)
@router.get("/decks/{deck_id}/edit", response_class=HTMLResponse)
async def edit_deck_form(request: Request, deck_id: str, db: Session = Depends(get_db)):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    
    deck = deck_repo.get_by_id(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck não encontrado")
    
    cards = card_repo.get_all()
    deck_cards = deck_repo.get_deck_cards(deck_id)
    
    # Separar líderes para facilitar a seleção
    leaders = [card for card in cards if card.card_type == "Leader"]
    
    return templates.TemplateResponse("decks/form.html", {
        "request": request,
        "deck": deck,
        "deck_cards": deck_cards,
        "cards": cards,
        "leaders": leaders
    })

# Rota para atualizar deck
@router.post("/decks/{deck_id}/edit")
async def update_deck(request: Request, deck_id: str, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        deck_data = dict(form_data)
        
        # Extrair cartas do formulário
        cards_data = json.loads(deck_data.get("cards_json", "[]"))
        
        # Converter para formato esperado
        cards = []
        for card in cards_data:
            deck_card = {
                "card_id": card["id"],
                "quantity": card["quantity"],
                "is_money": card.get("is_money", False),
                "is_heat": card.get("is_heat", False)
            }
            cards.append(deck_card)
        
        # Atualizar dados básicos
        update_data = {
            "name": deck_data["name"],
            "description": deck_data.get("description", ""),
            "leader_id": deck_data["leader_id"],
            "cards": cards
        }
        
        # Atualizar no banco
        repository = DeckRepository(db)
        repository.update(deck_id, update_data)
        
        return RedirectResponse(url=f"/decks/{deck_id}", status_code=303)
    
    except Exception as e:
        logger.error(f"Erro ao atualizar deck: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Rota para deletar deck
@router.get("/decks/{deck_id}/delete")
async def delete_deck(deck_id: str, db: Session = Depends(get_db)):
    repository = DeckRepository(db)
    success = repository.delete(deck_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Deck não encontrado")
    
    return RedirectResponse(url="/decks", status_code=303)

# Rota para validar deck
@router.get("/decks/{deck_id}/validate")
async def validate_deck(deck_id: str, db: Session = Depends(get_db)):
    repository = DeckRepository(db)
    validation = repository.validate_deck(deck_id)
    return validation

# Rota para obter estatísticas do deck
@router.get("/decks/{deck_id}/stats")
async def deck_stats(deck_id: str, db: Session = Depends(get_db)):
    repository = DeckRepository(db)
    deck = repository.get_by_id(deck_id)
    
    if not deck:
        raise HTTPException(status_code=404, detail="Deck não encontrado")
    
    return deck.stats or {}

# Rota para exportar deck
@router.get("/decks/{deck_id}/export")
async def export_deck(deck_id: str, db: Session = Depends(get_db)):
    repository = DeckRepository(db)
    deck = repository.get_by_id(deck_id)
    
    if not deck:
        raise HTTPException(status_code=404, detail="Deck não encontrado")
    
    # Buscar detalhes completos das cartas
    cards = repository.get_deck_cards(deck_id)
    
    export_data = {
        "id": deck.id,
        "name": deck.name,
        "description": deck.description,
        "leader_id": deck.leader_id,
        "cards": cards
    }
    
    return export_data