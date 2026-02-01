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


@router.get("/")
async def list_notifications(
    days: int = Query(3, ge=0, le=60),
    user_id: str = Depends(get_current_user_id)
):
    """
    In-app notifications for upcoming recurring transactions.
    """
    transactions_collection = await get_collection("transactions")
    today = datetime.utcnow().date()
    latest_date = today + timedelta(days=days)

    cursor = transactions_collection.find({
        "user_id": user_id,
        "is_recurring": True
    })

    notifications = []
    async for txn in cursor:
        frequency = txn.get("recurring_frequency")
        interval = txn.get("recurring_interval", 1)
        if not frequency:
            continue

        base_date = txn.get("date")
        if not base_date:
            continue

        base_day = base_date.date() if isinstance(base_date, datetime) else base_date
        next_date = next_occurrence(base_day, frequency, interval, today)
        if not next_date:
            continue

        end_date = txn.get("recurring_end_date")
        if end_date:
            end_day = end_date.date() if isinstance(end_date, datetime) else end_date
            if next_date > end_day:
                continue

        if next_date > latest_date:
            continue

        days_left = (next_date - today).days
        if days_left == 0:
            when_text = "today"
        elif days_left == 1:
            when_text = "tomorrow"
        else:
            when_text = f"in {days_left} days"

        amount = txn.get("amount", 0)
        currency = txn.get("currency", "€")
        title = txn.get("merchant_name") or txn.get("description") or "Transaction"
        if txn.get("type") == "income":
            message = f"Upcoming income {when_text}: {title} {currency}{amount:.2f}"
        else:
            message = f"Upcoming payment {when_text}: {title} {currency}{amount:.2f}"

        notifications.append({
            "id": f"{str(txn.get('_id'))}-{next_date.isoformat()}",
            "message": message,
            "time": format_date_ddmmyyyy(next_date)
        })

    return notifications
