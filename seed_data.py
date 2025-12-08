import sys
import os
from datetime import datetime, timedelta

# Add current directory to path to allow imports from app
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.project import Project
from app.db.models.news import News
from app.db.models.event import Event
from app.db.models.room import Room
from app.db.models.task import Task
from app.db.models.system_status import SystemStatus
from app.core.security import get_password_hash

def seed():
    db = SessionLocal()
    
    try:
        # Check if data exists
        if db.query(User).first():
            print("Database already contains users. Clearing existing data to ensure clean state...")
            # Optional: Clear tables if you want a fresh start every time
            db.query(Task).delete()
            db.query(Event).delete()
            db.query(Room).delete()
            db.query(News).delete()
            db.query(Project).delete()
            db.query(SystemStatus).delete()
            db.query(User).delete()
            db.commit()
            # For now, let's just return if data exists to avoid duplicates
            # print("Skipping seed (Users found).")
            # return

        print("Creating Users...")
        admin = User(
            name="Admin User",
            email="admin@wfl.local",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        user1 = User(
            name="Sarah Meyer",
            email="sarah@wfl.local",
            password_hash=get_password_hash("user123"),
            role="team"
        )
        user2 = User(
            name="Jonas Müller",
            email="jonas@wfl.local",
            password_hash=get_password_hash("user123"),
            role="mitarbeit"
        )
        db.add_all([admin, user1, user2])
        db.commit()
        db.refresh(admin)
        db.refresh(user1)
        db.refresh(user2)

        print("Creating Projects...")
        p1 = Project(
            title="Digitalisierung Sportverein",
            description="Einführung einer neuen Vereinssoftware.",
            status="green",
            responsible_user_id=user1.id,
            created_at=datetime.utcnow() - timedelta(days=10)
        )
        p2 = Project(
            title="Sommerfest 2025",
            description="Planung des jährlichen Sommerfests.",
            status="yellow",
            responsible_user_id=user2.id,
            created_at=datetime.utcnow() - timedelta(days=5)
        )
        p3 = Project(
            title="Website Relaunch",
            description="Neugestaltung der Homepage.",
            status="red",
            responsible_user_id=admin.id,
            created_at=datetime.utcnow() - timedelta(days=20)
        )
        db.add_all([p1, p2, p3])
        db.commit()

        print("Creating News...")
        n1 = News(
            title="Pressekonferenz zur neuen Sozialberatung",
            body="Die Pressekonferenz war ein voller Erfolg.",
            author_id=admin.id,
            created_at=datetime.utcnow(),
            tags=["Öffentlich", "Presse"]
        )
        n2 = News(
            title="Raumplanung für Adventskonzert abgeschlossen",
            body="Alle Räume sind gebucht und bestätigt.",
            author_id=user1.id,
            created_at=datetime.utcnow() - timedelta(days=1),
            tags=["Intern", "Planung"]
        )
        n3 = News(
            title="Förderantrag „Sport für alle“ bewilligt",
            body="Wir haben die Zusage für die Fördermittel erhalten!",
            author_id=user2.id,
            created_at=datetime.utcnow() - timedelta(days=3),
            tags=["Vorstand", "Finanzen"]
        )
        db.add_all([n1, n2, n3])
        db.commit()

        print("Creating Rooms...")
        r1 = Room(name="Konferenzraum", description="Großer Besprechungsraum", capacity=20)
        r2 = Room(name="Raum A", description="Kleiner Gruppenraum", capacity=8)
        r3 = Room(name="Externe Termine", description="Platzhalter für externe Orte", capacity=0)
        db.add_all([r1, r2, r3])
        db.commit()
        db.refresh(r1)
        db.refresh(r2)
        db.refresh(r3)

        print("Creating Events...")
        e1 = Event(
            title="Team Jour Fixe",
            description="Wöchentliches Team-Meeting",
            start=datetime.utcnow() + timedelta(days=1, hours=9),
            end=datetime.utcnow() + timedelta(days=1, hours=10),
            room_id=r2.id,
            created_by=admin.id
        )
        e2 = Event(
            title="Koordination Ehrenamt",
            description="Treffen mit den Ehrenamtskoordinatoren",
            start=datetime.utcnow() + timedelta(days=1, hours=12),
            end=datetime.utcnow() + timedelta(days=1, hours=13, minutes=30),
            room_id=r1.id,
            created_by=user1.id
        )
        e3 = Event(
            title="Besuch im Rathaus",
            description="Gespräch mit dem Bürgermeister",
            start=datetime.utcnow() + timedelta(days=2, hours=10),
            end=datetime.utcnow() + timedelta(days=2, hours=11),
            room_id=r3.id,
            created_by=admin.id
        )
        db.add_all([e1, e2, e3])
        db.commit()

        print("Creating Tasks...")
        t1 = Task(
            title="Budgetbericht erstellen",
            description="Q4 Zahlen zusammenstellen",
            status="in_progress",
            project_id=p1.id,
            assignee_id=user1.id,
            created_by=admin.id,
            due_date=datetime.utcnow().date() + timedelta(days=2)
        )
        t2 = Task(
            title="Catering bestellen",
            description="Für das Sommerfest",
            status="open",
            project_id=p2.id,
            assignee_id=user2.id,
            created_by=user1.id,
            due_date=datetime.utcnow().date() + timedelta(days=14)
        )
        t3 = Task(
            title="Server Updates",
            description="Sicherheitsupdates einspielen",
            status="done",
            assignee_id=admin.id,
            created_by=admin.id,
            due_date=datetime.utcnow().date() - timedelta(days=1)
        )
        db.add_all([t1, t2, t3])
        db.commit()

        print("Creating System Status...")
        s1 = SystemStatus(service="Database", status="ok", message="Operational")
        s2 = SystemStatus(service="API Gateway", status="ok", message="Operational")
        s3 = SystemStatus(service="Email Service", status="ok", message="Operational")
        s4 = SystemStatus(service="Backup Job", status="warning", message="Last backup delayed")
        db.add_all([s1, s2, s3, s4])
        db.commit()

        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
