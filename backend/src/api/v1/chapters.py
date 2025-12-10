from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models.chapter import Chapter
from ...models.learning_step import LearningStep
from ...services.chapter_service import ChapterService
from ...services.learning_step_service import LearningStepService

router = APIRouter()

@router.get("/", response_model=List[Chapter])
def get_all_chapters(db: Session = Depends(get_db)):
    """Get all available chapters in the textbook"""
    chapters = ChapterService.get_all_chapters(db)
    return chapters

@router.get("/{chapter_id}", response_model=Chapter)
def get_chapter_by_id(chapter_id: str, db: Session = Depends(get_db)):
    """Get details of a specific chapter including its steps"""
    chapter = ChapterService.get_chapter_with_steps(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter with ID {chapter_id} not found"
        )
    return chapter

@router.get("/{chapter_id}/steps", response_model=List[LearningStep])
def get_chapter_steps(chapter_id: str, db: Session = Depends(get_db)):
    """Get all steps for a specific chapter"""
    steps = LearningStepService.get_steps_by_chapter(db, chapter_id)
    return steps