# WfL Dashboard Backend

FastAPI-Backend für den NiPoGi-Server von "Wir für Lukas". Das Projekt bündelt Projekt-, Termin-, Aufgaben- und Statusdaten für das interne Dashboard.

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

### Datenbank

Standardmäßig nutzt die App SQLite (`data.db` im Projektverzeichnis). Passe die `DATABASE_URL` in `.env` an, um PostgreSQL oder andere Backends zu verwenden.

```env
DATABASE_URL=sqlite:///./data.db
SECRET_KEY=please-change-me
```

Beim Start erzeugt die App automatisch alle Tabellen. Für Migrationen kann Alembic ergänzt werden.

### Kern-Endpunkte (`/api/...`)

- `POST /auth/login` – JWT anfordern
- `POST /auth/users` – Benutzer verwalten (Admin)
- `GET/POST/PUT /projects` – Projekte & Status
- `GET /projects/{project_id}/summary` – Task-Kennzahlen plus Events & News zu einem Projekt
- `GET/POST/PUT/DELETE /news` – Nachrichten mit Tags & Sichtbarkeit
- `GET/POST/PUT/DELETE /events` – Termine mit Raumbezug
- `GET/POST/PUT/DELETE /rooms` – Räume pflegen
- `GET/POST/PATCH /tasks` – Aufgaben und Zuständigkeiten
- `GET/POST/PATCH /metrics` – Kennzahlen pflegen
- `GET/POST/PATCH /system/status` – Dienstestatus
- `GET /status/summary` – Übersicht für das Dashboard (Projekte, Termine, News)
- `GET /users/me` – Eigenes Profil abrufen
- `PATCH /users/me/password` – Passwortänderung für eingeloggte Benutzer

## Weiteres

- Rollen: `admin`, `vorstand`, `team`, `mitarbeit`, `public`
- Authentifizierung via JWT; Passwörter werden mit bcrypt gehasht
- CORS ist aktuell offen (`*`); für Produktion anpassen
- Nachrichten-Endpunkt unterstützt optionale Filter `since` (ISO-Zeitstempel) und `limit` (max. 50 Einträge)
- Projekt-Summary liefert aggregierte Task-Counts, kommende Events und aktuelle News für Dashboards
- Tests decken Authentifizierungs- und CRUD-Flows exemplarisch ab (`tests/test_api.py`)

## Tests

```powershell
pytest
```
