"""
API route definitions for the YouTube Video Fetcher service.

This module defines the HTTP endpoints for retrieving and searching videos.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import schemas
from app.errors import errors
from app.services.service import get_videos_service, search_videos_service
from app.db.database import get_db

router = APIRouter()

@router.get("/")
async def root():
    """
    Health check endpoint for the API.

    Returns:
        dict: A message indicating the API is running.
    """
    return {"message": "YouTube Latest Videos API is running."}

@router.get("/videos", response_model=schemas.PaginatedVideoResponse)
async def get_videos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a paginated list of stored videos, sorted by published datetime (descending).

    Args:
        page (int): The page number (1-based).
        page_size (int): The number of videos per page.
        db (AsyncSession): The async database session (injected).

    Returns:
        PaginatedVideoResponse: Paginated video data.
    """
    return await get_videos_service(db, page, page_size)

@router.get("/search", response_model=schemas.VideoSearchResponse)
async def search_videos(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for videos by title or description, supporting partial and multi-word matching.

    Args:
        q (str): The search query string.
        page (int): The page number (1-based).
        page_size (int): The number of videos per page.
        db (AsyncSession): The async database session (injected).

    Returns:
        VideoSearchResponse: Paginated search results.
    """
    # Validate that the search query is not empty or just whitespace
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errors.INVALID_SEARCH_QUERY,
        )
    return await search_videos_service(db, q, page, page_size)
