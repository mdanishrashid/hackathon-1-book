import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.learning_step import LearningStep
from ..models.learning_path import LearningPath
from ..models.user_profile import UserProfile
from ..models.chapter import Chapter

class PersonalizationService:
    @staticmethod
    def get_learning_path_for_user(db: Session, user_id: str) -> Optional[LearningPath]:
        """Get the personalized learning path for a user, or create a default one"""
        # First try to get a specific learning path for this user
        learning_path = db.query(LearningPath) \
                         .filter(LearningPath.user_id == user_id) \
                         .order_by(LearningPath.created_at.desc()).first()

        return learning_path

    @staticmethod
    def create_personalized_learning_path(db: Session, user_id: str, path_name: str,
                                        path_description: str, steps_sequence: List[str],
                                        path_type: str = "personalized") -> LearningPath:
        """Create a new personalized learning path for a user"""
        learning_path = LearningPath(
            user_id=user_id,
            name=path_name,
            description=path_description,
            path_type=path_type,
            steps_sequence=json.dumps(steps_sequence)  # Store as JSON string
        )
        db.add(learning_path)
        db.commit()
        db.refresh(learning_path)
        return learning_path

    @staticmethod
    def customize_steps_by_user_background(db: Session, chapter_id: str, user_profile: UserProfile) -> List[LearningStep]:
        """Customize the learning steps based on user's background level"""
        # Get all steps for the chapter
        all_steps = db.query(LearningStep) \
                     .filter(LearningStep.chapter_id == chapter_id) \
                     .order_by(LearningStep.order_index).all()

        background_level = user_profile.background_level

        # Apply personalization based on background level
        if background_level == "advanced":
            # For advanced users, potentially skip some introductory steps
            # or provide more advanced content
            return all_steps
        elif background_level == "intermediate":
            # For intermediate users, provide standard path but with some customization
            return all_steps
        else:  # beginner
            # For beginners, ensure all steps are included in full detail
            return all_steps

    @staticmethod
    def get_adaptive_steps_for_user(db: Session, chapter_id: str, user_id: str) -> List[LearningStep]:
        """Get steps that are personalized for a specific user in a chapter"""
        # Get user profile
        user_profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        if not user_profile:
            # If no profile exists, return default steps
            return db.query(LearningStep) \
                     .filter(LearningStep.chapter_id == chapter_id) \
                     .order_by(LearningStep.order_index).all()

        # Customize steps based on user background
        return PersonalizationService.customize_steps_by_user_background(db, chapter_id, user_profile)

    @staticmethod
    def calculate_step_difficulty_adjustment(user_profile: UserProfile, step: LearningStep) -> Dict[str, Any]:
        """Calculate how a step should be adjusted for a user based on their background"""
        # This would be a more complex algorithm in a real system
        # For now, we'll return some basic adjustments based on background

        adjustments = {
            "content_depth": 1.0,  # 1.0 = normal, <1.0 = simplified, >1.0 = more detailed
            "examples_count": 1,   # Number of examples to include
            "prerequisites_check": True,  # Whether to check prerequisites strictly
            "time_requirement": 1.0,      # Multiplier for required time to complete
        }

        background_level = user_profile.background_level

        if background_level == "advanced":
            adjustments["content_depth"] = 1.5  # More in-depth content
            adjustments["examples_count"] = 2    # More examples
            adjustments["prerequisites_check"] = False  # Less strict on prerequisites
            adjustments["time_requirement"] = 0.7       # Less time required
        elif background_level == "intermediate":
            adjustments["content_depth"] = 1.0  # Standard content
            adjustments["examples_count"] = 1    # Standard examples
            adjustments["prerequisites_check"] = True   # Standard prerequisite checking
            adjustments["time_requirement"] = 1.0       # Standard time
        else:  # beginner
            adjustments["content_depth"] = 0.7  # Simplified content
            adjustments["examples_count"] = 3    # More examples for clarity
            adjustments["prerequisites_check"] = True   # Strict prerequisite checking
            adjustments["time_requirement"] = 1.3       # More time allowed

        return adjustments