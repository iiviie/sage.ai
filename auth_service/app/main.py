from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import get_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown.
    Initializes database on startup.
    """
    # Startup: Initialize database
    print("🚀 Starting up Sage Auth Service...")
    print("📦 Initializing database...")
    init_db()
    print("✅ Database initialized successfully")
    yield
    # Shutdown
    print("👋 Shutting down Sage Auth Service...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Authentication service for Sage.ai with Google OAuth2",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    Verifies database connectivity and service status.
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "service": "auth_service",
        "database": db_status,
        "environment": settings.ENVIRONMENT
    }
