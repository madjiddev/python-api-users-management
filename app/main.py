"""
app/main.py — Point d'entrée de l'API

- Crée l'application FastAPI
- Configure CORS
- Personnalise la doc OpenAPI (Swagger/ReDoc avec sécurité JWT)
- Monte les routers d'auth et d'utilisateurs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routes import auth, users
from .db import Base, engine
from .models.user import User  # noqa: F401 (pour que la table soit connue)
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env (si présent)
load_dotenv()

# Crée (si besoin) les tables au démarrage du process
Base.metadata.create_all(bind=engine)

# App FastAPI
app = FastAPI(
    title="API Users Management",
    description="API de gestion des utilisateurs avec JWT, SQLite et SQLAlchemy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=True
)

# CORS (origines autorisées) : lire depuis .env ou fallback à *
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
allow_origins = [o.strip() for o in CORS_ORIGINS.split(",")] if CORS_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swagger/ReDoc — déclare le schéma de sécurité JWT global
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Security scheme pour le Bearer token
    schema.setdefault("components", {}).setdefault("securitySchemes", {})["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    # Applique la sécurité par défaut (affichée dans la doc). Les endpoints publics restent publics.
    for path in schema.get("paths", {}).values():
        for op in path.values():
            op.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi

# Monter les routers
app.include_router(auth.router)    # /auth
app.include_router(users.router)   # /users

# Healthcheck simple
@app.get("/health")
def health():
    return {"status": "ok"}
