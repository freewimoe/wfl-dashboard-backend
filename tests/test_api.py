"""Integration tests covering core API flows."""

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient


def authenticate(client: TestClient, email: str, password: str) -> str:
    """Return bearer token for given credentials."""

    response = client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return token


def test_full_domain_flow(client: TestClient, admin_credentials: dict[str, str]) -> None:
    """Exercise authentication and CRUD operations across core endpoints."""

    token = authenticate(client, admin_credentials["email"], admin_credentials["password"])
    auth_header = {"Authorization": f"Bearer {token}"}

    # Create a secondary user via admin endpoint
    user_payload = {
        "name": "Projektleiterin",
        "email": "lead@example.com",
        "password": "passwort123",
        "role": "team",
    }
    resp = client.post("/api/auth/users", json=user_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text
    lead_user = resp.json()

    # Create project
    project_payload = {
        "title": "Kulturprogramm 2026",
        "description": "Vorbereitung der Kulturveranstaltungen",
        "status": "green",
        "responsible_user_id": lead_user["id"],
    }
    resp = client.post("/api/projects", json=project_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text
    project = resp.json()

    # Create room
    room_payload = {"name": "Saal Lukas", "description": "Großer Saal", "capacity": 120}
    resp = client.post("/api/rooms", json=room_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text
    room = resp.json()

    # Create event referencing project and room
    start = datetime.now(timezone.utc) + timedelta(days=7)
    end = start + timedelta(hours=2)
    event_payload = {
        "title": "Jahresauftakt",
        "description": "Kick-off im Saal",
        "start": start.isoformat(),
        "end": end.isoformat(),
        "room_id": room["id"],
        "is_public": True,
        "project_id": project["id"],
    }
    resp = client.post("/api/events", json=event_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text

    # Create news entry tied to project
    news_payload = {
        "title": "Ticketverkauf gestartet",
        "body": "Ab sofort können Tickets reserviert werden.",
        "tags": ["kultur", "verkauf"],
        "is_public": True,
        "project_id": project["id"],
    }
    resp = client.post("/api/news", json=news_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text

    # Create metric
    metric_payload = {"name": "spenden_q1", "value": 12500.5}
    resp = client.post("/api/metrics", json=metric_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text

    # Create system status entry
    status_payload = {"service": "nextcloud", "status": "ok", "message": "Erreichbar"}
    resp = client.post("/api/system/status", json=status_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text

    # Create task assigned to lead user
    task_payload = {
        "title": "Budgetplanung",
        "description": "Vorlage für den Vorstand vorbereiten",
        "project_id": project["id"],
        "assignee_id": lead_user["id"],
        "status": "open",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=14)).date().isoformat(),
    }
    resp = client.post("/api/tasks", json=task_payload, headers=auth_header)
    assert resp.status_code == 201, resp.text

    # Verify summary endpoint aggregates data
    resp = client.get("/api/status/summary", headers=auth_header)
    assert resp.status_code == 200, resp.text
    payload = resp.json()
    assert any(item["id"] == project["id"] for item in payload["projects"])
    assert payload["upcoming_events"], "Expected at least one upcoming event"
    assert payload["recent_news"], "Expected at least one news entry"

    # Ensure tasks listing can be filtered by assignee
    resp = client.get(f"/api/tasks?assignee_id={lead_user['id']}", headers=auth_header)
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Budgetplanung"

    # Unauthorized access check: creating project without token should fail
    resp = client.post("/api/projects", json=project_payload)
    assert resp.status_code == 401
