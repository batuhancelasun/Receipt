"""
MongoDB document models for Receipt Tracker
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    """User model for authentication"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    hashed_password: str
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CategoryModel(BaseModel):
    """Expense/Income category"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    icon: str  # Emoji or icon name
    color: str  # Hex color
    type: str  # "expense" or "income"
    user_id: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TransactionItemModel(BaseModel):
    """Individual item in a transaction"""
    name: str
    quantity: float = 1.0
    unit_price: float
    total_price: float


class TransactionModel(BaseModel):
    """Transaction (expense or income) model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    type: str  # "expense" or "income"
    amount: float
    currency: str = "€"
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    merchant_name: Optional[str] = None
    description: Optional[str] = None
    date: datetime
    items: Optional[List[TransactionItemModel]] = []
    receipt_id: Optional[str] = None  # Link to receipt if scanned
    tags: List[str] = []
    is_recurring: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class ReceiptModel(BaseModel):
    """Receipt scan model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    filename: str
    file_path: str
    scan_status: str  # "pending", "processing", "completed", "failed"
    ai_confidence: Optional[float] = None
    extracted_data: Optional[dict] = None  # Raw AI extraction
    transaction_id: Optional[str] = None  # Created transaction
    error_message: Optional[str] = None
    scanned_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class SettingsModel(BaseModel):
    """Application settings per user"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    gemini_api_key: Optional[str] = None
    default_currency: str = "€"
    theme: str = "dark"  # "dark" or "light"
    budget_alerts: bool = True
    monthly_budget: Optional[float] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
