from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Modificar o formato da URL para ser mais explícito
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:lightning7@localhost:5432/yakuza_tcg")

# Criar engine com encoding específico
engine = create_engine(
    DATABASE_URL,
    client_encoding='utf8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()