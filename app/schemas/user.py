"""
app/schemas/user.py — Schémas Pydantic (entrées/sorties API)
"""

from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: constr(min_length=8) | None = None
    role: str | None = None  # uniquement admin côté route (on protégera)

class UserOut(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    # Pydantic v2:
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
