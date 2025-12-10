# Data Model: Step-by-Step Execution Feature

## Entity: UserProfile
**Description**: Stores user-specific information including background knowledge for personalization

**Fields**:
- id (UUID, Primary Key)
- auth_id (String, Foreign Key to Better-Auth user) - required
- background_level (Enum: beginner, intermediate, advanced) - required, default: beginner
- preferred_language (String) - required, default: "en"
- created_at (DateTime) - required
- updated_at (DateTime) - required
- learning_preferences (JSON) - optional, for personalization settings

**Relationships**:
- One-to-many: LearningProgress (via user_id)

**Validation Rules**:
- background_level must be one of the defined enum values
- auth_id must be unique and reference a valid Better-Auth user

## Entity: Chapter
**Description**: Represents a learning chapter that contains multiple sequential steps

**Fields**:
- id (UUID, Primary Key)
- title (String, max 255) - required
- description (Text) - required
- order_index (Integer) - required
- prerequisite_chapter_id (UUID, Foreign Key to Chapter) - optional
- is_active (Boolean) - required, default: true
- created_at (DateTime) - required
- updated_at (DateTime) - required

**Relationships**:
- One-to-many: LearningStep (via chapter_id)
- Many-to-many: UserProfiles (via LearningProgress)

**Validation Rules**:
- Title must be unique within the textbook
- order_index must be unique within the textbook
- prerequisite_chapter_id must reference a valid existing chapter

## Entity: LearningStep
**Description**: Represents an individual step within a chapter that users must complete sequentially

**Fields**:
- id (UUID, Primary Key)
- chapter_id (UUID, Foreign Key to Chapter) - required
- title (String, max 255) - required
- content (Text) - required
- step_type (Enum: reading, quiz, exercise, video, interactive) - required
- order_index (Integer) - required
- prerequisite_step_id (UUID, Foreign Key to LearningStep) - optional
- required_completion_criteria (JSON) - required, default: {"type": "time", "value": 60}
- created_at (DateTime) - required
- updated_at (DateTime) - required

**Relationships**:
- Many-to-one: Chapter (via chapter_id)
- One-to-many: LearningProgress (via step_id)

**Validation Rules**:
- order_index must be unique within the chapter
- chapter_id must reference a valid existing chapter
- step_type must be one of the defined enum values
- required_completion_criteria must be valid JSON with appropriate structure

## Entity: LearningProgress
**Description**: Tracks user progress through learning steps and chapters

**Fields**:
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to UserProfile) - required
- step_id (UUID, Foreign Key to LearningStep) - required
- status (Enum: not_started, in_progress, completed, skipped) - required, default: not_started
- completion_percentage (Integer, 0-100) - optional, default: 0
- started_at (DateTime) - optional
- completed_at (DateTime) - optional
- progress_data (JSON) - optional, for storing step-specific progress
- created_at (DateTime) - required
- updated_at (DateTime) - required

**Relationships**:
- Many-to-one: UserProfile (via user_id)
- Many-to-one: LearningStep (via step_id)

**Validation Rules**:
- Combination of user_id and step_id must be unique
- status must be one of the defined enum values
- completion_percentage must be between 0 and 100
- completed_at must be null if status is not "completed"

## Entity: LearningPath
**Description**: Represents a personalized learning path based on user background and preferences

**Fields**:
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to UserProfile) - required
- name (String, max 255) - required
- description (Text) - optional
- path_type (Enum: default, personalized, remedial) - required, default: default
- steps_sequence (JSON) - required
- created_at (DateTime) - required
- updated_at (DateTime) - required

**Relationships**:
- Many-to-one: UserProfile (via user_id)
- Many-to-many: LearningStep (via steps_sequence)

**Validation Rules**:
- user_id must reference a valid existing user profile
- path_type must be one of the defined enum values
- steps_sequence must be valid JSON with appropriate structure

## Relationships Summary

1. UserProfile → LearningProgress (one-to-many)
2. Chapter → LearningStep (one-to-many)
3. UserProfile → LearningPath (one-to-many)
4. LearningStep → LearningProgress (one-to-many)
5. UserProfile → LearningPath (one-to-many)

## Indexes for Performance

- UserProfile: index on auth_id
- LearningProgress: composite index on (user_id, step_id)
- LearningProgress: index on status
- LearningStep: composite index on (chapter_id, order_index)
- Chapter: index on order_index