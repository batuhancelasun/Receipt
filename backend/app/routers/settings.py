"""
Settings router for app configuration
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from bson import ObjectId

from ..schemas import SettingsUpdate, SettingsResponse, CategoryCreate, CategoryUpdate, CategoryResponse
from ..services.auth import get_current_user_id
from ..services.database import get_collection
from ..services.ai_scanner import get_scanner

router = APIRouter()


def _parse_iso_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


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
    
    # Update settings - use $setOnInsert to set user_id on new docs
    result = await settings_collection.find_one_and_update(
        {"user_id": user_id},
        {
            "$set": update_doc,
            "$setOnInsert": {"user_id": user_id}
        },
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


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    updates: CategoryUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a category"""
    categories_collection = await get_collection("categories")
    
    update_doc = {}
    if updates.name is not None:
        update_doc["name"] = updates.name
    if updates.icon is not None:
        update_doc["icon"] = updates.icon
    if updates.color is not None:
        update_doc["color"] = updates.color
    
    if not update_doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No updates provided"
        )
    
    result = await categories_collection.find_one_and_update(
        {"_id": ObjectId(category_id), "user_id": user_id},
        {"$set": update_doc},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return CategoryResponse(
        id=str(result["_id"]),
        name=result["name"],
        icon=result["icon"],
        color=result["color"],
        type=result["type"]
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


@router.get("/export")
async def export_user_data(user_id: str = Depends(get_current_user_id)):
    """Export user settings, categories, and transactions as JSON"""
    settings_collection = await get_collection("settings")
    categories_collection = await get_collection("categories")
    transactions_collection = await get_collection("transactions")

    settings = await settings_collection.find_one({"user_id": user_id}) or {}
    export_settings = {
        "default_currency": settings.get("default_currency", "€"),
        "theme": settings.get("theme", "dark"),
        "budget_alerts": settings.get("budget_alerts", True),
        "monthly_budget": settings.get("monthly_budget")
    }

    categories = []
    categories_cursor = categories_collection.find({"user_id": user_id})
    async for cat in categories_cursor:
        categories.append({
            "id": str(cat["_id"]),
            "name": cat["name"],
            "icon": cat.get("icon"),
            "color": cat.get("color"),
            "type": cat.get("type")
        })

    transactions = []
    txn_cursor = transactions_collection.find({"user_id": user_id})
    async for txn in txn_cursor:
        transactions.append({
            "id": str(txn["_id"]),
            "type": txn.get("type"),
            "amount": txn.get("amount"),
            "currency": txn.get("currency", "€"),
            "category_id": str(txn.get("category_id")) if txn.get("category_id") else None,
            "category_name": txn.get("category_name"),
            "merchant_name": txn.get("merchant_name"),
            "description": txn.get("description"),
            "date": txn.get("date").isoformat() if isinstance(txn.get("date"), datetime) else txn.get("date"),
            "items": txn.get("items", []),
            "tags": txn.get("tags", []),
            "is_recurring": txn.get("is_recurring", False),
            "recurring_frequency": txn.get("recurring_frequency"),
            "recurring_interval": txn.get("recurring_interval", 1),
            "recurring_end_date": txn.get("recurring_end_date").isoformat() if isinstance(txn.get("recurring_end_date"), datetime) else txn.get("recurring_end_date"),
            "created_at": txn.get("created_at").isoformat() if isinstance(txn.get("created_at"), datetime) else None,
            "updated_at": txn.get("updated_at").isoformat() if isinstance(txn.get("updated_at"), datetime) else None
        })

    return {
        "exported_at": datetime.utcnow().isoformat(),
        "settings": export_settings,
        "categories": categories,
        "transactions": transactions
    }


@router.post("/import")
async def import_user_data(
    payload: dict,
    mode: str = Query("replace", pattern="^(replace|merge)$"),
    user_id: str = Depends(get_current_user_id)
):
    """Import user settings, categories, and transactions"""
    settings_collection = await get_collection("settings")
    categories_collection = await get_collection("categories")
    transactions_collection = await get_collection("transactions")

    settings = payload.get("settings", {})
    categories = payload.get("categories", [])
    transactions = payload.get("transactions", [])

    if mode == "replace":
        await transactions_collection.delete_many({"user_id": user_id})
        await categories_collection.delete_many({"user_id": user_id})

    await settings_collection.find_one_and_update(
        {"user_id": user_id},
        {
            "$set": {
                "default_currency": settings.get("default_currency", "€"),
                "theme": settings.get("theme", "dark"),
                "budget_alerts": settings.get("budget_alerts", True),
                "monthly_budget": settings.get("monthly_budget")
            },
            "$setOnInsert": {"user_id": user_id}
        },
        upsert=True,
        return_document=True
    )

    category_id_map = {}
    for cat in categories:
        cat_doc = {
            "user_id": user_id,
            "name": cat.get("name"),
            "icon": cat.get("icon"),
            "color": cat.get("color"),
            "type": cat.get("type")
        }
        result = await categories_collection.insert_one(cat_doc)
        if cat.get("id"):
            category_id_map[str(cat.get("id"))] = str(result.inserted_id)

    imported_txn_count = 0
    for txn in transactions:
        txn_date = _parse_iso_datetime(txn.get("date"))
        if not txn_date:
            continue
        recurring_end = _parse_iso_datetime(txn.get("recurring_end_date"))
        created_at = _parse_iso_datetime(txn.get("created_at")) or datetime.utcnow()
        updated_at = _parse_iso_datetime(txn.get("updated_at")) or datetime.utcnow()

        category_id = txn.get("category_id")
        mapped_category_id = category_id_map.get(str(category_id)) if category_id else None

        txn_doc = {
            "user_id": user_id,
            "type": txn.get("type"),
            "amount": float(txn.get("amount", 0)),
            "currency": txn.get("currency", "€"),
            "category_id": mapped_category_id,
            "category_name": txn.get("category_name"),
            "merchant_name": txn.get("merchant_name"),
            "description": txn.get("description"),
            "date": txn_date,
            "items": txn.get("items", []),
            "tags": txn.get("tags", []),
            "is_recurring": bool(txn.get("is_recurring", False)),
            "recurring_frequency": txn.get("recurring_frequency"),
            "recurring_interval": int(txn.get("recurring_interval", 1)),
            "recurring_end_date": recurring_end,
            "created_at": created_at,
            "updated_at": updated_at
        }
        await transactions_collection.insert_one(txn_doc)
        imported_txn_count += 1

    return {
        "status": "ok",
        "categories_imported": len(categories),
        "transactions_imported": imported_txn_count,
        "mode": mode
    }
