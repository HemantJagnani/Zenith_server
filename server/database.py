from sqlalchemy import create_engine, Column, String, Integer, Float, TIMESTAMP, ARRAY, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic_settings import BaseSettings
from functools import lru_cache

# Settings
class Settings(BaseSettings):
    database_url: str
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env

@lru_cache()
def get_settings():
    return Settings()

# Database setup
settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
