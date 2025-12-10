from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class LearningStep(Base):
    __tablename__ = "learning_steps"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(PostgresUUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    step_type = Column(String, nullable=False)  # Enum: reading, quiz, exercise, video, interactive
    order_index = Column(Integer, nullable=False)
    prerequisite_step_id = Column(PostgresUUID(as_uuid=True), ForeignKey("learning_steps.id"))  # Self-referencing
    required_completion_criteria = Column(String, nullable=False)  # JSON data stored as string, default: {"type": "time", "value": 60}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chapter = relationship("Chapter", back_populates="steps")
    progress = relationship("LearningProgress", back_populates="step")

    def __repr__(self):
        return f"<LearningStep(id={self.id}, title={self.title}, chapter_id={self.chapter_id})>"