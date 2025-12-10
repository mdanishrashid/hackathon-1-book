from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.chapter import Chapter
from ..models.learning_step import LearningStep

class ChapterService:
    @staticmethod
    def get_all_chapters(db: Session) -> List[Chapter]:
        """Retrieve all chapters with their steps"""
        return db.query(Chapter).order_by(Chapter.order_index).all()

    @staticmethod
    def get_chapter_by_id(db: Session, chapter_id: str) -> Optional[Chapter]:
        """Retrieve a specific chapter by ID with its steps"""
        return db.query(Chapter).filter(Chapter.id == chapter_id).first()

    @staticmethod
    def get_chapter_with_steps(db: Session, chapter_id: str) -> Optional[Chapter]:
        """Retrieve a chapter with its associated steps"""
        return db.query(Chapter).filter(Chapter.id == chapter_id).first()

    @staticmethod
    def create_chapter(db: Session, chapter_data: dict) -> Chapter:
        """Create a new chapter"""
        chapter = Chapter(**chapter_data)
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
        return chapter

    @staticmethod
    def update_chapter(db: Session, chapter_id: str, chapter_data: dict) -> Optional[Chapter]:
        """Update an existing chapter"""
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if chapter:
            for key, value in chapter_data.items():
                setattr(chapter, key, value)
            db.commit()
            db.refresh(chapter)
        return chapter

    @staticmethod
    def delete_chapter(db: Session, chapter_id: str) -> bool:
        """Delete a chapter"""
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if chapter:
            db.delete(chapter)
            db.commit()
            return True
        return False