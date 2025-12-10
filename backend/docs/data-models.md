# Data Models

This document describes the core data models used in the AI-Native Textbook backend.

## User Profile Model

Represents user information and learning preferences:

- `id`: UUID identifier
- `auth_id`: Authentication ID (foreign key to Better-Auth)
- `background_level`: User's experience level (beginner, intermediate, advanced)
- `preferred_language`: Language preference
- `learning_preferences`: JSON string for customized learning settings
- `created_at`, `updated_at`: Timestamps

## Chapter Model

Represents a major topic or section:

- `id`: UUID identifier
- `title`: Chapter title
- `description`: Chapter description
- `order_index`: Sequence order
- `created_at`, `updated_at`: Timestamps

## Learning Step Model

Represents an individual learning unit:

- `id`: UUID identifier
- `chapter_id`: Reference to parent chapter
- `title`: Step title
- `content`: Learning content
- `step_type`: Type of learning activity
- `order_index`: Position in chapter sequence
- `prerequisite_step_id`: ID of required prerequisite step
- `required_completion_criteria`: JSON string for completion requirements
- `created_at`, `updated_at`: Timestamps

## Learning Progress Model

Tracks user progress through steps:

- `id`: UUID identifier
- `user_id`: Reference to user profile
- `step_id`: Reference to learning step
- `status`: Progress status (not_started, in_progress, completed)
- `completion_percentage`: Progress percentage
- `started_at`, `completed_at`: Progress timestamps
- `progress_data`: JSON string for additional progress data
- `created_at`, `updated_at`: Timestamps

## Learning Path Model

Represents a customized sequence of learning steps:

- `id`: UUID identifier
- `user_id`: Reference to user profile
- `name`: Learning path name
- `description`: Path description
- `path_type`: Path type (default, personalized, remedial)
- `steps_sequence`: JSON string representing the sequence of steps
- `created_at`, `updated_at`: Timestamps