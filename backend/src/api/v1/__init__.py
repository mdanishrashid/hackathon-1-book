from fastapi import APIRouter
from . import auth, chapters, steps, progress, profiles, learning_paths, rag

router = APIRouter()

# Include all v1 sub-routers
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
router.include_router(steps.router, prefix="/steps", tags=["steps"])
router.include_router(progress.router, prefix="/progress", tags=["progress"])
router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning-paths"])
router.include_router(rag.router, prefix="/rag", tags=["rag"])