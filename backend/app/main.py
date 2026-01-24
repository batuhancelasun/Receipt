"""
Receipt Tracker - FastAPI Backend
Serves both the Vue.js frontend and REST API endpoints
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import os

from .routers import receipts, transactions, settings, auth
from .services.database import connect_to_mongo, close_mongo_connection


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
    description="AI-powered receipt tracking with Gemini 2.0 Flash",
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

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "service": "receipt-tracker"}


# Mount static assets FIRST - before any catch-all route
# This ensures JS, CSS, images are served correctly
if os.path.exists("/app/static/assets"):
    app.mount("/assets", StaticFiles(directory="/app/static/assets"), name="assets")

# Serve favicon
@app.get("/favicon.ico")
async def favicon():
    favicon_path = "/app/static/favicon.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404, detail="Favicon not found")


# Root route - serve index.html
@app.get("/")
async def root():
    """Serve Vue.js SPA root"""
    index_path = "/app/static/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not built yet"}


# SPA fallback - serve index.html for all other client-side routes
# This MUST be the last route definition
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve Vue.js SPA for all non-API routes"""
    index_path = "/app/static/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # Fallback for development
    return {"message": "Frontend not built yet"}
