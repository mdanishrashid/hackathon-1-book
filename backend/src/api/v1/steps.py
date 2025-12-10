from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ...models.learning_step import LearningStep
from ...services.learning_step_service import LearningStepService
from ...api.v1.auth import get_current_active_user, User

router = APIRouter()

@router.get("/{step_id}", response_model=LearningStep)
def get_step_by_id(step_id: str, db: Session = Depends(get_db)):
    """Get details of a specific learning step"""
    step = LearningStepService.get_step_by_id(db, step_id)
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Learning step with ID {step_id} not found"
        )
    return step

@router.get("/chapter/{chapter_id}", response_model=List[LearningStep])
def get_steps_by_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """Get all steps for a specific chapter, in order"""
    steps = LearningStepService.get_steps_by_chapter(db, chapter_id)
    return steps

@router.get("/chapter/{chapter_id}/adaptive", response_model=List[LearningStep])
def get_adaptive_steps_by_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized steps for a chapter based on user profile"""
    # Find the user profile to get the UUID
    from ...models.user_profile import UserProfile
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    # Get adaptive steps based on user profile
    steps = LearningStepService.get_adaptive_steps_by_chapter(db, chapter_id, user_profile.id)
    return steps

@router.get("/{step_id}/next", response_model=Optional[LearningStep])
def get_next_step(step_id: str, db: Session = Depends(get_db)):
    """Get the next step in the sequence after the specified step"""
    next_step = LearningStepService.get_next_step(db, step_id)
    return next_step

@router.get("/{step_id}/previous", response_model=Optional[LearningStep])
def get_prev_step(step_id: str, db: Session = Depends(get_db)):
    """Get the previous step in the sequence before the specified step"""
    prev_step = LearningStepService.get_prev_step(db, step_id)
    return prev_step

@router.get("/chapter/{chapter_id}/first", response_model=Optional[LearningStep])
def get_first_step_of_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get the first step of a chapter, potentially personalized for the user"""
    from ...models.user_profile import UserProfile
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        # If no profile exists, return the standard first step
        return LearningStepService.get_first_step_of_chapter(db, chapter_id)

    # Get personalized first step based on user profile
    step = LearningStepService.get_first_adaptive_step_of_chapter(db, chapter_id, user_profile.id)
    return step