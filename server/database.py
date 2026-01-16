from sqlalchemy import create_engine, Column, String, Integer, Float, TIMESTAMP, ARRAY, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

# Global flag to track database availability
db_available = False

# Settings
class Settings(BaseSettings):
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env

@lru_cache()
def get_settings():
    return Settings()

# Database setup
settings = get_settings()

# Initialize engine and session factory
engine = None
SessionLocal = None

if settings.database_url:
    try:
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # db_available will be set to True in init_db() after tables are created
    except Exception as e:
        print(f"⚠️ Failed to create database engine: {e}")
else:
    print("⚠️ No DATABASE_URL found. Running in no-database mode.")

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    picture_url = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    last_login = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, index=True)
    duration = Column(Integer)  # in seconds
    topic = Column(String(100))
    transcript = Column(Text)
    score = Column(Float)
    strengths = Column(ARRAY(Text))
    weaknesses = Column(ARRAY(Text))
    suggestions = Column(ARRAY(Text))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

# Database dependency
def get_db():
    if not db_available or SessionLocal is None:
        try:
            yield None
        finally:
            pass
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def init_db():
    """Initialize database tables"""
    global db_available
    if engine is None:
        db_available = False
        print("⚠️ No database engine configured. Running without persistent storage.")
        return

    try:
        Base.metadata.create_all(bind=engine)
        db_available = True
        print("✅ Database initialized")
    except Exception as e:
        db_available = False
        print(f"⚠️ Database initialization failed: {e}")
        print("⚠️ Running without database - OAuth will work but data won't persist")
