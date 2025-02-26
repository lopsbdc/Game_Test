from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from ..database.connection import get_db
from ..database.repositories.card_repository import CardRepository
from ..database.schemas import CardCreate, Card
import logging
import sys


# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def handle_image_upload(image, card_id: str) -> str:
    """
    Função auxiliar para processar upload de imagem.
    Retorna a URL da imagem se bem sucedido.
    """
    try:
        logger.info(f"Processando imagem para card_id: {card_id}")
        
        image_dir = Path("static/images")
        image_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = image_dir / f"{card_id}.png"
        contents = await image.read()
        
        with open(file_path, "wb") as f:
            f.write(contents)
            
        if file_path.exists():
            image_url = f"/static/images/{card_id}.png"
            logger.info(f"Imagem salva com sucesso: {image_url}")
            return image_url
        else:
            raise Exception("Arquivo não foi criado")
            
    except Exception as e:
        logger.error(f"Erro no upload da imagem: {str(e)}")
        raise

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Rota GET para listar cartas
@router.get("/cards", response_class=HTMLResponse)
async def list_cards(request: Request, db: Session = Depends(get_db)):
    repository = CardRepository(db)
    cards = repository.get_all()
    return templates.TemplateResponse("cards/list.html", {"request": request, "cards": cards})

# Nova carta - GET (formulário)
@router.get("/cards/new", response_class=HTMLResponse)
async def new_card_form(request: Request):
    return templates.TemplateResponse("cards/form.html", {
        "request": request,
        "card": None
    })

@router.post("/cards/new/check")
async def check_card(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    repository = CardRepository(db)
    
    exists = repository.check_exists(
        id=form.get('id'),
        name=form.get('name')
    )
    
    return exists

# Nova carta - POST (salvar)
@router.post("/cards/new")
async def create_card(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        form = await request.form()
        card_data = dict(form)
        print("Dados iniciais:", card_data)

        if "image" in form and hasattr(form["image"], "filename"):
            logger.info("Processando upload de imagem")
            image = form["image"]
            file_path = Path(f"static/images/{card_data['id']}.png")
            logger.debug(f"Caminho do arquivo: {file_path}")
            
            file_path.parent.mkdir(exist_ok=True)
            content = await image.read()
            logger.debug(f"Tamanho do conteúdo: {len(content)} bytes")
            
            file_path.write_bytes(content)
            logger.info(f"Imagem salva em: {file_path}")
            
            card_data['image_url'] = f"/static/images/{card_data['id']}.png"
            print("Dados após adicionar image_url:", card_data)
        else:
            logger.warning("Nenhuma imagem encontrada no formulário")

        # Convertemos tipos numéricos
        if 'cost' in card_data:
            card_data['cost'] = int(card_data['cost'])
        if 'power' in card_data:
            card_data['power'] = int(card_data['power'])
        if 'heat_cost' in card_data:
            card_data['heat_cost'] = int(card_data['heat_cost'])

        print("Dados finais antes de criar:", card_data)
        repository = CardRepository(db)
        repository.create(CardCreate(**card_data))
        logger.info("Carta criada com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao criar carta: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    return RedirectResponse(url="/cards", status_code=303)

# Rota GET para visualizar carta
@router.get("/cards/{card_id}", response_class=HTMLResponse)
async def view_card(request: Request, card_id: str, db: Session = Depends(get_db)):
    repository = CardRepository(db)
    card = repository.get_by_id(card_id)
    return templates.TemplateResponse("cards/view.html", {"request": request, "card": card})

# Rota GET para editar carta
@router.get("/cards/{card_id}/edit", response_class=HTMLResponse)
async def edit_card(request: Request, card_id: str, db: Session = Depends(get_db)):
    repository = CardRepository(db)
    card = repository.get_by_id(card_id)
    return templates.TemplateResponse("cards/form.html", {"request": request, "card": card})

@router.get("/cards/{card_id}/delete")
async def delete_card(card_id: str, db: Session = Depends(get_db)):
    repository = CardRepository(db)
    repository.delete(card_id)
    return RedirectResponse(url="/cards", status_code=303)

# Rota POST para salvar edição
@router.post("/cards/{card_id}/edit")
async def update_card(
    request: Request,
    card_id: str,
    db: Session = Depends(get_db)
):
    try:
        form = await request.form()
        card_data = dict(form)

        if "image" in form and hasattr(form["image"], "filename"):
            image = form["image"]
            card_data['image_url'] = await handle_image_upload(image, card_id)

        repository = CardRepository(db)
        repository.update(card_id, card_data)
        return RedirectResponse(url="/cards", status_code=303)
        
    except Exception as e:
        logger.error(f"Erro ao atualizar carta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
