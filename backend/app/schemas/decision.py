"""Decision schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DecisionCreate(BaseModel):
    """Schema for creating a decision."""
    
    title: str = Field(..., min_length=1, max_length=500)
    original_input: str = Field(..., min_length=1)
    locale: str = Field(default="en", pattern="^(en|id)$")
    alternatives: Optional[list[str]] = None


class DecisionResponse(BaseModel):
    """Schema for decision response."""
    
    id: UUID
    title: str
    original_input: str
    locale: str
    current_version_number: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class DecisionListResponse(BaseModel):
    """Schema for list of decisions."""
    
    decisions: list[DecisionResponse]
    total: int
