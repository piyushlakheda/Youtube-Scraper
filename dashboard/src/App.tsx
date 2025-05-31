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
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 24 }}>
      <h1>YouTube Video Dashboard</h1>
      <form onSubmit={handleSearch} style={{ marginBottom: 16 }}>
        <input
          type="text"
          placeholder="Search videos..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          style={{ padding: 8, fontSize: 16, width: 300 }}
        />
        <button type="submit" style={{ marginLeft: 8, padding: "8px 16px" }}>
          Search
        </button>
        <select
          value={sort}
          onChange={handleSortChange}
          style={{ marginLeft: 16, padding: 8, fontSize: 16 }}
        >
          <option value="date">Sort by Date</option>
          <option value="title">Sort by Title</option>
        </select>
      </form>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          <VideoList videos={videos} />
          <div style={{ marginTop: 24, textAlign: "center" }}>
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              style={{ marginRight: 8, padding: "8px 16px" }}
            >
              Previous
            </button>
            <span>
              Page {page} of {Math.ceil(total / PAGE_SIZE) || 1}
            </span>
            <button
              onClick={() => setPage((p) => (p * PAGE_SIZE < total ? p + 1 : p))}
              disabled={page * PAGE_SIZE >= total}
              style={{ marginLeft: 8, padding: "8px 16px" }}
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
