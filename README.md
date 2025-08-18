🚀 API Users Management — FastAPI
API REST complète de gestion des utilisateurs construite avec FastAPI, JWT, SQLAlchemy et SQLite.
Elle permet l'inscription, la connexion sécurisée, la gestion des profils utilisateurs, avec un système de rôles (user / admin) et une documentation interactive (Swagger et ReDoc).

📌 Sommaire
Fonctionnalités

Architecture du projet

Technologies

Installation

Configuration

Lancement

Endpoints API

Exemples d’utilisation

Tests

✨ Fonctionnalités
Inscription d’utilisateurs (/auth/register)

Connexion avec génération d’un JWT

Profil (/auth/me) avec authentification

Gestion complète des utilisateurs :

Listing avec pagination et recherche

Consultation par ID

Modification (email, mot de passe, rôle)

Suppression (désactivation)

Rôles et permissions :

user : peut voir et modifier son propre profil

admin : peut gérer tous les utilisateurs

Documentation interactive via Swagger et ReDoc

Sécurité avec mot de passe hashé (bcrypt) + JWT

📂 Architecture du projet
graphql
Copier
Modifier
python-api-users-management/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # Point d'entrée FastAPI
│   ├── db.py            # Connexion DB et session
│   ├── deps.py          # Dépendances (auth)
│   ├── core/            # Fonctions de sécurité (JWT, hash)
│   ├── models/          # Modèles SQLAlchemy (User)
│   ├── schemas/         # Schémas Pydantic
│   └── routes/          # Routes API (auth, users)
│
├── tests/               # Tests pytest
├── .env.example         # Variables d'environnement exemple
├── .gitignore           # Fichiers ignorés par Git
├── requirements.txt     # Dépendances Python
└── start_api.ps1        # Script PowerShell pour démarrer l’API
🧱 Technologies
FastAPI : Framework Python moderne

SQLAlchemy : ORM

Pydantic v2 : Validation des données

SQLite : Base de données légère

python-jose : Gestion JWT

passlib : Hash des mots de passe

pytest : Tests automatisés

⚙ Installation
bash
Copier
Modifier
# 1. Cloner le repo
git clone https://github.com/madjiddev/python-api-users-management.git
cd python-api-users-management

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
🔧 Configuration
Copier le fichier .env.example en .env

bash
Copier
Modifier
cp .env.example .env
Modifier .env selon vos besoins :

env
Copier
Modifier
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=une_chaine_ultra_secrete
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000
▶ Lancement
bash
Copier
Modifier
uvicorn app.main:app --reload
Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

📡 Endpoints API
Méthode	URL	Auth requise	Description
POST	/auth/register	❌	Inscription
POST	/auth/login	❌	Connexion JWT
GET	/auth/me	✅	Profil connecté
GET	/users/	✅	Liste utilisateurs
GET	/users/{id}	✅	Détail utilisateur
PUT	/users/{id}	✅	Modifier utilisateur
DELETE	/users/{id}	✅	Désactiver utilisateur

📌 Exemples d’utilisation
1️⃣ Inscription
bash
Copier
Modifier
curl -X POST http://127.0.0.1:8000/auth/register \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"motdepasse123"}'
2️⃣ Connexion
bash
Copier
Modifier
curl -X POST http://127.0.0.1:8000/auth/login \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=test@example.com&password=motdepasse123"
Réponse :

json
Copier
Modifier
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
3️⃣ Profil connecté
bash
Copier
Modifier
curl -X GET http://127.0.0.1:8000/auth/me \
-H "Authorization: Bearer VOTRE_TOKEN"
🧪 Tests
bash
Copier
Modifier
pytest -q
✅ Teste inscription, connexion, accès protégé, et listing utilisateurs.
