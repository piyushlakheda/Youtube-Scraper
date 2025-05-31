from fastapi import FastAPI, Depends, Query, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.db.database import engine, Base, get_db, AsyncSessionLocal
from app.youtube_fetcher import youtube_fetcher_loop
from app.exceptions.exception_handlers import (
    http_error_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.routes.routes import router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Start background fetcher, pass sessionmaker
    loop = asyncio.get_event_loop()
    loop.create_task(youtube_fetcher_loop(AsyncSessionLocal))
    yield

app = FastAPI(
    title="YouTube Latest Videos API",
    description="Fetches and serves latest YouTube videos for a given search query.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
