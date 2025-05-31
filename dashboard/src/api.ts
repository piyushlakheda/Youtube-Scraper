import { PaginatedVideoResponse, VideoSearchResponse } from "./types";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function getVideos(page = 1, pageSize = 20): Promise<PaginatedVideoResponse> {
  const res = await fetch(`${API_BASE}/videos?page=${page}&page_size=${pageSize}`);
  if (!res.ok) throw new Error("Failed to fetch videos");
  return res.json();
}

export async function searchVideos(query: string, page = 1, pageSize = 20): Promise<VideoSearchResponse> {
  const res = await fetch(
    `${API_BASE}/search?q=${encodeURIComponent(query)}&page=${page}&page_size=${pageSize}`
  );
  if (!res.ok) throw new Error("Failed to search videos");
  return res.json();
}
