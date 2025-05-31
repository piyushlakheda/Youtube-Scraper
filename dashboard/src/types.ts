export interface Thumbnail {
  url: string;
  width: number;
  height: number;
}

export interface Thumbnails {
  [key: string]: Thumbnail;
}

export interface Video {
  id: number;
  youtube_video_id: string;
  title: string;
  description: string;
  published_at: string;
  thumbnails: Thumbnails;
  video_url: string;
  created_at: string;
}

export interface PaginatedVideoResponse {
  total: number;
  page: number;
  page_size: number;
  videos: Video[];
}

export interface VideoSearchResponse {
  total: number;
  videos: Video[];
}
