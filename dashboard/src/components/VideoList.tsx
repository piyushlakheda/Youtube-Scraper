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
    <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
      {videos.map((video) => (
        <div
          key={video.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: 8,
            width: 320,
            padding: 12,
            background: "#fff",
          }}
        >
          <a href={video.video_url} target="_blank" rel="noopener noreferrer">
            <img
              src={video.thumbnails.high?.url || video.thumbnails.default?.url}
              alt={video.title}
              style={{ width: "100%", borderRadius: 4 }}
            />
          </a>
          <h3 style={{ fontSize: "1.1rem", margin: "0.5rem 0" }}>{video.title}</h3>
          <div style={{ fontSize: "0.9rem", color: "#666" }}>
            {new Date(video.published_at).toLocaleString()}
          </div>
          <p style={{ fontSize: "0.95rem", margin: "0.5rem 0" }}>
            {video.description}
          </p>
          <a href={video.video_url} target="_blank" rel="noopener noreferrer">
            Watch on YouTube
          </a>
        </div>
      ))}
    </div>
  );
};

export default VideoList;
