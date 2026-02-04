"""
Notifications router for in-app reminders
"""
from datetime import datetime, timedelta, date
import calendar
from fastapi import APIRouter, Depends, Query

from ..services.auth import get_current_user_id
from ..services.database import get_collection

router = APIRouter()


def format_date_ddmmyyyy(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def add_months(base: date, months: int) -> date:
    year = base.year + (base.month - 1 + months) // 12
    month = (base.month - 1 + months) % 12 + 1
    day = min(base.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def add_years(base: date, years: int) -> date:
    year = base.year + years
    day = min(base.day, calendar.monthrange(year, base.month)[1])
    return date(year, base.month, day)


def next_occurrence(base: date, frequency: str, interval: int, today: date) -> date | None:
    if interval <= 0:
        return None
    if base >= today:
        return base

    if frequency == "daily":
        days_diff = (today - base).days
        steps = (days_diff + interval - 1) // interval
        return base + timedelta(days=steps * interval)

    if frequency == "weekly":
        step_days = 7 * interval
        days_diff = (today - base).days
        steps = (days_diff + step_days - 1) // step_days
        return base + timedelta(days=steps * step_days)

    if frequency == "monthly":
        months_diff = (today.year - base.year) * 12 + (today.month - base.month)
        steps = months_diff // interval
        candidate = add_months(base, steps * interval)
        if candidate < today:
            candidate = add_months(base, (steps + 1) * interval)
        return candidate

    if frequency == "yearly":
        years_diff = today.year - base.year
        steps = years_diff // interval
        candidate = add_years(base, steps * interval)
        if candidate < today:
            candidate = add_years(base, (steps + 1) * interval)
        return candidate

    return None


@router.get("")
async def list_notifications(
    days: int = Query(3, ge=0, le=60),
    user_id: str = Depends(get_current_user_id)
):
    """
    In-app notifications for upcoming recurring and one-off transactions.
    """
    transactions_collection = await get_collection("transactions")
    # Use UTC for consistency
    now = datetime.utcnow()
    today = now.date()
    # Ensure current date is used for range
    latest_date = today + timedelta(days=days)
    
    # Define the start of today and end of latest date as a datetime for comparison if needed
    today_dt = datetime.combine(today, datetime.min.time())
    latest_dt = datetime.combine(latest_date, datetime.max.time())

    # Fetch recurring transactions OR one-off transactions in the future range
    cursor = transactions_collection.find({
        "user_id": user_id,
        "$or": [
            {"is_recurring": True},
            {
                "is_recurring": {"$ne": True},
                "date": {"$gte": today_dt, "$lte": latest_dt}
            }
        ]
    })

    notifications = []
    async for txn in cursor:
        is_recurring = txn.get("is_recurring", False)
        base_date = txn.get("date")
        if not base_date:
            continue
            
        # Standardize to date object
        txn_date = base_date.date() if isinstance(base_date, datetime) else base_date

        target_date = None
        if is_recurring:
            frequency = txn.get("recurring_frequency")
            interval = txn.get("recurring_interval", 1)
            if not frequency:
                continue

            next_date = next_occurrence(txn_date, frequency, interval, today)
            if not next_date:
                continue

            end_date = txn.get("recurring_end_date")
            if end_date:
                end_day = end_date.date() if isinstance(end_date, datetime) else end_date
                if next_date > end_day:
                    continue

            if next_date > latest_date:
                continue
            
            target_date = next_date
        else:
            # One-off transaction already filtered by query, but let's be sure
            if txn_date < today or txn_date > latest_date:
                continue
            target_date = txn_date

        if not target_date:
            continue

        days_left = (target_date - today).days
        if days_left == 0:
            when_text = "today"
        elif days_left == 1:
            when_text = "tomorrow"
        else:
            when_text = f"in {days_left} days"

        amount = txn.get("amount", 0)
        currency = txn.get("currency", "€")
        title = txn.get("merchant_name") or txn.get("description") or "Transaction"
        
        if is_recurring:
            if txn.get("type") == "income":
                message = f"Upcoming income {when_text}: {title} {currency}{amount:.2f}"
            else:
                message = f"Upcoming payment {when_text}: {title} {currency}{amount:.2f}"
        else:
            if txn.get("type") == "income":
                message = f"One-off income {when_text}: {title} {currency}{amount:.2f}"
            else:
                message = f"One-off payment {when_text}: {title} {currency}{amount:.2f}"

        notifications.append({
            "id": f"{str(txn.get('_id'))}-{target_date.isoformat()}",
            "message": message,
            "time": format_date_ddmmyyyy(target_date),
            "date_sort": target_date.isoformat()
        })

    # Sort notifications by date (closest first)
    notifications.sort(key=lambda x: x["date_sort"])
    
    # Remove the sort key before returning
    for n in notifications:
        del n["date_sort"]
    
    return notifications
