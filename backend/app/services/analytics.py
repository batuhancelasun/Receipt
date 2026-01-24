"""
Analytics service for generating financial insights
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
from collections import defaultdict


async def calculate_period_stats(
    transactions: List[Dict],
    start_date: datetime,
    end_date: datetime
) -> Dict[str, Any]:
    """
    Calculate statistics for a given period
    
    Args:
        transactions: List of transaction documents
        start_date: Period start
        end_date: Period end
        
    Returns:
        Dictionary with income, expenses, and net calculations
    """
    total_income = 0.0
    total_expenses = 0.0
    transaction_count = 0
    
    for txn in transactions:
        txn_date = txn.get("date")
        if start_date <= txn_date <= end_date:
            transaction_count += 1
            amount = txn.get("amount", 0)
            if txn.get("type") == "income":
                total_income += amount
            else:
                total_expenses += amount
    
    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net": round(total_income - total_expenses, 2),
        "transaction_count": transaction_count
    }


async def calculate_category_breakdown(
    transactions: List[Dict],
    transaction_type: str,
    start_date: datetime,
    end_date: datetime,
    categories: Dict[str, Dict]
) -> List[Dict[str, Any]]:
    """
    Calculate spending/income breakdown by category
    
    Args:
        transactions: List of transaction documents
        transaction_type: "expense" or "income"
        start_date: Period start
        end_date: Period end
        categories: Dictionary mapping category_id to category data
        
    Returns:
        List of category breakdowns with amounts and percentages
    """
    category_totals = defaultdict(float)
    total = 0.0
    
    # Calculate totals per category
    for txn in transactions:
        if txn.get("type") != transaction_type:
            continue
        
        txn_date = txn.get("date")
        if start_date <= txn_date <= end_date:
            amount = txn.get("amount", 0)
            category_id = txn.get("category_id", "uncategorized")
            category_totals[category_id] += amount
            total += amount
    
    # Build breakdown with percentages
    breakdown = []
    for category_id, amount in category_totals.items():
        category_data = categories.get(category_id, {})
        percentage = (amount / total * 100) if total > 0 else 0
        
        breakdown.append({
            "category_id": category_id if category_id != "uncategorized" else None,
            "category_name": category_data.get("name", "Uncategorized"),
            "amount": round(amount, 2),
            "percentage": round(percentage, 2),
            "color": category_data.get("color", "#6B7280")
        })
    
    # Sort by amount descending
    breakdown.sort(key=lambda x: x["amount"], reverse=True)
    return breakdown


def get_period_dates(
    period: str,
    year: int = None,
    month: int = None
) -> tuple[datetime, datetime]:
    """
    Get start and end dates for a period type
    
    Args:
        period: "daily", "monthly", "yearly", or "all"
        year: Optional specific year
        month: Optional specific month (1-12)
        
    Returns:
        Tuple of (start_date, end_date)
    """
    now = datetime.utcnow()
    target_year = year if year is not None else now.year
    target_month = month if month is not None else now.month
    
    if period == "daily":
        # For daily, we stick to "today" unless we implement a date picker.
        # But if year/month are passed without day, it doesn't make sense for "daily".
        # We'll just ignore year/month for daily for now or assume today.
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == "monthly":
        start = datetime(target_year, target_month, 1)
        # Get last day of month
        if target_month == 12:
            end = datetime(target_year + 1, 1, 1) - timedelta(days=1)
        else:
            end = datetime(target_year, target_month + 1, 1) - timedelta(days=1)
        end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == "yearly":
        start = datetime(target_year, 1, 1)
        end = datetime(target_year, 12, 31, 23, 59, 59, 999999)
    else:  # all
        start = datetime(2000, 1, 1)
        end = datetime(2100, 12, 31, 23, 59, 59)
    
    return start, end
