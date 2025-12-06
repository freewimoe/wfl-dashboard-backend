# WfL Dashboard Backend

FastAPI-Backend für den NiPoGi-Server von "Wir für Lukas". Das Projekt liefert Status- und News-Endpunkte als Grundlage für das spätere Dashboard-Frontend.

## Voraussetzungen

- Python 3.10 oder neuer
- Optional: Ein virtuelles Environment (`python -m venv .venv`)

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Entwicklung

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Wichtige Endpunkte:

- `GET /status` – einfacher Health-Check
- `GET /news` – Beispiel-News-Einträge

## Nächste Schritte

- Routen um Authentifizierung und weitere Domain-Funktionen erweitern
- Datenhaltung (z. B. PostgreSQL, SQLite oder REST-Quellen) anbinden
- Frontend-Dashboard anbinden und CORS-Regeln einschränken
