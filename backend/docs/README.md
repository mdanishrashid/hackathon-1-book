# AI-Native Textbook Backend API

The backend server for the AI-Native Textbook for Physical AI & Humanoid Robotics, built with FastAPI.

## Overview

This API provides the core functionality for the AI-Native Textbook, including:
- User authentication and authorization
- Chapter and learning step management
- Progress tracking and visualization
- Personalized learning path delivery
- Data persistence and retrieval

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy ORM**: Database abstraction for persistent data storage
- **JWT Authentication**: Secure user authentication and authorization
- **Async Support**: Designed for high performance and concurrency
- **Type Safety**: Full type hints for better code reliability

## API Structure

- **/api/v1**: Version 1 of the API
  - **/auth**: Authentication endpoints
  - **/chapters**: Chapter management
  - **/steps**: Learning step management and delivery
  - **/progress**: Progress tracking and visualization
  - **/profiles**: User profile management
  - **/learning-paths**: Personalized learning path management

## Quick Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables (see `.env.example`)
3. Run database migrations: `alembic upgrade head`
4. Start the server: `uvicorn main:app --reload`

## Endpoints

For detailed API documentation, start the server and visit the `/docs` endpoint for interactive API documentation.