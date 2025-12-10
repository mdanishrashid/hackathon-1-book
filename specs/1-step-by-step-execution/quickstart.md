# Quickstart Guide: Step-by-Step Execution Feature

## Overview
This guide will help you get started with the step-by-step execution feature for the AI-Native Textbook. This feature enables users to progress through educational content in a sequential, structured manner with progress tracking and personalization.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for Docusaurus)
- Access to PostgreSQL database
- Better-Auth configured for authentication

## Setup

### 1. Environment Configuration
```bash
# Database configuration
export DATABASE_URL="postgresql://username:password@localhost:5432/textbook_db"

# Authentication configuration
export BETTER_AUTH_SECRET="your-secret-key"
export BETTER_AUTH_URL="http://localhost:3000"

# JWT secrets
export SECRET_KEY="your-jwt-secret-key"
```

### 2. Install Dependencies
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies (in your Docusaurus directory)
cd website
npm install
```

### 3. Database Setup
```bash
# Run database migrations to create required tables
cd backend
alembic upgrade head
```

## API Usage

### 1. Getting Started
To begin using the step-by-step execution feature, first ensure the user is authenticated via Better-Auth.

### 2. Fetch Available Chapters
```javascript
// Get all available chapters
GET /api/v1/chapters

// Response:
[
  {
    "id": "uuid-string",
    "title": "Introduction to AI",
    "description": "Basic concepts of artificial intelligence",
    "order_index": 1,
    "is_active": true
  }
]
```

### 3. Navigate to a Chapter
```javascript
// Get details of a specific chapter with its steps
GET /api/v1/chapters/{chapterId}

// Response includes the chapter details and all its steps in order
```

### 4. Retrieve Steps
```javascript
// Get all steps for a chapter
GET /api/v1/steps/chapter/{chapterId}

// Get personalized/adaptive steps for a chapter based on user profile
GET /api/v1/steps/chapter/{chapterId}/adaptive
```

### 5. Track and Update Progress
```javascript
// Check progress for a specific step
GET /api/v1/progress/steps/{stepId}

// Mark a step as completed
POST /api/v1/progress/steps/{stepId}/complete

// Request body may include validation data depending on the step
{
  "validation_data": {
    // Step-specific validation data
  }
}
```

### 6. View Overall Progress
```javascript
// Get user's overall progress
GET /api/v1/progress

// Response includes overall completion percentage and progress per chapter
{
  "total_steps": 50,
  "completed_steps": 15,
  "in_progress_steps": 5,
  "not_started_steps": 30,
  "overall_completion_percentage": 30.0,
  "chapters": [
    {
      "chapter_id": "uuid",
      "chapter_title": "Introduction to AI",
      "total_steps": 10,
      "completed_steps": 3,
      "in_progress_steps": 1,
      "completion_percentage": 30.0
    }
  ]
}
```

### 7. User Profile Management
```javascript
// Get user profile
GET /api/v1/profiles/me

// Update user profile
PUT /api/v1/profiles/me

// Request body:
{
  "background_level": "intermediate",  // beginner, intermediate, advanced
  "preferred_language": "en",
  "learning_preferences": "{\"visual_learner\": true, \"time_per_step\": 300}"
}
```

### 8. Learning Path Management
```javascript
// Get user's learning paths
GET /api/v1/learning-paths

// Create a custom learning path
POST /api/v1/learning-paths

// Get adaptive learning path based on user profile
GET /api/v1/learning-paths/adaptive/{chapter_id}
```

## Implementation Tips

### 1. Enforcing Step Sequences
The API enforces that users must complete the current step before accessing the next one. Your frontend should check the progress status before allowing navigation to the next step.

### 2. Progress Validation
Different step types may require different validation for completion:
- Reading steps: May require minimum time on page
- Quiz steps: May require passing grade
- Exercise steps: May require submission of correct answer

### 3. Personalization
Retrieve the user's profile to customize the learning path based on their background level.
```javascript
GET /api/v1/profiles/me

// Use the background_level to determine which content path to present
```

## Error Handling

Common responses:
- `401 Unauthorized`: User not authenticated
- `403 Forbidden`: Attempting to access steps in wrong sequence
- `404 Not Found`: Requested resource does not exist
- `400 Bad Request`: Invalid request data

## Frontend Integration

### 1. Progress Indicators
Display progress bars or completion indicators that update in real-time as users complete steps.

### 2. Navigation Controls
Only enable "Next" button when the current step is marked as completed.

### 3. Resume Functionality
On page load, check the user's progress and resume from where they left off.

## Testing

### Unit Tests
```bash
# Run backend tests
cd backend
python -m pytest tests/unit/

# Run API contract tests
python -m pytest tests/contract/
```

### Integration Tests
```bash
# Run integration tests
python -m pytest tests/integration/
```

## Next Steps

1. Review the full API documentation by running the server and visiting `/docs`
2. Implement the progress tracking UI components in Docusaurus
3. Connect the UI to the backend API endpoints
4. Test the complete learning flow with real educational content

## Troubleshooting

- If progress isn't saving: Check that your authentication tokens are being sent with all requests
- If steps appear out of order: Verify that the `order_index` values are correctly set in the database
- If personalization isn't working: Confirm that user profiles are being saved with the proper background level
- If authentication fails: Ensure Better-Auth is properly configured and tokens are valid