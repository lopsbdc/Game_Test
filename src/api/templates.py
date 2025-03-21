from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
import json
import logging
import uuid

from ..database.connection import get_db
from ..database.repositories.template_repository import TemplateRepository
from ..database.schemas import CardTemplateCreate

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

async def handle_background_image_upload(image, template_id: str) -> str:
    """
    Função auxiliar para processar upload de imagem de fundo.
    Retorna a URL da imagem se bem sucedido.
    """
    try:
        logger.info(f"Processando imagem de fundo para template_id: {template_id}")
        
        image_dir = Path("static/templates")
        image_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = image_dir / f"{template_id}_bg.png"
        contents = await image.read()
        
        with open(file_path, "wb") as f:
            f.write(contents)
            
        if file_path.exists():
            image_url = f"/static/templates/{template_id}_bg.png"
            logger.info(f"Imagem de fundo salva com sucesso: {image_url}")
            return image_url
        else:
            raise Exception("Arquivo não foi criado")
            
    except Exception as e:
        logger.error(f"Erro no upload da imagem de fundo: {str(e)}")
        raise

# Rota para listar templates
@router.get("/templates", response_class=HTMLResponse)
async def list_templates(request: Request, db: Session = Depends(get_db)):
    repository = TemplateRepository(db)
    card_templates = repository.get_all()
    return templates.TemplateResponse("templates/list.html", {
        "request": request, 
        "templates": card_templates
    })

# Rota para novo template (formulário)
@router.get("/templates/new", response_class=HTMLResponse)
async def new_template_form(request: Request):
    return templates.TemplateResponse("templates/form.html", {
        "request": request,
        "template": None
    })

