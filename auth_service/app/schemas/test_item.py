"""
Pydantic schemas for TestItem API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TestItemCreate(BaseModel):
    """Schema for creating a new test item"""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the test item")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    is_active: bool = Field(default=True, description="Whether the item is active")


class TestItemUpdate(BaseModel):
    """Schema for updating a test item"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None


class TestItemResponse(BaseModel):
    """Schema for test item responses"""
    id: int
    title: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Allows creating from ORM models
