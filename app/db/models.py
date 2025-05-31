from sqlalchemy import Column, String, DateTime, Integer, JSON, Index, func
from .database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    youtube_video_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String, index=True)
    published_at = Column(DateTime(timezone=True), index=True, nullable=False)
    thumbnails = Column(JSON, nullable=False)
    video_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_videos_published_at_desc", published_at.desc()),
    )
