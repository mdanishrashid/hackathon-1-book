from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://username:password@localhost:5432/textbook_db"
    
    # Authentication settings
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Qdrant settings
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    
    # API settings
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    
    # Logging settings
    log_level: str = "INFO"
    
    # Application settings
    app_name: str = "AI Textbook API"
    version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

def get_settings():
    """Function to get settings - useful for dependency injection"""
    return settings