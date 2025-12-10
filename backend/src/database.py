from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings  # Import from the config module

# Create engine with connection pooling settings
engine = create_engine(
    settings.database_url,
    pool_size=10,  # Number of connection objects to maintain in the pool
    max_overflow=20,  # Additional connections beyond pool_size when needed
    pool_pre_ping=True,  # Validates connections before using them
    pool_recycle=300,  # Recycle connections after 5 minutes
    echo=False  # Set to True to log SQL queries (useful for debugging)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function that provides database sessions.
    Use this function as a dependency in your API endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()