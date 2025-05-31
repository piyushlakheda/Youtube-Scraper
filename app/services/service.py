"""
Service layer for business logic related to video retrieval and search.

This module provides helper functions that encapsulate the business logic
for fetching paginated videos and searching videos in the database.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.db import crud, schemas

async def get_videos_service(db: AsyncSession, page: int, page_size: int) -> schemas.PaginatedVideoResponse:
    """
    Retrieve a paginated list of videos from the database.

    Args:
        db (AsyncSession): The async database session.
        page (int): The page number (1-based).
        page_size (int): The number of videos per page.

    Returns:
        PaginatedVideoResponse: A paginated response containing video data.
    """
    videos, total = await crud.get_videos_paginated(db, page, page_size)
    return schemas.PaginatedVideoResponse(
        total=total,
        page=page,
        page_size=page_size,
        videos=[schemas.VideoRead.from_orm(v) for v in videos]
    )

async def search_videos_service(db: AsyncSession, query: str, page: int, page_size: int) -> schemas.VideoSearchResponse:
    """
    Search for videos in the database by query, supporting partial and multi-word matching.

    Args:
        db (AsyncSession): The async database session.
        query (str): The search query string.
        page (int): The page number (1-based).
        page_size (int): The number of videos per page.

    Returns:
        VideoSearchResponse: A paginated response containing search results.
    """
    videos, total = await crud.search_videos(db, query, page, page_size)
    return schemas.VideoSearchResponse(
        total=total,
        videos=[schemas.VideoRead.from_orm(v) for v in videos]
    )
