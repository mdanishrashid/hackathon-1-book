from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...database import get_db
from ...models.learning_progress import LearningProgress
from ...services.progress_service import ProgressService
from ...services.learning_step_service import LearningStepService
from ...api.v1.auth import get_current_active_user, User

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
def get_user_overall_progress(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's overall progress across all chapters and steps"""
    # Using the enhanced progress calculation from ProgressService
    overall_progress = ProgressService.get_user_overall_progress(db, current_user.id)
    return overall_progress

@router.get("/chapters/{chapter_id}", response_model=Dict[str, Any])
def get_user_chapter_progress(
    chapter_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's progress for a specific chapter"""
    chapter_progress = ProgressService.get_user_chapter_progress(db, current_user.id, chapter_id)
    return chapter_progress

@router.get("/steps/{step_id}", response_model=LearningProgress)
def get_progress_for_step(
    step_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get progress for a specific step"""
    progress = ProgressService.get_progress_for_step(db, current_user.id, step_id)
    if not progress:
        # If no progress exists, return a default not_started record
        step = LearningStepService.get_step_by_id(db, step_id)
        if not step:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Step with ID {step_id} not found"
            )

        # Create a default progress record if it doesn't exist
        progress = LearningProgress(
            user_id=current_user.id,
            step_id=step_id,
            status="not_started",
            completion_percentage=0
        )
        return progress

    return progress

@router.post("/steps/{step_id}/complete", response_model=LearningProgress)
def mark_step_complete(
    step_id: str,
    validation_data: Dict[str, Any] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a step as completed after validation"""
    # In a real implementation, you would validate the validation_data
    # to ensure the user has completed the required tasks for the step
    # For now, we'll just accept the completion request

    step = LearningStepService.get_step_by_id(db, step_id)
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Step with ID {step_id} not found"
        )

    # Check if user can access this step (based on prerequisite completion)
    if step.prerequisite_step_id:
        prereq_progress = ProgressService.get_progress_for_step(db, current_user.id, step.prerequisite_step_id)
        if not prereq_progress or prereq_progress.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access this step until prerequisite is completed"
            )

    # Mark the step as completed
    progress = ProgressService.mark_step_completed(db, current_user.id, step_id, validation_data)
    return progress

@router.put("/steps/{step_id}/reset", response_model=LearningProgress)
def reset_step_progress(
    step_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reset the progress for a specific step"""
    progress = ProgressService.record_step_progress(db, current_user.id, step_id, "not_started", 0)
    return progress