# YouTube Scraper

A scalable, production-ready FastAPI backend for fetching, storing, and searching the latest YouTube videos by tag/search query, with robust background fetching, multi-key quota management, and a modular, maintainable architecture.

## Features

- **Async background fetcher:** Periodically polls the YouTube Data API for the latest videos matching a configurable search query/tag, using multiple API keys for quota failover.
- **PostgreSQL database:** Stores video data with proper indexes for efficient retrieval and search.
- **Paginated API:** `/videos` endpoint returns videos in reverse chronological order, paginated.
- **Advanced Search API:** `/search` endpoint allows searching by title and description, supporting partial, out-of-order, and multi-word matching.
- **Dockerized deployment:** Includes `Dockerfile` and `docker-compose.yml` for easy setup.
- **Highly modular codebase:** Clean separation of concerns (db, services, routes, errors, exceptions).
- **Robust error handling:** Centralized error constants and global exception handlers.
- **Fully documented code and API.**

## Directory Structure

```
.
├── app/
│   ├── db/                # Database models, schemas, CRUD, connection
│   ├── services/          # Business logic/service layer
│   ├── routes/            # API route definitions
│   ├── errors/            # Error message constants
│   ├── exceptions/        # Exception handler functions
│   ├── youtube_fetcher.py # Background YouTube fetcher
├── main.py                # FastAPI entrypoint
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

## Backend Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-directory>
```

### 2. Configure environment variables

`.env` and fill in your values:

```env
YOUTUBE_API_KEYS=YOUR_API_KEY_1,YOUR_API_KEY_2
YOUTUBE_SEARCH_QUERY=news
YOUTUBE_FETCH_INTERVAL=600
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/youtube
```

- You can supply multiple API keys, comma-separated, for quota failover.

### 3. Run with Docker (recommended)

```bash
docker-compose up --build
```

- The API will be available at [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Run locally (without Docker)

- Ensure PostgreSQL is running and matches your `DATABASE_URL`.
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Start the server:

```bash
uvicorn main:app --reload
```

---

## Frontend (Dashboard) Setup

### 1. Install dependencies

```bash
cd dashboard
npm install
```

### 2. Configure API base URL (optional)

By default, the dashboard expects the backend at `http://localhost:8000`.  
To change this, create a `.env` file in the `dashboard/` directory:

```
REACT_APP_API_BASE=http://localhost:8000
```

### 3. Run the dashboard in development

```bash
npm start
```

- The dashboard will be available at [http://localhost:3000](http://localhost:3000)
- It will auto-reload on code changes.

### 4. Build for production

```bash
npm run build
```

- This will create a production-ready build in `dashboard/build/`.

---

## Running Backend and Frontend Together

- Start the backend (with Docker or locally) so the API is available at `http://localhost:8000`.
- Start the dashboard with `npm start` in the `dashboard/` directory.
- The dashboard will communicate with the backend via REST API, with CORS enabled.


## Backend Optimization Suggestions

- **Distributed Locking:** Use Redis with the Redlock algorithm to ensure only one instance fetches from the YouTube API at a time in a multi-instance deployment.
- **Rate Limiting:** Implement rate limiting on API endpoints to prevent abuse and accidental quota exhaustion.
- **API Key Rotation:** Track quota usage for each YouTube API key and rotate keys automatically when limits are reached.
- **Caching:** Use Redis or another in-memory cache for frequently accessed video/search results to reduce database load.
- **Asynchronous Task Queue:** Offload heavy or periodic tasks to a distributed task queue (e.g., Celery with Redis/RabbitMQ) for robust background processing.
- **Database Indexing:** Regularly review and optimize database indexes for search and retrieval patterns.


## API Usage

### Get latest videos (paginated)

```
GET /videos?page=1&page_size=20
```

### Search videos (partial, multi-word, out-of-order)

```
GET /search?q=how tea&page=1&page_size=10
```

### Health check

```
GET /
```

## Environment Variables

- `YOUTUBE_API_KEYS`: Comma-separated list of YouTube Data API v3 keys.
- `YOUTUBE_SEARCH_QUERY`: Search query/tag for fetching videos.
- `YOUTUBE_FETCH_INTERVAL`: Fetch interval in seconds (default: 600).
- `DATABASE_URL`: PostgreSQL connection string.

## Adding API Keys

- Get your API keys from the [Google Cloud Console](https://console.cloud.google.com/).
- Enable the YouTube Data API v3 for your project.
- Add multiple keys in `.env` as `YOUTUBE_API_KEYS=key1,key2,key3`.
