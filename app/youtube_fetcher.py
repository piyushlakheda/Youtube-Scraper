import os
import asyncio
from datetime import datetime, timedelta, timezone
import httpx
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.crud import upsert_videos
from app.db.schemas import VideoBase

YOUTUBE_API_KEYS = os.getenv("YOUTUBE_API_KEYS") or os.getenv("YOUTUBE_API_KEY", "YOUR_API_KEY")
if "," in YOUTUBE_API_KEYS:
    YOUTUBE_API_KEYS = [k.strip() for k in YOUTUBE_API_KEYS.split(",") if k.strip()]
else:
    YOUTUBE_API_KEYS = [YOUTUBE_API_KEYS]
YOUTUBE_SEARCH_QUERY = os.getenv("YOUTUBE_SEARCH_QUERY", "news")
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
FETCH_INTERVAL = int(os.getenv("YOUTUBE_FETCH_INTERVAL", "10"))  # seconds

_last_published_at = None

async def fetch_latest_videos():
    global _last_published_at
    params = {
        "part": "snippet",
        "q": YOUTUBE_SEARCH_QUERY,
        "type": "video",
        "order": "date",
        "maxResults": 20,
    }
    if _last_published_at:
        params["publishedAfter"] = _last_published_at.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        # Default: fetch videos from last 1 hour
        params["publishedAfter"] = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    last_error = None
    for key in YOUTUBE_API_KEYS:
        params["key"] = key
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(YOUTUBE_API_URL, params=params)
                if resp.status_code == 403:
                    # Quota or forbidden, try next key
                    print(f"API key quota exhausted or forbidden for key: {key}")
                    last_error = resp.text
                    continue
                resp.raise_for_status()
                data = resp.json()
                videos = []
                for item in data.get("items", []):
                    snippet = item["snippet"]
                    video_id = item["id"]["videoId"]
                    published_at = snippet["publishedAt"]
                    published_at_dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                    videos.append(
                        VideoBase(
                            youtube_video_id=video_id,
                            title=snippet["title"],
                            description=snippet.get("description", ""),
                            published_at=published_at_dt,
                            thumbnails=snippet.get("thumbnails", {}),
                            video_url=f"https://www.youtube.com/watch?v={video_id}",
                        )
                    )
                if videos:
                    # Update last published_at for next fetch
                    _last_published_at = max(v.published_at for v in videos)
                return videos
        except Exception as e:
            print(f"Error fetching YouTube videos with key {key}: {e}")
            last_error = str(e)
            continue
    print(f"All API keys exhausted or failed. Last error: {last_error}")
    return []

async def youtube_fetcher_loop(sessionmaker: async_sessionmaker):
    while True:
        try:
            async with sessionmaker() as db:
                videos = await fetch_latest_videos()
                if videos:
                    await upsert_videos(db, videos)
        except Exception as e:
            print(f"Error fetching YouTube videos: {e}")
        await asyncio.sleep(FETCH_INTERVAL)
