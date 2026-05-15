from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# In production, you might want to adjust connect_args for PostgreSQL
connect_args = {"check_same_thread": False} if settings.sqlalchemy_database_url.startswith("sqlite") else {}

engine = create_engine(
    settings.sqlalchemy_database_url, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
