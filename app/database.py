from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para pegar a sessão do banco na FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()