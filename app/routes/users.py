"""
app/routes/users.py — CRUD utilisateurs (simple)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models.user import User
from ..schemas.user import UserOut, UserUpdate
from ..deps import get_current_user, require_admin
from ..core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserOut])
def list_users(
    # Pagination simple + recherche
    limit: int = Query(50, ge=1, le=200, description="Nombre max d'éléments"),
    offset: int = Query(0, ge=0, description="Décalage de départ"),
    search: str | None = Query(None, description="Filtre email contient..."),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # token obligatoire
    # Pour limiter aux admins: remplacer la ligne au-dessus par:
    # current_admin: User = Depends(require_admin),
):
    """
    Liste paginée des utilisateurs (protégé par token).
    - limit/offset pour paginer.
    - search pour filtrer par email contenant 'search'.
    """
    q = db.query(User)
    if search:
        q = q.filter(User.email.contains(search))
    users = q.offset(offset).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Récupère un utilisateur par ID. Protégé.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Met à jour un utilisateur.
    - Règle: l'utilisateur peut se modifier lui-même.
    - Un admin peut modifier n'importe quel compte (email/role).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Permission: self ou admin
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Action non autorisée")

    # Email
    if payload.email and payload.email != user.email:
        exists = db.query(User).filter(User.email == payload.email, User.id != user_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        user.email = payload.email

    # Password
    if payload.password:
        user.hashed_password = get_password_hash(payload.password)

    # Role (seulement admin)
    if payload.role is not None:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Seul un admin peut changer le rôle")
        if payload.role not in ("user", "admin"):
            raise HTTPException(status_code=400, detail="Role invalide (user/admin)")
        user.role = payload.role

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Désactive (soft delete) un utilisateur.
    - Règle: self ou admin.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Action non autorisée")

    user.is_active = False
    db.add(user)
    db.commit()
    return {"status": "deleted"}