# Rota para verificar ID/nome duplicado
@router.post("/templates/new/check")
async def check_template(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    repository = TemplateRepository(db)
    
    exists = repository.check_exists(
        id=form.get('id'),
        name=form.get('name')
    )
    
    return exists

# Rota para criar template
@router.post("/templates/new")
async def create_template(request: Request, db: Session = Depends(get_db)):
    try:
        form = await request.form()
        template_data = dict(form)
        
        # Gerar ID se não fornecido
        if not template_data.get("id"):
            template_data["id"] = str(uuid.uuid4())[:8]
        
        # Converter campos numéricos
        if 'overlay_opacity' in template_data and template_data['overlay_opacity']:
            template_data['overlay_opacity'] = int(template_data['overlay_opacity'])
        if 'width_mm' in template_data and template_data['width_mm']:
            template_data['width_mm'] = int(template_data['width_mm'])
        if 'height_mm' in template_data and template_data['height_mm']:
            template_data['height_mm'] = int(template_data['height_mm'])

        if "background_image" in form and hasattr(form["background_image"], "filename"):
            image = form["background_image"]
            template_data['background_image_url'] = await handle_background_image_upload(image, template_data['id'])
        
        # Processar zonas do JSON
        if 'zones' in template_data and template_data['zones']:
            try:
                zones_str = template_data['zones']
                template_data['zones'] = json.loads(zones_str)
            except json.JSONDecodeError:
                logger.warning("Formato JSON inválido para zonas")
                template_data['zones'] = {}
        
        repository = TemplateRepository(db)
        repository.create(CardTemplateCreate(**template_data))
        logger.info(f"Template criado com sucesso: {template_data['id']}")
        
    except Exception as e:
        logger.error(f"Erro ao criar template: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    return RedirectResponse(url="/templates", status_code=303)

# Rota para visualizar template
@router.get("/templates/{template_id}", response_class=HTMLResponse)
async def view_template(request: Request, template_id: str, db: Session = Depends(get_db)):
    repository = TemplateRepository(db)
    template = repository.get_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return templates.TemplateResponse("templates/view.html", {
        "request": request, 
        "template": template
    })

# Rota para editar template (formulário)
@router.get("/templates/{template_id}/edit", response_class=HTMLResponse)
async def edit_template_form(request: Request, template_id: str, db: Session = Depends(get_db)):
    repository = TemplateRepository(db)
    template = repository.get_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return templates.TemplateResponse("templates/form.html", {
        "request": request, 
        "template": template
    })

# Rota para atualizar template
@router.post("/templates/{template_id}/edit")
async def update_template(request: Request, template_id: str, db: Session = Depends(get_db)):
    try:
        form = await request.form()
        template_data = dict(form)
        
        # Converter campos numéricos
        if 'overlay_opacity' in template_data and template_data['overlay_opacity']:
            template_data['overlay_opacity'] = int(template_data['overlay_opacity'])
        if 'width_mm' in template_data and template_data['width_mm']:
            template_data['width_mm'] = int(template_data['width_mm'])
        if 'height_mm' in template_data and template_data['height_mm']:
            template_data['height_mm'] = int(template_data['height_mm'])

        if "background_image" in form and hasattr(form["background_image"], "filename"):
            image = form["background_image"] 
            template_data['background_image_url'] = await handle_background_image_upload(image, template_id)
        
        # Processar zonas do JSON
        if 'zones' in template_data and template_data['zones']:
            try:
                zones_str = template_data['zones']
                template_data['zones'] = json.loads(zones_str)
            except json.JSONDecodeError:
                logger.warning("Formato JSON inválido para zonas")
                template_data['zones'] = {}
        
        repository = TemplateRepository(db)
        repository.update(template_id, template_data)
        logger.info(f"Template atualizado com sucesso: {template_id}")
        
    except Exception as e:
        logger.error(f"Erro ao atualizar template: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    return RedirectResponse(url=f"/templates/{template_id}", status_code=303)

# Rota para excluir template
@router.get("/templates/{template_id}/delete")
async def delete_template(template_id: str, db: Session = Depends(get_db)):
    repository = TemplateRepository(db)
    success = repository.delete(template_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return RedirectResponse(url="/templates", status_code=303)

# Rota para editor visual de template
@router.get("/templates/{template_id}/editor", response_class=HTMLResponse)
async def template_editor(request: Request, template_id: str, db: Session = Depends(get_db)):
    repository = TemplateRepository(db)
    template = repository.get_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return templates.TemplateResponse("templates/editor.html", {
        "request": request, 
        "template": template
    })

# Rota para salvar alterações do editor visual
@router.post("/templates/{template_id}/zones")
async def update_template_zones(request: Request, template_id: str, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        zones = data.get("zones", {})
        
        repository = TemplateRepository(db)
        template = repository.get_by_id(template_id)
        
        if not template:
            raise HTTPException(status_code=404, detail="Template não encontrado")
        
        # Atualizar apenas as zonas
        repository.update(template_id, {"zones": zones})
        
        return {"success": True, "message": "Zonas atualizadas com sucesso"}
        
    except Exception as e:
        logger.error(f"Erro ao atualizar zonas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/{template_id}/json")
async def get_template_json(template_id: str, db: Session = Depends(get_db)):
    repository = TemplateRepository(db)
    template = repository.get_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "background_type": template.background_type,
        "background_image_url": template.background_image_url,
        "overlay_opacity": template.overlay_opacity,
        "width_mm": template.width_mm,
        "height_mm": template.height_mm,
        "zones": template.zones
    }

@router.get("/templates/presets/{preset_name}")
async def get_template_preset(preset_name: str, db: Session = Depends(get_db)):
    # Definir alguns presets básicos
    presets = {
        "standard": {
            "name": "Template Padrão",
            "description": "Um template padrão com zonas para título, imagem, tipo, custo, poder e texto",
            "width_mm": 63,
            "height_mm": 88,
            "background_type": "color_based",
            "overlay_opacity": 80,
            "zones": {
                "title": {
                    "type": "text",
                    "x": 10,
                    "y": 10,
                    "width": 180,
                    "height": 30,
                    "field_name": "name",
                    "font_size": 16,
                    "text_align": "center",
                    "z_index": 10
                },
                "image": {
                    "type": "image",
                    "x": 20,
                    "y": 50,
                    "width": 160,
                    "height": 120,
                    "z_index": 5,
                    "image_fit": "contain"
                },
                "type": {
                    "type": "text",
                    "x": 10,
                    "y": 180,
                    "width": 100,
                    "height": 25,
                    "field_name": "card_type",
                    "font_size": 12,
                    "z_index": 10
                },
                "cost": {
                    "type": "text",
                    "x": 160,
                    "y": 180,
                    "width": 40,
                    "height": 40,
                    "field_name": "cost",
                    "font_size": 14,
                    "text_align": "center",
                    "z_index": 10,
                    "background_color": "rgba(0,0,0,0.5)",
                    "border_radius": 20
                },
                "text": {
                    "type": "text",
                    "x": 10,
                    "y": 210,
                    "width": 180,
                    "height": 100,
                    "field_name": "text",
                    "font_size": 12,
                    "z_index": 10,
                    "background_color": "rgba(0,0,0,0.3)",
                    "border_radius": 5
                },
                "flavor": {
                    "type": "text",
                    "x": 10,
                    "y": 320,
                    "width": 180,
                    "height": 30,
                    "field_name": "flavor_text",
                    "font_size": 10,
                    "font_style": "italic",
                    "text_align": "center",
                    "z_index": 10
                }
            }
        },
        # Outros presets podem ser adicionados aqui
    }
    
    if preset_name not in presets:
        raise HTTPException(status_code=404, detail="Preset não encontrado")
    
    return presets[preset_name]