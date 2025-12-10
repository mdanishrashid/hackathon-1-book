from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.learning_progress import LearningProgress
from ..models.learning_step import LearningStep
from ..models.chapter import Chapter
from ..services.learning_step_service import LearningStepService

class ProgressValidationException(Exception):
    """Exception raised when step completion validation fails"""
    pass

class ProgressService:
    @staticmethod
    def get_user_progress(db: Session, user_id: str) -> List[LearningProgress]:
        """Get all progress records for a specific user"""
        return db.query(LearningProgress).filter(LearningProgress.user_id == user_id).all()

    @staticmethod
    def get_progress_for_step(db: Session, user_id: str, step_id: str) -> Optional[LearningProgress]:
        """Get progress for a specific user and step"""
        return db.query(LearningProgress) \
                 .filter(LearningProgress.user_id == user_id) \
                 .filter(LearningProgress.step_id == step_id) \
                 .first()

    @staticmethod
    def get_progress_for_chapter(db: Session, user_id: str, chapter_id: str) -> List[LearningProgress]:
        """Get progress for all steps in a specific chapter for a user"""
        return db.query(LearningProgress) \
                 .join(LearningStep, LearningProgress.step_id == LearningStep.id) \
                 .filter(LearningProgress.user_id == user_id) \
                 .filter(LearningStep.chapter_id == chapter_id) \
                 .all()

    @staticmethod
    def validate_step_completion(db: Session, user_id: str, step_id: str, validation_data: Optional[dict] = None) -> bool:
        """Validate if a user can complete a specific step"""
        import json

        step = LearningStepService.get_step_by_id(db, step_id)
        if not step:
            raise ProgressValidationException(f"Step with ID {step_id} does not exist")

        # Check if user has completed the prerequisite step (if any)
        if step.prerequisite_step_id:
            prereq_progress = ProgressService.get_progress_for_step(db, user_id, step.prerequisite_step_id)
            if not prereq_progress or prereq_progress.status != "completed":
                raise ProgressValidationException(
                    f"Cannot complete step {step_id} until prerequisite step {step.prerequisite_step_id} is completed"
                )

        # Validate based on required completion criteria
        # In the future, this could include specific checks based on step type and criteria
        required_criteria = {}
        if step.required_completion_criteria:
            try:
                required_criteria = json.loads(step.required_completion_criteria)
            except json.JSONDecodeError:
                # If JSON parsing fails, we might want to handle this differently
                # For now, just continue with empty dict
                pass

        # For now, just checking if the step has time-based requirements
        if required_criteria.get("type") == "time" and required_criteria.get("value"):
            # If validation_data includes time spent, check if sufficient
            time_spent = validation_data.get("time_spent") if validation_data else 0
            if time_spent and time_spent < required_criteria["value"]:
                raise ProgressValidationException(
                    f"Insufficient time spent on step. Required: {required_criteria['value']} seconds, Actual: {time_spent} seconds"
                )

        return True  # Validation passed

    @staticmethod
    def record_step_progress(db: Session, user_id: str, step_id: str, status: str,
                           completion_percentage: int = 0, progress_data: Optional[dict] = None) -> LearningProgress:
        """Record or update progress for a specific user and step"""
        progress = ProgressService.get_progress_for_step(db, user_id, step_id)

        if progress:
            # Update existing progress
            progress.status = status
            progress.completion_percentage = completion_percentage
            progress.progress_data = str(progress_data) if progress_data else None

            if status == "completed" and not progress.completed_at:
                progress.completed_at = datetime.utcnow()
            elif status != "completed":
                progress.completed_at = None

            progress.updated_at = datetime.utcnow()
        else:
            # Create new progress record
            progress_data_str = str(progress_data) if progress_data else None
            progress = LearningProgress(
                user_id=user_id,
                step_id=step_id,
                status=status,
                completion_percentage=completion_percentage,
                progress_data=progress_data_str
            )
            if status == "completed":
                progress.completed_at = datetime.utcnow()
            db.add(progress)

        db.commit()
        db.refresh(progress)
        return progress

    @staticmethod
    def mark_step_completed(db: Session, user_id: str, step_id: str, progress_data: Optional[dict] = None) -> LearningProgress:
        """Mark a specific step as completed for a user after validation"""
        # First validate if the step can be completed
        ProgressService.validate_step_completion(db, user_id, step_id, progress_data)

        return ProgressService.record_step_progress(
            db, user_id, step_id, "completed",
            completion_percentage=100, progress_data=progress_data
        )

    @staticmethod
    def mark_step_in_progress(db: Session, user_id: str, step_id: str,
                            completion_percentage: int = 0, progress_data: Optional[dict] = None) -> LearningProgress:
        """Mark a specific step as in progress for a user"""
        return ProgressService.record_step_progress(
            db, user_id, step_id, "in_progress",
            completion_percentage=completion_percentage, progress_data=progress_data
        )

    @staticmethod
    def can_access_next_step(db: Session, user_id: str, current_step_id: str) -> bool:
        """Check if user can access the next step based on completion of current step"""
        # Get the current step's progress
        current_progress = ProgressService.get_progress_for_step(db, user_id, current_step_id)

        # User can proceed if the current step is completed
        return current_progress and current_progress.status == "completed"

    @staticmethod
    def get_next_step_for_user(db: Session, user_id: str, current_step_id: str) -> Optional[LearningStep]:
        """Get the next step user should access based on progression rules"""
        # First check if user can proceed to next step in sequence
        if ProgressService.can_access_next_step(db, user_id, current_step_id):
            # Get next step in the same chapter
            next_step = LearningStepService.get_next_step(db, current_step_id)
            return next_step

        # If current step is not completed, return current step
        return LearningStepService.get_step_by_id(db, current_step_id)

    @staticmethod
    def get_user_chapter_progress(db: Session, user_id: str, chapter_id: str) -> dict:
        """Get overall progress summary for a chapter for a user"""
        all_steps = LearningStepService.get_steps_by_chapter(db, chapter_id)
        user_progress = ProgressService.get_progress_for_chapter(db, user_id, chapter_id)

        # Create a mapping of step_id to progress for quick lookup
        progress_map = {p.step_id: p for p in user_progress}

        completed_steps = 0
        in_progress_steps = 0
        total_steps = len(all_steps)

        for step in all_steps:
            step_progress = progress_map.get(step.id)
            if step_progress and step_progress.status == "completed":
                completed_steps += 1
            elif step_progress and step_progress.status == "in_progress":
                in_progress_steps += 1

        return {
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "in_progress_steps": in_progress_steps,
            "not_started_steps": total_steps - completed_steps - in_progress_steps,
            "completion_percentage": round((completed_steps / total_steps * 100) if total_steps > 0 else 0, 2),
            "steps": [
                {
                    "step_id": step.id,
                    "step_title": step.title,
                    "order_index": step.order_index,
                    "status": progress_map.get(step.id, LearningProgress(status="not_started")).status,
                    "completion_percentage": progress_map.get(step.id, LearningProgress(completion_percentage=0)).completion_percentage
                }
                for step in all_steps
            ]
        }

    @staticmethod
    def get_user_overall_progress(db: Session, user_id: str) -> dict:
        """Get overall progress summary across all chapters for a user"""
        from ..services.chapter_service import ChapterService

        # Get all chapters
        all_chapters = ChapterService.get_all_chapters(db)

        # Calculate overall progress across all chapters
        total_steps = 0
        completed_steps = 0
        in_progress_steps = 0

        chapter_progress = []

        for chapter in all_chapters:
            chapter_prog = ProgressService.get_user_chapter_progress(db, user_id, chapter.id)

            total_steps += chapter_prog["total_steps"]
            completed_steps += chapter_prog["completed_steps"]
            in_progress_steps += chapter_prog["in_progress_steps"]

            chapter_progress.append({
                "chapter_id": chapter.id,
                "chapter_title": chapter.title,
                "total_steps": chapter_prog["total_steps"],
                "completed_steps": chapter_prog["completed_steps"],
                "in_progress_steps": chapter_prog["in_progress_steps"],
                "completion_percentage": chapter_prog["completion_percentage"]
            })

        overall_completion_percentage = round((completed_steps / total_steps * 100) if total_steps > 0 else 0, 2)

        return {
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "in_progress_steps": in_progress_steps,
            "not_started_steps": total_steps - completed_steps - in_progress_steps,
            "overall_completion_percentage": overall_completion_percentage,
            "chapters": chapter_progress
        }