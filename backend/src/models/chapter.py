from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)
    prerequisite_chapter_id = Column(PostgresUUID(as_uuid=True), ForeignKey("chapters.id"))  # Self-referencing
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to learning steps
    steps = relationship("LearningStep", back_populates="chapter", order_by="LearningStep.order_index")

    def __repr__(self):
        return f"<Chapter(id={self.id}, title={self.title})>"