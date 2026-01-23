"""
Receipt Tracker - FastAPI Backend
Serves both the Vue.js frontend and REST API endpoints
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

# API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(receipts.router, prefix="/api/receipts", tags=["Receipts"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "service": "receipt-tracker"}

# Serve Vue.js static files (built frontend)
# This will be mounted after the Docker build copies the dist folder
if os.path.exists("/app/static"):
    app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")
