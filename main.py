from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.api import cards, decks, templates  # Adicionar o módulo de templates

app = FastAPI(title="Yakuza TCG")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclui as rotas
app.include_router(cards.router)
app.include_router(decks.router)
app.include_router(templates.router)