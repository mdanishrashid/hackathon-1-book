from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id = Column(String, unique=True, nullable=False)  # Foreign Key to Better-Auth user
    background_level = Column(String, nullable=False, default="beginner")  # Enum: beginner, intermediate, advanced
    preferred_language = Column(String, nullable=False, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    learning_preferences = Column(String)  # JSON data stored as string

    # Relationship to learning progress
    progress = relationship("LearningProgress", back_populates="user")
    learning_paths = relationship("LearningPath", back_populates="user")

    def __repr__(self):
        return f"<UserProfile(id={self.id}, auth_id={self.auth_id})>"