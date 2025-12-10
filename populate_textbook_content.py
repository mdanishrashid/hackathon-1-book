"""
Script to populate the AI-Native Textbook with chapters and steps for Physical AI & Humanoid Robotics
Based on the project constitution: 10-12 short, clean, modern chapters that can be read in under 60 minutes total
"""
import os
import sys
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend src directory to the path so we can import the models
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.database import Base
from backend.src.models.chapter import Chapter
from backend.src.models.learning_step import LearningStep

def create_sample_chapters():
    """Create sample chapters for the AI-Native Textbook"""
    
    # Sample chapters based on the project title: "AI-Native Textbook for Physical AI & Humanoid Robotics"
    chapters_data = [
        {
            "title": "Introduction to Physical AI",
            "description": "Understanding the fundamentals of physical AI - the intersection of artificial intelligence and real-world physical systems",
            "order_index": 1
        },
        {
            "title": "Humanoid Robotics Overview", 
            "description": "Introduction to humanoid robots, their design principles, and applications in modern society",
            "order_index": 2
        },
        {
            "title": "Embodied Cognition and AI",
            "description": "How physical embodiment influences artificial intelligence and learning",
            "order_index": 3
        },
        {
            "title": "Locomotion and Movement Control",
            "description": "Principles of walking, balancing, and movement control in humanoid robots",
            "order_index": 4
        },
        {
            "title": "Perception Systems",
            "description": "How humanoid robots perceive and interpret their environment using sensors",
            "order_index": 5
        },
        {
            "title": "Manipulation and Dexterity", 
            "description": "Controlling robotic hands and arms for precise manipulation tasks",
            "order_index": 6
        },
        {
            "title": "Human-Robot Interaction",
            "description": "Designing interfaces and behaviors for effective human-robot collaboration",
            "order_index": 7
        },
        {
            "title": "AI Learning in Physical Systems",
            "description": "How robots learn from physical interaction with their environment",
            "order_index": 8
        },
        {
            "title": "Applications and Ethics",
            "description": "Real-world applications of humanoid robots and ethical considerations",
            "order_index": 9
        },
        {
            "title": "Future of Physical AI",
            "description": "Emerging trends and future possibilities in humanoid robotics",
            "order_index": 10
        },
        {
            "title": "Building Your First Physical AI System",
            "description": "A practical guide to implementing your first physical AI system",
            "order_index": 11
        },
        {
            "title": "Case Studies",
            "description": "Real-world examples and case studies of humanoid robots in action",
            "order_index": 12
        }
    ]
    
    return chapters_data

def create_sample_steps_for_chapter(chapter_id):
    """Create sample steps for a chapter"""
    # Each chapter will have 3-5 steps for an engaging experience
    base_steps = [
        {
            "title": "Introduction",
            "content": "Brief overview and learning objectives for this section. In this chapter, you will learn about the fundamental concepts that make physical AI systems unique and how they differ from traditional AI approaches.",
            "step_type": "reading",
            "order_index": 1,
            "required_completion_criteria": '{"type": "time", "value": 60}'  # Require 60 seconds minimum
        },
        {
            "title": "Core Concepts",
            "content": "In-depth exploration of key concepts in this chapter. We'll examine the core principles, theories, and methodologies that underpin the subject matter, providing you with a strong foundation for understanding more advanced topics.",
            "step_type": "reading",
            "order_index": 2,
            "required_completion_criteria": '{"type": "time", "value": 120}'  # Require 120 seconds minimum
        },
        {
            "title": "Practical Application",
            "content": "Real-world examples and applications of the concepts discussed. See how these principles are implemented in actual physical AI and humanoid robotics systems, with case studies and examples from the field.",
            "step_type": "reading",
            "order_index": 3,
            "required_completion_criteria": '{"type": "time", "value": 90}'  # Require 90 seconds minimum
        },
        {
            "title": "Knowledge Check",
            "content": "Quick assessment to reinforce learning. Test your understanding of the key concepts covered in this chapter with a short quiz designed to help you retain what you've learned.",
            "step_type": "quiz",
            "order_index": 4,
            "required_completion_criteria": '{"type": "quiz_score", "value": 70}'  # Require 70% score
        },
        {
            "title": "Summary and Next Steps",
            "content": "Recap of key points and preparation for the next chapter. Review what you've learned and get a preview of the upcoming material to help consolidate your knowledge and prepare for the next steps in your learning journey.",
            "step_type": "reading",
            "order_index": 5,
            "required_completion_criteria": '{"type": "time", "value": 60}'  # Require 60 seconds minimum
        }
    ]
    
    # Return only first 3 steps for shorter chapters (as per constitution of 60 minutes total)
    steps = []
    for i in range(3):  # Each chapter has 3 steps for brevity
        step = base_steps[i].copy()
        step["chapter_id"] = chapter_id
        steps.append(step)
    
    return steps

def populate_database():
    """Populate the database with sample chapters and steps"""
    # Connect to the database (assuming the environment variable is set)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./textbook.db")
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Check if chapters already exist
        existing_chapter_count = db.query(Chapter).count()
        if existing_chapter_count > 0:
            print(f"Database already contains {existing_chapter_count} chapters. Skipping population.")
            return
            
        # Create and add chapters
        chapters = create_sample_chapters()
        chapter_objects = []
        
        for chapter_data in chapters:
            chapter = Chapter(
                id=uuid.uuid4(),
                title=chapter_data["title"],
                description=chapter_data["description"],
                order_index=chapter_data["order_index"],
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(chapter)
            chapter_objects.append(chapter)
        
        # Commit chapters to get their IDs
        db.commit()
        
        # Create and add steps for each chapter
        for chapter in chapter_objects:
            steps_data = create_sample_steps_for_chapter(chapter.id)
            
            for step_data in steps_data:
                step = LearningStep(
                    id=uuid.uuid4(),
                    chapter_id=step_data["chapter_id"],
                    title=step_data["title"],
                    content=step_data["content"],
                    step_type=step_data["step_type"],
                    order_index=step_data["order_index"],
                    required_completion_criteria=step_data["required_completion_criteria"],
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(step)
        
        # Commit all steps
        db.commit()
        
        print(f"Successfully added {len(chapter_objects)} chapters and their steps to the database.")
        
    except Exception as e:
        print(f"Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()