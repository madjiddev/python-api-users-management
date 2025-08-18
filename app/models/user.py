"""
app/models/user.py — Modèle ORM User (table 'users')
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Rôle simple: 'user' (par défaut) ou 'admin'
    role = Column(String, default="user", nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
