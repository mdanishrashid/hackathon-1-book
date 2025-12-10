from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    path_type = Column(String, nullable=False, default="default")  # Enum: default, personalized, remedial
    steps_sequence = Column(String, nullable=False)  # JSON data stored as string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("UserProfile", back_populates="learning_paths")

    def __repr__(self):
        return f"<LearningPath(id={self.id}, name={self.name}, user_id={self.user_id})>"