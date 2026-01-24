"""
Transactions router for CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from bson import ObjectId
from typing import Optional, List

from ..schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    AnalyticsResponse,
    PeriodStats,
    CategoryBreakdown
)
from ..services.auth import get_current_user_id
from ..services.database import get_collection
from ..services.analytics import (
    calculate_period_stats,
    calculate_category_breakdown,
    get_period_dates
)

router = APIRouter()


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    user_id: str = Depends(get_current_user_id)
):
    """
    Create a new transaction manually or from receipt scan
    """
    transactions_collection = await get_collection("transactions")
    categories_collection = await get_collection("categories")
    
    # Get category name if category_id provided
    category_name = None
    if transaction.category_id:
        category = await categories_collection.find_one({"_id": ObjectId(transaction.category_id)})
        if category:
            category_name = category["name"]
    
    # Build transaction document
    txn_doc = {
        "user_id": user_id,
        "type": transaction.type,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "category_id": transaction.category_id,
        "category_name": category_name,
        "merchant_name": transaction.merchant_name,
        "description": transaction.description,
        "date": transaction.date,
        "items": [item.dict() for item in transaction.items] if transaction.items else [],
        "tags": transaction.tags,
        "is_recurring": transaction.is_recurring,
        "recurring_frequency": transaction.recurring_frequency,
        "recurring_interval": transaction.recurring_interval,
        "recurring_end_date": transaction.recurring_end_date,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await transactions_collection.insert_one(txn_doc)
    txn_doc["_id"] = result.inserted_id
    
    return TransactionResponse(
        id=str(txn_doc["_id"]),
        type=txn_doc["type"],
        amount=txn_doc["amount"],
        currency=txn_doc["currency"],
        category_id=txn_doc.get("category_id"),
        category_name=txn_doc.get("category_name"),
        merchant_name=txn_doc.get("merchant_name"),
        description=txn_doc.get("description"),
        date=txn_doc["date"],
        items=txn_doc.get("items", []),
        tags=txn_doc.get("tags", []),
        is_recurring=txn_doc["is_recurring"],
        recurring_frequency=txn_doc.get("recurring_frequency"),
        recurring_interval=txn_doc.get("recurring_interval", 1),
        recurring_end_date=txn_doc.get("recurring_end_date"),
        created_at=txn_doc["created_at"],
        updated_at=txn_doc["updated_at"]
    )


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    user_id: str = Depends(get_current_user_id),
    transaction_type: Optional[str] = Query(None, regex="^(expense|income)$"),
    category_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    List transactions with optional filters
    """
    transactions_collection = await get_collection("transactions")
    
    # Build query
    query = {"user_id": user_id}
    if transaction_type:
        query["type"] = transaction_type
    if category_id:
        query["category_id"] = category_id
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = start_date
        if end_date:
            date_query["$lte"] = end_date
        query["date"] = date_query
    
    # Execute query
    cursor = transactions_collection.find(query) \
        .sort("date", -1) \
        .skip(skip) \
        .limit(limit)
    
    transactions = []
    async for txn in cursor:
        transactions.append(TransactionResponse(
            id=str(txn["_id"]),
            type=txn["type"],
            amount=txn["amount"],
            currency=txn.get("currency", "€"),
            category_id=txn.get("category_id"),
            category_name=txn.get("category_name"),
            merchant_name=txn.get("merchant_name"),
            description=txn.get("description"),
            date=txn["date"],
            items=txn.get("items", []),
            receipt_id=txn.get("receipt_id"),
            tags=txn.get("tags", []),
            is_recurring=txn.get("is_recurring", False),
            recurring_frequency=txn.get("recurring_frequency"),
            recurring_interval=txn.get("recurring_interval", 1),
            recurring_end_date=txn.get("recurring_end_date"),
            created_at=txn["created_at"],
            updated_at=txn["updated_at"]
        ))
    
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific transaction"""
    transactions_collection = await get_collection("transactions")
    
    txn = await transactions_collection.find_one({
        "_id": ObjectId(transaction_id),
        "user_id": user_id
    })
    
    if not txn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return TransactionResponse(
        id=str(txn["_id"]),
        type=txn["type"],
        amount=txn["amount"],
        currency=txn.get("currency", "€"),
        category_id=txn.get("category_id"),
        category_name=txn.get("category_name"),
        merchant_name=txn.get("merchant_name"),
        description=txn.get("description"),
        date=txn["date"],
        items=txn.get("items", []),
        receipt_id=txn.get("receipt_id"),
        tags=txn.get("tags", []),
        is_recurring=txn.get("is_recurring", False),
        recurring_frequency=txn.get("recurring_frequency"),
        recurring_interval=txn.get("recurring_interval", 1),
        recurring_end_date=txn.get("recurring_end_date"),
        created_at=txn["created_at"],
        updated_at=txn["updated_at"]
    )


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    updates: TransactionUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a transaction"""
    transactions_collection = await get_collection("transactions")
    
    # Build update document
    update_doc = {"updated_at": datetime.utcnow()}
    if updates.type is not None:
        update_doc["type"] = updates.type
    if updates.amount is not None:
        update_doc["amount"] = updates.amount
    if updates.currency is not None:
        update_doc["currency"] = updates.currency
    if updates.category_id is not None:
        update_doc["category_id"] = updates.category_id
        # Update category name
        categories_collection = await get_collection("categories")
        category = await categories_collection.find_one({"_id": ObjectId(updates.category_id)})
        if category:
            update_doc["category_name"] = category["name"]
    if updates.merchant_name is not None:
        update_doc["merchant_name"] = updates.merchant_name
    if updates.description is not None:
        update_doc["description"] = updates.description
    if updates.date is not None:
        update_doc["date"] = updates.date
    if updates.items is not None:
        update_doc["items"] = [item.dict() for item in updates.items]
    if updates.tags is not None:
        update_doc["tags"] = updates.tags
    if updates.is_recurring is not None:
        update_doc["is_recurring"] = updates.is_recurring
    if updates.recurring_frequency is not None:
        update_doc["recurring_frequency"] = updates.recurring_frequency
    if updates.recurring_interval is not None:
        update_doc["recurring_interval"] = updates.recurring_interval
    if updates.recurring_end_date is not None:
        update_doc["recurring_end_date"] = updates.recurring_end_date
    
    # Update transaction
    result = await transactions_collection.find_one_and_update(
        {"_id": ObjectId(transaction_id), "user_id": user_id},
        {"$set": update_doc},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return TransactionResponse(
        id=str(result["_id"]),
        type=result["type"],
        amount=result["amount"],
        currency=result.get("currency", "€"),
        category_id=result.get("category_id"),
        category_name=result.get("category_name"),
        merchant_name=result.get("merchant_name"),
        description=result.get("description"),
        date=result["date"],
        items=result.get("items", []),
        receipt_id=result.get("receipt_id"),
        tags=result.get("tags", []),
        is_recurring=result.get("is_recurring", False),
        recurring_frequency=result.get("recurring_frequency"),
        recurring_interval=result.get("recurring_interval", 1),
        recurring_end_date=result.get("recurring_end_date"),
        created_at=result["created_at"],
        updated_at=result["updated_at"]
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a transaction"""
    transactions_collection = await get_collection("transactions")
    
    result = await transactions_collection.delete_one({
        "_id": ObjectId(transaction_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )


@router.get("/analytics/{period}", response_model=AnalyticsResponse)
async def get_analytics(
    period: str,
    year: Optional[int] = Query(None, ge=2000, le=2100),
    month: Optional[int] = Query(None, ge=1, le=12),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get analytics for a period (daily, monthly, yearly)
    """
    if period not in ["daily", "monthly", "yearly", "all"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Period must be 'daily', 'monthly', 'yearly', or 'all'"
        )
    
    transactions_collection = await get_collection("transactions")
    categories_collection = await get_collection("categories")
    
    # Get date range
    start_date, end_date = get_period_dates(period, year, month)
    
    # Get all transactions in period
    cursor = transactions_collection.find({
        "user_id": user_id,
        "date": {"$gte": start_date, "$lte": end_date}
    })
    transactions = await cursor.to_list(length=None)
    
    # Get categories for mapping
    categories_cursor = categories_collection.find({"user_id": user_id})
    categories = {}
    async for cat in categories_cursor:
        categories[str(cat["_id"])] = cat
    
    # Calculate stats
    stats = await calculate_period_stats(transactions, start_date, end_date)
    expense_breakdown = await calculate_category_breakdown(
        transactions, "expense", start_date, end_date, categories
    )
    income_breakdown = await calculate_category_breakdown(
        transactions, "income", start_date, end_date, categories
    )
    
    return AnalyticsResponse(
        period=period,
        stats=PeriodStats(**stats),
        expense_breakdown=[CategoryBreakdown(**item) for item in expense_breakdown],
        income_breakdown=[CategoryBreakdown(**item) for item in income_breakdown]
    )
