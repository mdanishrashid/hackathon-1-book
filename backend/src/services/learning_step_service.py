from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.learning_step import LearningStep
from ..models.chapter import Chapter
from ..services.personalization_service import PersonalizationService
from ..models.user_profile import UserProfile

class LearningStepService:
    @staticmethod
    def get_step_by_id(db: Session, step_id: str) -> Optional[LearningStep]:
        """Retrieve a specific learning step by ID"""
        return db.query(LearningStep).filter(LearningStep.id == step_id).first()

    @staticmethod
    def get_steps_by_chapter(db: Session, chapter_id: str) -> List[LearningStep]:
        """Retrieve all steps for a specific chapter, ordered by sequence"""
        return db.query(LearningStep) \
                 .filter(LearningStep.chapter_id == chapter_id) \
                 .order_by(LearningStep.order_index).all()

    @staticmethod
    def get_adaptive_steps_by_chapter(db: Session, chapter_id: str, user_id: str) -> List[LearningStep]:
        """Retrieve personalized steps for a specific chapter based on user profile"""
        return PersonalizationService.get_adaptive_steps_for_user(db, chapter_id, user_id)

    @staticmethod
    def get_next_step(db: Session, current_step_id: str) -> Optional[LearningStep]:
        """Get the next step in the sequence after the current step"""
        current_step = db.query(LearningStep).filter(LearningStep.id == current_step_id).first()
        if not current_step:
            return None

        # Find the next step in the same chapter with the next order_index
        next_step = db.query(LearningStep) \
                      .filter(LearningStep.chapter_id == current_step.chapter_id) \
                      .filter(LearningStep.order_index > current_step.order_index) \
                      .order_by(LearningStep.order_index).first()

        return next_step

    @staticmethod
    def get_prev_step(db: Session, current_step_id: str) -> Optional[LearningStep]:
        """Get the previous step in the sequence before the current step"""
        current_step = db.query(LearningStep).filter(LearningStep.id == current_step_id).first()
        if not current_step:
            return None

        # Find the previous step in the same chapter with the previous order_index
        prev_step = db.query(LearningStep) \
                      .filter(LearningStep.chapter_id == current_step.chapter_id) \
                      .filter(LearningStep.order_index < current_step.order_index) \
                      .order_by(LearningStep.order_index.desc()).first()

        return prev_step

    @staticmethod
    def get_first_step_of_chapter(db: Session, chapter_id: str) -> Optional[LearningStep]:
        """Get the first step in a chapter"""
        return db.query(LearningStep) \
                 .filter(LearningStep.chapter_id == chapter_id) \
                 .order_by(LearningStep.order_index).first()

    @staticmethod
    def get_first_adaptive_step_of_chapter(db: Session, chapter_id: str, user_id: str) -> Optional[LearningStep]:
        """Get the first step in a chapter, potentially personalized for the user"""
        steps = LearningStepService.get_adaptive_steps_by_chapter(db, chapter_id, user_id)
        return steps[0] if steps else None

    @staticmethod
    def create_step(db: Session, step_data: dict) -> LearningStep:
        """Create a new learning step"""
        step = LearningStep(**step_data)
        db.add(step)
        db.commit()
        db.refresh(step)
        return step

    @staticmethod
    def update_step(db: Session, step_id: str, step_data: dict) -> Optional[LearningStep]:
        """Update an existing learning step"""
        step = db.query(LearningStep).filter(LearningStep.id == step_id).first()
        if step:
            for key, value in step_data.items():
                setattr(step, key, value)
            db.commit()
            db.refresh(step)
        return step

    @staticmethod
    def delete_step(db: Session, step_id: str) -> bool:
        """Delete a learning step"""
        step = db.query(LearningStep).filter(LearningStep.id == step_id).first()
        if step:
            db.delete(step)
            db.commit()
            return True
        return False