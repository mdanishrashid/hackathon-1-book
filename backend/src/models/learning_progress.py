from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)
    step_id = Column(PostgresUUID(as_uuid=True), ForeignKey("learning_steps.id"), nullable=False)
    status = Column(String, nullable=False, default="not_started")  # Enum: not_started, in_progress, completed, skipped
    completion_percentage = Column(Integer, default=0)  # 0-100
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    progress_data = Column(String)  # JSON data stored as string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("UserProfile", back_populates="progress")
    step = relationship("LearningStep", back_populates="progress")

    def __repr__(self):
        return f"<LearningProgress(id={self.id}, user_id={self.user_id}, step_id={self.step_id}, status={self.status})>"