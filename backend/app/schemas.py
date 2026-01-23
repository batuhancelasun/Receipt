"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# Authentication Schemas
class UserCreate(BaseModel):
    """User registration schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


# Transaction Schemas
class TransactionItem(BaseModel):
    """Transaction item schema"""
    name: str
    quantity: float = 1.0
    unit_price: float
    total_price: float


class TransactionCreate(BaseModel):
    """Create transaction schema"""
    type: str = Field(..., pattern="^(expense|income)$")
    amount: float = Field(..., gt=0)
    currency: str = "€"
    category_id: Optional[str] = None
    merchant_name: Optional[str] = None
    description: Optional[str] = None
    date: datetime
    items: Optional[List[TransactionItem]] = []
    tags: List[str] = []
    is_recurring: bool = False


class TransactionUpdate(BaseModel):
    """Update transaction schema"""
    type: Optional[str] = Field(None, pattern="^(expense|income)$")
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    category_id: Optional[str] = None
    merchant_name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    items: Optional[List[TransactionItem]] = None
    tags: Optional[List[str]] = None
    is_recurring: Optional[bool] = None


class TransactionResponse(BaseModel):
    """Transaction response schema"""
    id: str
    type: str
    amount: float
    currency: str
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    merchant_name: Optional[str] = None
    description: Optional[str] = None
    date: datetime
    items: List[TransactionItem] = []
    receipt_id: Optional[str] = None
    tags: List[str] = []
    is_recurring: bool
    created_at: datetime
    updated_at: datetime


# Receipt Schemas
class ReceiptScanResponse(BaseModel):
    """Receipt scan response"""
    id: str
    filename: str
    scan_status: str
    ai_confidence: Optional[float] = None
    extracted_data: Optional[dict] = None
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None
    scanned_at: datetime


# Settings Schemas
class SettingsUpdate(BaseModel):
    """Update settings schema"""
    gemini_api_key: Optional[str] = None
    default_currency: Optional[str] = None
    theme: Optional[str] = Field(None, pattern="^(dark|light)$")
    budget_alerts: Optional[bool] = None
    monthly_budget: Optional[float] = Field(None, ge=0)


class SettingsResponse(BaseModel):
    """Settings response schema (without sensitive data)"""
    default_currency: str
    theme: str
    budget_alerts: bool
    monthly_budget: Optional[float]
    has_gemini_api_key: bool  # Don't expose the actual key


# Category Schemas
class CategoryCreate(BaseModel):
    """Create category schema"""
    name: str = Field(..., min_length=1, max_length=50)
    icon: str
    color: str = Field(..., pattern="^#[0-9A-Fa-f]{6}$")
    type: str = Field(..., pattern="^(expense|income)$")


class CategoryResponse(BaseModel):
    """Category response schema"""
    id: str
    name: str
    icon: str
    color: str
    type: str


# Analytics Schemas
class PeriodStats(BaseModel):
    """Statistics for a time period"""
    total_income: float
    total_expenses: float
    net: float
    transaction_count: int


class CategoryBreakdown(BaseModel):
    """Expense/income breakdown by category"""
    category_id: Optional[str]
    category_name: str
    amount: float
    percentage: float
    color: str


class AnalyticsResponse(BaseModel):
    """Analytics response with stats and charts"""
    period: str  # "daily", "monthly", "yearly"
    stats: PeriodStats
    expense_breakdown: List[CategoryBreakdown]
    income_breakdown: List[CategoryBreakdown]
