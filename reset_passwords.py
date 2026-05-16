import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app import models, auth

db = SessionLocal()

admin = db.query(models.User).filter(models.User.username == "admin").first()
member = db.query(models.User).filter(models.User.username == "member").first()

if admin:
    admin.hashed_password = auth.get_password_hash("admin123")
    ok = auth.verify_password("admin123", admin.hashed_password)
    print(f"admin password reset. Verify test: {ok}")

if member:
    member.hashed_password = auth.get_password_hash("member123")
    ok = auth.verify_password("member123", member.hashed_password)
    print(f"member password reset. Verify test: {ok}")

db.commit()
db.close()
print("Passwords reset successfully.")
