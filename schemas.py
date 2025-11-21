"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Public site schemas for De Bessa Hair

class Contact(BaseModel):
    """
    Contact messages from the website
    Collection name: "contact"
    """
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=40)
    message: str = Field(..., min_length=5, max_length=2000)
    language: Optional[str] = Field("en", description="User language code")

class Review(BaseModel):
    """
    Customer reviews for the website
    Collection name: "review"
    """
    name: str = Field(..., min_length=2, max_length=120)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)
    source: Optional[str] = Field(None, description="e.g., Google, Instagram")
    locale: Optional[str] = Field("en")
    date: Optional[datetime] = None

# Example schemas retained for reference (not used by the site directly)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
