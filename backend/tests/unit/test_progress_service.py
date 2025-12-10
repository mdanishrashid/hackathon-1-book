import unittest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from src.models.learning_progress import LearningProgress
from src.services.progress_service import ProgressService, ProgressValidationException
from datetime import datetime

class TestProgressService(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = Mock(spec=Session)
        self.user_id = "test-user-id"
        self.step_id = "test-step-id"
        
    def test_get_user_progress(self):
        """Test getting all progress records for a user"""
        # Arrange
        expected_progress = [
            Mock(spec=LearningProgress, id=1, user_id=self.user_id, step_id="step1"),
            Mock(spec=LearningProgress, id=2, user_id=self.user_id, step_id="step2")
        ]
        self.mock_db.query().filter().all.return_value = expected_progress
        
        # Act
        result = ProgressService.get_user_progress(self.mock_db, self.user_id)
        
        # Assert
        self.assertEqual(result, expected_progress)
        self.mock_db.query().filter.assert_called_once()
        
    def test_get_progress_for_step(self):
        """Test getting progress for a specific user and step"""
        # Arrange
        expected_progress = Mock(spec=LearningProgress, 
                                user_id=self.user_id, 
                                step_id=self.step_id,
                                status="in_progress",
                                completion_percentage=50)
        self.mock_db.query().filter().filter().first.return_value = expected_progress
        
        # Act
        result = ProgressService.get_progress_for_step(self.mock_db, self.user_id, self.step_id)
        
        # Assert
        self.assertEqual(result, expected_progress)
        self.mock_db.query().filter().filter().first.assert_called_once()
        
    def test_get_progress_for_step_not_found(self):
        """Test getting progress when no record exists"""
        # Arrange
        self.mock_db.query().filter().filter().first.return_value = None
        
        # Act
        result = ProgressService.get_progress_for_step(self.mock_db, self.user_id, self.step_id)
        
        # Assert
        self.assertIsNone(result)
        
    def test_record_step_progress_new(self):
        """Test recording progress for a step that doesn't have existing progress"""
        # Arrange
        mock_progress = Mock(spec=LearningProgress, id=1, user_id=self.user_id, step_id=self.step_id)
        self.mock_db.query().filter().filter().first.return_value = None  # No existing progress
        self.mock_db.add = Mock()
        self.mock_db.commit = Mock()
        self.mock_db.refresh = Mock()
        
        # Act
        with patch('src.services.progress_service.LearningProgress', return_value=mock_progress):
            result = ProgressService.record_step_progress(
                self.mock_db, 
                self.user_id, 
                self.step_id, 
                "completed", 
                100, 
                {"test": "data"}
            )
        
        # Assert
        self.assertEqual(result, mock_progress)
        self.mock_db.add.assert_called_once_with(mock_progress)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(mock_progress)
        
    def test_record_step_progress_update(self):
        """Test updating existing progress for a step"""
        # Arrange
        existing_progress = Mock(spec=LearningProgress, 
                                id=1, 
                                user_id=self.user_id, 
                                step_id=self.step_id,
                                status="in_progress",
                                completion_percentage=50,
                                progress_data=None,
                                completed_at=None,
                                updated_at=None)
        self.mock_db.query().filter().filter().first.return_value = existing_progress
        self.mock_db.commit = Mock()
        self.mock_db.refresh = Mock()
        
        # Act
        result = ProgressService.record_step_progress(
            self.mock_db, 
            self.user_id, 
            self.step_id, 
            "completed", 
            100, 
            {"test": "data"}
        )
        
        # Assert
        self.assertEqual(result, existing_progress)
        self.assertEqual(existing_progress.status, "completed")
        self.assertEqual(existing_progress.completion_percentage, 100)
        self.assertIsNotNone(existing_progress.completed_at)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(existing_progress)
        
    def test_validate_step_completion_success(self):
        """Test successful step completion validation"""
        # Arrange
        mock_step = Mock()
        mock_step.prerequisite_step_id = None
        mock_step.required_completion_criteria = None
        
        with patch('src.services.learning_step_service.LearningStepService.get_step_by_id', 
                   return_value=mock_step):
            # Act
            result = ProgressService.validate_step_completion(self.mock_db, self.user_id, self.step_id)
        
        # Assert
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()