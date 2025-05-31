from sqlalchemy import select, desc, or_, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .models import Video
from .schemas import VideoBase

async def upsert_videos(db: AsyncSession, videos: List[VideoBase]):
    for video in videos:
        stmt = insert(Video).values(
            youtube_video_id=video.youtube_video_id,
            title=video.title,
            description=video.description,
            published_at=video.published_at,
            thumbnails=video.thumbnails,
            video_url=video.video_url,
        ).on_conflict_do_nothing(index_elements=['youtube_video_id'])
        await db.execute(stmt)
    await db.commit()

async def get_videos_paginated(
    db: AsyncSession, page: int = 1, page_size: int = 20
):
    stmt = select(Video).order_by(desc(Video.published_at)).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    videos = result.scalars().all()
    total = await db.scalar(select(func.count()).select_from(Video))
    return videos, total

async def search_videos(
    db: AsyncSession, query: str, page: int = 1, page_size: int = 20
):
    words = [w.strip() for w in query.strip().split() if w.strip()]
    if not words:
        return [], 0

    from sqlalchemy import and_

    conditions = [
        or_(
            Video.title.ilike(f"%{word}%"),
            Video.description.ilike(f"%{word}%"),
        )
        for word in words
    ]
    stmt = (
        select(Video)
        .where(and_(*conditions))
        .order_by(desc(Video.published_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    videos = result.scalars().all()
    total = await db.scalar(
        select(func.count()).select_from(Video).where(and_(*conditions))
    )
    return videos, total
