from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Items API model
class Item(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="john.doe@example.com")
    item_name: str = Field(..., example="Widget A")
    quantity: int = Field(..., ge=0, example=10)  # Quantity should be non-negative
    expiry_date: str = Field(..., example="2024-12-31")  # YYYY-MM-DD format
    insert_date: datetime = Field(default_factory=datetime.utcnow)  # Automatically set insert date

class UpdateItem(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john.doe@example.com")
    item_name: Optional[str] = Field(None, example="Widget A")
    quantity: Optional[int] = Field(None, ge=0, example=10)  # Optional but should be non-negative
    expiry_date: Optional[str] = Field(None, example="2024-12-31")  # YYYY-MM-DD format


class FilterItemsRequest(BaseModel):
    email: Optional[str] = None
    expiry_date: Optional[str] = None  # Use string for ISO format date
    insert_date: Optional[str] = None   # Use string for ISO format date
    quantity: Optional[int] = None


class AggregationResult(BaseModel):
    email: str
    count: int

# Clock-In API model
class ClockInRecord(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    location: str = Field(..., example="Warehouse A")
    insert_datetime: datetime = Field(default_factory=datetime.utcnow)  # Automatically set clock-in date

class UpdateClockIn(BaseModel):
    email: Optional[str] = Field(None, example="john.doe@example.com")
    location: Optional[str] = Field(None, example="Warehouse A")
