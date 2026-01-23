"""
Settings router for app configuration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from ..schemas import SettingsUpdate, SettingsResponse, CategoryCreate, CategoryResponse
from ..services.auth import get_current_user_id
from ..services.database import get_collection
from ..services.ai_scanner import get_scanner

router = APIRouter()


@router.get("/", response_model=SettingsResponse)
async def get_settings(user_id: str = Depends(get_current_user_id)):
    """Get user settings"""
    settings_collection = await get_collection("settings")
    
    settings = await settings_collection.find_one({"user_id": user_id})
    
    if not settings:
        # Create default settings if not exist
        settings = {
            "user_id": user_id,
            "default_currency": "€",
            "theme": "dark",
            "budget_alerts": True
        }
        await settings_collection.insert_one(settings)
    
    return SettingsResponse(
        default_currency=settings.get("default_currency", "€"),
        theme=settings.get("theme", "dark"),
        budget_alerts=settings.get("budget_alerts", True),
        monthly_budget=settings.get("monthly_budget"),
        has_gemini_api_key=bool(settings.get("gemini_api_key"))
    )


@router.put("/", response_model=SettingsResponse)
async def update_settings(
    updates: SettingsUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update user settings"""
    settings_collection = await get_collection("settings")
    
    update_doc = {}
    if updates.gemini_api_key is not None:
        update_doc["gemini_api_key"] = updates.gemini_api_key
        # Update AI scanner with new key
        scanner = get_scanner()
        scanner.set_api_key(updates.gemini_api_key)
    
    if updates.default_currency is not None:
        update_doc["default_currency"] = updates.default_currency
    if updates.theme is not None:
        update_doc["theme"] = updates.theme
    if updates.budget_alerts is not None:
        update_doc["budget_alerts"] = updates.budget_alerts
    if updates.monthly_budget is not None:
        update_doc["monthly_budget"] = updates.monthly_budget
    
    # Update settings
    result = await settings_collection.find_one_and_update(
        {"user_id": user_id},
        {"$set": update_doc},
        upsert=True,
        return_document=True
    )
    
    return SettingsResponse(
        default_currency=result.get("default_currency", "€"),
        theme=result.get("theme", "dark"),
        budget_alerts=result.get("budget_alerts", True),
        monthly_budget=result.get("monthly_budget"),
        has_gemini_api_key=bool(result.get("gemini_api_key"))
    )


# Category management endpoints
@router.get("/categories")
async def list_categories(user_id: str = Depends(get_current_user_id)):
    """List all categories for user"""
    categories_collection = await get_collection("categories")
    
    cursor = categories_collection.find({"user_id": user_id})
    categories = []
    async for cat in cursor:
        categories.append(CategoryResponse(
            id=str(cat["_id"]),
            name=cat["name"],
            icon=cat["icon"],
            color=cat["color"],
            type=cat["type"]
        ))
    
    return categories


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new category"""
    categories_collection = await get_collection("categories")
    
    category_doc = {
        "user_id": user_id,
        "name": category.name,
        "icon": category.icon,
        "color": category.color,
        "type": category.type
    }
    
    result = await categories_collection.insert_one(category_doc)
    
    return CategoryResponse(
        id=str(result.inserted_id),
        name=category.name,
        icon=category.icon,
        color=category.color,
        type=category.type
    )


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a category"""
    categories_collection = await get_collection("categories")
    
    result = await categories_collection.delete_one({
        "_id": ObjectId(category_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
