# API Endpoints Documentation

This document provides details about the backend API endpoints for the AI-Native Textbook.

## Authentication Endpoints

### `POST /api/v1/auth/login`
Authenticate a user and return a JWT token.

### `POST /api/v1/auth/register`
Register a new user account.

## Chapter Endpoints

### `GET /api/v1/chapters`
Retrieve a list of all available chapters.

### `GET /api/v1/chapters/{chapter_id}`
Get details of a specific chapter.

## Step Endpoints

### `GET /api/v1/steps/{step_id}`
Get details of a specific learning step.

### `GET /api/v1/steps/chapter/{chapter_id}`
Get all steps for a specific chapter.

### `GET /api/v1/steps/chapter/{chapter_id}/adaptive`
Get personalized steps for a chapter based on user profile.

### `GET /api/v1/steps/chapter/{chapter_id}/first`
Get the first step of a chapter, potentially personalized.

## Progress Endpoints

### `GET /api/v1/progress`
Get user's overall progress across all chapters and steps.

### `GET /api/v1/progress/chapters/{chapter_id}`
Get user's progress for a specific chapter.

### `GET /api/v1/progress/steps/{step_id}`
Get progress for a specific step.

### `POST /api/v1/progress/steps/{step_id}/complete`
Mark a step as completed after validation.

## Profile Endpoints

### `GET /api/v1/profiles/me`
Get the authenticated user's profile information.

### `PUT /api/v1/profiles/me`
Update the authenticated user's profile information.

## Learning Path Endpoints

### `GET /api/v1/learning-paths`
Get all learning paths for the authenticated user.

### `GET /api/v1/learning-paths/{path_id}`
Get a specific learning path by ID.

### `POST /api/v1/learning-paths`
Create a new learning path for the authenticated user.

### `PUT /api/v1/learning-paths/{path_id}`
Update an existing learning path.

### `DELETE /api/v1/learning-paths/{path_id}`
Delete a learning path.

### `GET /api/v1/learning-paths/adaptive/{chapter_id}`
Get an adaptive learning path for the user based on their profile and the chapter.