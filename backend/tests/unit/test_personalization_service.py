import unittest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from src.models.user_profile import UserProfile
from src.models.learning_step import LearningStep
from src.services.personalization_service import PersonalizationService

class TestPersonalizationService(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = Mock(spec=Session)
        self.user_id = "test-user-id"
        self.chapter_id = "test-chapter-id"
        
    def test_calculate_step_difficulty_adjustment_beginner(self):
        """Test difficulty adjustment for beginner user"""
        # Arrange
        user_profile = Mock(spec=UserProfile)
        user_profile.background_level = "beginner"
        mock_step = Mock(spec=LearningStep)
        
        # Act
        result = PersonalizationService.calculate_step_difficulty_adjustment(user_profile, mock_step)
        
        # Assert
        self.assertEqual(result["content_depth"], 0.7)
        self.assertEqual(result["examples_count"], 3)
        self.assertTrue(result["prerequisites_check"])
        self.assertEqual(result["time_requirement"], 1.3)
        
    def test_calculate_step_difficulty_adjustment_intermediate(self):
        """Test difficulty adjustment for intermediate user"""
        # Arrange
        user_profile = Mock(spec=UserProfile)
        user_profile.background_level = "intermediate"
        mock_step = Mock(spec=LearningStep)
        
        # Act
        result = PersonalizationService.calculate_step_difficulty_adjustment(user_profile, mock_step)
        
        # Assert
        self.assertEqual(result["content_depth"], 1.0)
        self.assertEqual(result["examples_count"], 1)
        self.assertTrue(result["prerequisites_check"])
        self.assertEqual(result["time_requirement"], 1.0)
        
    def test_calculate_step_difficulty_adjustment_advanced(self):
        """Test difficulty adjustment for advanced user"""
        # Arrange
        user_profile = Mock(spec=UserProfile)
        user_profile.background_level = "advanced"
        mock_step = Mock(spec=LearningStep)
        
        # Act
        result = PersonalizationService.calculate_step_difficulty_adjustment(user_profile, mock_step)
        
        # Assert
        self.assertEqual(result["content_depth"], 1.5)
        self.assertEqual(result["examples_count"], 2)
        self.assertFalse(result["prerequisites_check"])
        self.assertEqual(result["time_requirement"], 0.7)

if __name__ == '__main__':
    unittest.main()