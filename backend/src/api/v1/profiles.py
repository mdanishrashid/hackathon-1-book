from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from ...database import get_db
from ...models.user_profile import UserProfile
from ...api.v1.auth import get_current_active_user, User

router = APIRouter()

class UserProfileUpdate(BaseModel):
    background_level: Optional[str] = None  # beginner, intermediate, advanced
    preferred_language: Optional[str] = None
    learning_preferences: Optional[str] = None  # JSON string

@router.get("/me", response_model=UserProfile)
def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get the authenticated user's profile information"""
    # In a real implementation, the current_user.id would map to the UserProfile auth_id
    # For now, we'll search by username as a placeholder
    profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not profile:
        # Create a default profile if one doesn't exist
        profile = UserProfile(
            auth_id=current_user.username,
            background_level="beginner",
            preferred_language="en"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile

@router.put("/me", response_model=UserProfile)
def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update the authenticated user's profile information"""
    profile = db.query(UserProfile).filter(UserProfile.auth_id == current_user.username).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    # Update fields if provided
    if profile_update.background_level is not None:
        profile.background_level = profile_update.background_level
    if profile_update.preferred_language is not None:
        profile.preferred_language = profile_update.preferred_language
    if profile_update.learning_preferences is not None:
        profile.learning_preferences = profile_update.learning_preferences

    db.commit()
    db.refresh(profile)

    return profile