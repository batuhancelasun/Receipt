"""
Database connection management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
db = Database()

async def get_database():
    """Get database instance"""
    return db.client[os.getenv("MONGODB_DB_NAME", "receipt_tracker")]

async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(mongo_url)
    print(f"✓ Connected to MongoDB at {mongo_url}")

async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    if db.client:
        db.client.close()
        print("✓ Closed MongoDB connection")

# Collection helpers
async def get_collection(collection_name: str):
    """Get a collection from the database"""
    database = await get_database()
    return database[collection_name]
