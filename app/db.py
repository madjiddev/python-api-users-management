"""
app/db.py — Connexion base + session SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Charger .env si présent
load_dotenv()

# URL DB (par défaut: SQLite fichier local ./app.db)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ORM
Base = declarative_base()

# Dépendance pour FastAPI: ouvre/ferme une session par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
