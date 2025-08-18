# Active l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Lance l'API en mode auto-reload
uvicorn app.main:app --reload
