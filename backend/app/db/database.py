from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import os
from typing import Generator

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/hotel_pms"
)

# Render'da DATABASE_URL otomatik olarak sağlanır
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Render'da bağlantı havuzu sorunları için
    echo=False,  # SQL sorgularını yazdırmak için True yapabilirsiniz
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """FastAPI'de veritabanı oturumu sağla"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
