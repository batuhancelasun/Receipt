"""
Initialization script to create admin user on startup
"""
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_admin_user():
    """Create admin user from environment variables if not exists"""
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@receipt.local")
    
    if not admin_username or not admin_password:
        print("⚠️  No admin credentials provided in environment variables")
        return
    
    # Connect to MongoDB
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "receipt_tracker")
    
    client = AsyncIOMotorClient(mongodb_url)
    db = client[db_name]
    users_collection = db["users"]
    
    # Check if admin already exists
    existing_admin = await users_collection.find_one({"username": admin_username})
    
    if existing_admin:
        print(f"✓ Admin user '{admin_username}' already exists")
        client.close()
        return
    
    # Create admin user
    hashed_password = pwd_context.hash(admin_password)
    admin_doc = {
        "username": admin_username,
        "email": admin_email,
        "hashed_password": hashed_password,
        "is_admin": True,
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(admin_doc)
    admin_id = str(result.inserted_id)
    
    # Create default settings
    settings_collection = db["settings"]
    await settings_collection.insert_one({
        "user_id": admin_id,
        "default_currency": "€",
        "theme": "dark",
        "budget_alerts": True
    })
    
    # Create default categories
    categories_collection = db["categories"]
    default_categories = [
        {"name": "Food & Dining", "icon": "🍔", "color": "#EF4444", "type": "expense"},
        {"name": "Transportation", "icon": "🚗", "color": "#F59E0B", "type": "expense"},
        {"name": "Shopping", "icon": "🛍️", "color": "#8B5CF6", "type": "expense"},
        {"name": "Entertainment", "icon": "🎬", "color": "#EC4899", "type": "expense"},
        {"name": "Bills & Utilities", "icon": "💡", "color": "#6366F1", "type": "expense"},
        {"name": "Salary", "icon": "💰", "color": "#10B981", "type": "income"},
        {"name": "Other Income", "icon": "💵", "color": "#14B8A6", "type": "income"},
    ]
    
    for cat in default_categories:
        cat["user_id"] = admin_id
    
    await categories_collection.insert_many(default_categories)
    
    print(f"✓ Created admin user: {admin_username}")
    client.close()


if __name__ == "__main__":
    asyncio.run(create_admin_user())
