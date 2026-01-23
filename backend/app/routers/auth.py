"""
Authentication router for user registration and login
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from bson import ObjectId

from ..schemas import UserCreate, UserLogin, Token
from ..services.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user_id
)
from ..services.database import get_collection

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user
    
    Creates a new user account with hashed password and returns JWT token
    """
    users_collection = await get_collection("users")
    
    # Check if username already exists
    existing_user = await users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = await users_collection.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Create default settings for user
    settings_collection = await get_collection("settings")
    await settings_collection.insert_one({
        "user_id": user_id,
        "default_currency": "€",
        "theme": "dark",
        "budget_alerts": True
    })
    
    # Create default categories
    categories_collection = await get_collection("categories")
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
        cat["user_id"] = user_id
    
    await categories_collection.insert_many(default_categories)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with username and password
    
    Returns JWT access token on successful authentication
    """
    users_collection = await get_collection("users")
    
    # Find user
    user = await users_collection.find_one({"username": credentials.username})
    
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    user_id = str(user["_id"])
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """
    Get current authenticated user information
    """
    users_collection = await get_collection("users")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }
