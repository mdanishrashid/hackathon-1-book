from typing import Optional
from sqlalchemy.orm import Session
from ..models.user_profile import UserProfile

class UserService:
    @staticmethod
    def get_user_profile_by_auth_id(db: Session, auth_id: str) -> Optional[UserProfile]:
        """Retrieve a user profile by its auth ID"""
        return db.query(UserProfile).filter(UserProfile.auth_id == auth_id).first()

    @staticmethod
    def create_user_profile(db: Session, auth_id: str, background_level: str = "beginner", 
                           preferred_language: str = "en", learning_preferences: Optional[str] = None) -> UserProfile:
        """Create a new user profile"""
        profile = UserProfile(
            auth_id=auth_id,
            background_level=background_level,
            preferred_language=preferred_language,
            learning_preferences=learning_preferences
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update_user_profile(db: Session, auth_id: str, **kwargs) -> Optional[UserProfile]:
        """Update user profile with provided fields"""
        profile = db.query(UserProfile).filter(UserProfile.auth_id == auth_id).first()
        if profile:
            for key, value in kwargs.items():
                if hasattr(profile, key) and value is not None:
                    setattr(profile, key, value)
            db.commit()
            db.refresh(profile)
        return profile

    @staticmethod
    def get_or_create_user_profile(db: Session, auth_id: str, **defaults) -> UserProfile:
        """Get user profile or create with defaults if it doesn't exist"""
        profile = UserService.get_user_profile_by_auth_id(db, auth_id)
        if not profile:
            profile = UserService.create_user_profile(db, auth_id, **defaults)
        return profile