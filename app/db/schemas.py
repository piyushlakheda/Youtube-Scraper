from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class VideoBase(BaseModel):
    youtube_video_id: str
    title: str
    description: str
    published_at: datetime
    thumbnails: Dict[str, Any]
    video_url: str

class VideoRead(VideoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedVideoResponse(BaseModel):
    total: int
    page: int
    page_size: int
    videos: List[VideoRead]

class VideoSearchResponse(BaseModel):
    total: int
    videos: List[VideoRead]
