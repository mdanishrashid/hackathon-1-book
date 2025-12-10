---
sidebar_position: 3
---

# Developer Guide

This guide helps developers understand and extend the AI-Native Textbook platform.

## Architecture

The frontend is built with Docusaurus and includes:

- **Step-by-Step Navigation**: Components for sequential learning
- **Progress Tracking**: Visual indicators of learning progress
- **Personalization**: User profile and learning path customization
- **API Integration**: Communication with the backend API

## Key Components

### StepProgress Component
Manages navigation and progress visualization for individual steps within chapters.

### ProgressBar Component
Displays visual progress indicators for chapters and overall learning.

### LearningPathSelector Component
Allows users to select different learning paths based on their background.

### Dashboard Page
Provides an overview of user progress across all chapters.

## API Client

The `api-client.js` service handles communication with the backend API, including:

- Chapter and step retrieval
- Progress tracking and updates
- User profile management
- Learning path selection

## Adding New Content

New chapters and steps are managed through the backend API. The frontend adapts to the content structure provided by the backend.