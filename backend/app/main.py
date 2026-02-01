"""
Receipt Tracker - FastAPI Backend
Serves both the Vue.js frontend and REST API endpoints
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import os
from pathlib import Path

from .routers import receipts, transactions, settings, auth, notifications
from .services.database import connect_to_mongo, close_mongo_connection

# Static files directory
STATIC_DIR = Path("/app/static")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await connect_to_mongo()
    
    # Create admin user if environment variables are set
    from .init_admin import create_admin_user
    await create_admin_user()
    
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Receipt Tracker",
    description="AI-powered receipt tracking with Gemini 2.5 Flash Lite",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes - these take priority
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(receipts.router, prefix="/api/receipts", tags=["Receipts"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "service": "receipt-tracker"}


# Serve static files (JS, CSS, images, etc.)
# This must be done AFTER API routes
if STATIC_DIR.exists():
    # Mount the entire static directory at root for all static files
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


# Exception handler for 404 - serve index.html for SPA routes
@app.exception_handler(StarletteHTTPException)
async def custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # Check if this is an API request
        if request.url.path.startswith("/api/"):
            return HTMLResponse(
                content='{"detail": "Not Found"}',
                status_code=404,
                media_type="application/json"
            )
        
        # For non-API routes, serve the SPA index.html
        index_path = STATIC_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    
    # Re-raise the exception for other status codes
    return HTMLResponse(
        content=f'{{"detail": "{exc.detail}"}}',
        status_code=exc.status_code,
        media_type="application/json"
    )
