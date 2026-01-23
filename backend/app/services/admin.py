"""
Admin-only utilities and dependencies
"""
from fastapi import HTTPException, status, Depends
from bson import ObjectId
from .database import get_collection
from .auth import get_current_user_id


async def get_current_admin_user_id(user_id: str = Depends(get_current_user_id)) -> str:
    """
    Dependency to ensure current user is an admin
    
    Args:
        user_id: Current authenticated user ID
        
    Returns:
        User ID if user is admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    users_collection = await get_collection("users")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user or not user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return user_id
