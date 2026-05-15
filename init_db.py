import os
import sys

# Add current directory to path so it can find 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app import models, auth

def init():
    # Ensure tables are created
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    admin = db.query(models.User).filter(models.User.username == "admin").first()
    if not admin:
        admin = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=auth.get_password_hash("admin123"),
            role=models.Role.ADMIN
        )
        db.add(admin)
        
        member = models.User(
            username="member",
            email="member@example.com",
            hashed_password=auth.get_password_hash("member123"),
            role=models.Role.MEMBER
        )
        db.add(member)
        
        # Add a sample project
        project = models.Project(
            name="Alpha Build",
            description="First version of the application."
        )
        db.add(project)
        
        db.commit()
        db.refresh(project)
        
        # Add a sample task
        task = models.Task(
            title="Design Database Schema",
            description="Create the models for the app.",
            project_id=project.id,
            assigned_to_id=admin.id,
            status=models.TaskStatus.DONE
        )
        db.add(task)
        db.commit()
        
        print("Database initialized successfully with test users:")
        print("  Admin: admin / admin123")
        print("  Member: member / member123")
    else:
        print("Database already initialized.")
    
    db.close()

if __name__ == "__main__":
    init()
