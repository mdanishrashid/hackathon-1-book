from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json
from ...database import get_db
from ...models.learning_path import LearningPath
from ...models.user_profile import UserProfile
from ...services.personalization_service import PersonalizationService
from ...api.v1.auth import get_current_active_user, User

router = APIRouter()

class LearningPathCreate(BaseModel):
    name: str
    description: Optional[str] = None
    path_type: str = "default"  # default, personalized, remedial
    steps_sequence: List[str]  # List of step IDs in order

class LearningPathUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    path_type: Optional[str] = None

@router.get("/", response_model=List[LearningPath])
def get_user_learning_paths(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all learning paths for the authenticated user"""
    # Find the user profile first to get the user UUID
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        # If no profile exists, return empty list
        return []

    paths = db.query(LearningPath).filter(LearningPath.user_id == user_profile.id).all()
    return paths

@router.get("/{path_id}", response_model=LearningPath)
def get_learning_path(
    path_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific learning path by ID"""
    # Find the user profile first
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == user_profile.id
    ).first()

    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )

    return path

@router.post("/", response_model=LearningPath)
def create_learning_path(
    learning_path_data: LearningPathCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new learning path for the authenticated user"""
    # Find the user profile first
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    # Create the learning path
    learning_path = PersonalizationService.create_personalized_learning_path(
        db,
        user_profile.id,
        learning_path_data.name,
        learning_path_data.description or "",
        learning_path_data.steps_sequence,
        learning_path_data.path_type
    )

    return learning_path

@router.put("/{path_id}", response_model=LearningPath)
def update_learning_path(
    path_id: str,
    learning_path_data: LearningPathUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an existing learning path"""
    # Find the user profile first
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == user_profile.id
    ).first()

    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )

    # Update fields
    if learning_path_data.name is not None:
        path.name = learning_path_data.name
    if learning_path_data.description is not None:
        path.description = learning_path_data.description
    if learning_path_data.path_type is not None:
        path.path_type = learning_path_data.path_type

    db.commit()
    db.refresh(path)

    return path

@router.delete("/{path_id}")
def delete_learning_path(
    path_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a learning path"""
    # Find the user profile first
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == user_profile.id
    ).first()

    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )

    db.delete(path)
    db.commit()

    return {"message": "Learning path deleted successfully"}

@router.get("/adaptive/{chapter_id}", response_model=dict)
def get_adaptive_learning_path(
    chapter_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get an adaptive learning path for the user based on their profile and the chapter"""
    # Find the user profile first
    user_profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    # Get the learning path for the user in this chapter
    learning_path = PersonalizationService.get_learning_path_for_user(db, user_profile.id)

    # If no specific path exists for this user, create an adaptive path based on their background
    if not learning_path:
        # For now, we'll return a basic response with the user's background level
        # In a real system, we would generate an adaptive path based on user profile
        return {
            "chapter_id": chapter_id,
            "user_background": user_profile.background_level,
            "message": f"Using adaptive learning approach based on your background level: {user_profile.background_level}",
            "recommended_steps_count": 0  # Placeholder for actual logic
        }

    return {
        "path_id": learning_path.id,
        "path_name": learning_path.name,
        "path_type": learning_path.path_type,
        "steps_sequence": json.loads(learning_path.steps_sequence) if learning_path.steps_sequence else [],
        "user_background": user_profile.background_level
    }