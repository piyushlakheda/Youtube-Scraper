import React, { useEffect, useState } from "react";
import VideoList from "./components/VideoList";
import { getVideos, searchVideos } from "./api";
import { Video } from "./types";

const PAGE_SIZE = 12;

function App() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [query, setQuery] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sort, setSort] = useState<"date" | "title">("date");

  useEffect(() => {
    setLoading(true);
    const fetch = async () => {
      try {
        if (query.trim()) {
          const res = await searchVideos(query, page, PAGE_SIZE);
          let vids = res.videos;
          if (sort === "title") {
            vids = [...vids].sort((a, b) => a.title.localeCompare(b.title));
          }
          setVideos(vids);
          setTotal(res.total);
        } else {
          const res = await getVideos(page, PAGE_SIZE);
          let vids = res.videos;
          if (sort === "title") {
            vids = [...vids].sort((a, b) => a.title.localeCompare(b.title));
          }
          setVideos(vids);
          setTotal(res.total);
        }
      } catch (e) {
        setVideos([]);
        setTotal(0);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, [page, query, sort]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    setQuery(searchInput.trim());
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSort(e.target.value as "date" | "title");
  };

  return (
    <div style={{ maxWidth: 1300, margin: "0 auto", padding: 32 }}>
      <h1 style={{ textAlign: "center", letterSpacing: 1.5 }}>YouTube Video Dashboard</h1>
      <form
        onSubmit={handleSearch}
        style={{
          margin: "0 auto 24px auto",
          background: "var(--card-bg)",
          borderRadius: 12,
          boxShadow: "var(--shadow)",
          padding: 24,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 16,
          maxWidth: 700,
        }}
      >
        <input
          type="text"
          placeholder="Search videos..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          style={{ width: 320 }}
        />
        <button type="submit">Search</button>
        <select value={sort} onChange={handleSortChange}>
          <option value="date">Sort by Date</option>
          <option value="title">Sort by Title</option>
        </select>
      </form>
      {loading ? (
        <div style={{ textAlign: "center", color: "var(--accent)", fontSize: 22, marginTop: 40 }}>
          Loading...
        </div>
      ) : (
        <>
          <VideoList videos={videos} />
          <div style={{ marginTop: 32, textAlign: "center" }}>
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              Previous
            </button>
            <span style={{ margin: "0 18px", fontWeight: 500, color: "var(--accent)" }}>
              Page {page} of {Math.ceil(total / PAGE_SIZE) || 1}
            </span>
            <button
              onClick={() => setPage((p) => (p * PAGE_SIZE < total ? p + 1 : p))}
              disabled={page * PAGE_SIZE >= total}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
