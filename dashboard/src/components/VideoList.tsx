import React from "react";
import { Video } from "../types";

interface VideoListProps {
  videos: Video[];
}

const VideoList: React.FC<VideoListProps> = ({ videos }) => {
  if (videos.length === 0) {
    return <div>No videos found.</div>;
  }

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "1.5rem", justifyContent: "center" }}>
      {videos.map((video) => (
        <div
          key={video.id}
          className="glass-card"
          style={{
            width: 340,
            padding: 16,
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <a href={video.video_url} target="_blank" rel="noopener noreferrer">
            <img
              src={video.thumbnails.high?.url || video.thumbnails.default?.url}
              alt={video.title}
              style={{ width: "100%", borderRadius: 8, marginBottom: 8, background: "#000" }}
            />
          </a>
          <h3 style={{ fontSize: "1.1rem", margin: "0.5rem 0", color: "var(--accent)" }}>{video.title}</h3>
          <div style={{ fontSize: "0.9rem", color: "var(--text-muted)" }}>
            {new Date(video.published_at).toLocaleString()}
          </div>
          <p style={{ fontSize: "0.97rem", margin: "0.5rem 0", color: "var(--text)" }}>
            {video.description}
          </p>
          <a href={video.video_url} target="_blank" rel="noopener noreferrer" style={{ color: "var(--accent)" }}>
            ▶ Watch on YouTube
          </a>
        </div>
      ))}
    </div>
  );
};

export default VideoList;
