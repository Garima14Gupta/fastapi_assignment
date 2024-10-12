from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models import ClockInRecord, UpdateClockIn
from database import clock_in_collection
from datetime import datetime
from typing import Optional, List

router = APIRouter()

def is_valid_object_id(oid: str) -> bool:
    """Check if the provided string is a valid ObjectId."""
    return isinstance(oid, str) and len(oid) == 24 and all(c in '0123456789abcdefABCDEF' for c in oid)

def serialize_clock_in(clock_in: dict) -> dict:
    """Convert ObjectId and other necessary fields for JSON serialization."""
    clock_in['_id'] = str(clock_in['_id'])  # Convert ObjectId to string
    return clock_in

# POST: Create a new clock-in record
@router.post("/clock-in")
def create_clock_in(clock_in: ClockInRecord):
    clock_in_data = clock_in.dict()
    clock_in_data["insert_date"] = datetime.now().isoformat()  # Add insert date-time
    result = clock_in_collection.insert_one(clock_in_data)
    return {"id": str(result.inserted_id)}

# GET: Filter clock-in records
@router.get("/clock-in/filter", response_model=List[ClockInRecord])
def filter_clock_in(email: Optional[str] = None, location: Optional[str] = None, insert_date: Optional[str] = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_date:
        query["insert_date"] = {"$gte": insert_date}

    clock_ins = list(clock_in_collection.find(query))
    return [serialize_clock_in(clock_in) for clock_in in clock_ins]  # Serialize each clock-in

# GET: Retrieve clock-in record by ID
@router.get("/clock-in/{id}", response_model=ClockInRecord)
def get_clock_in(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
    clock_in = clock_in_collection.find_one({"_id": ObjectId(id)})
    if clock_in:
        return serialize_clock_in(clock_in)  # Serialize the clock-in
    raise HTTPException(status_code=404, detail="Clock-in record not found")

# DELETE: Delete a clock-in record by ID
@router.delete("/clock-in/{id}")
def delete_clock_in(id: str):
    result = clock_in_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"msg": "Clock-in record deleted"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")

# PUT: Update a clock-in record by ID
@router.put("/clock-in/{id}")
def update_clock_in(id: str, clock_in: UpdateClockIn):
    update_data = {k: v for k, v in clock_in.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = clock_in_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 1:
        return {"msg": "Clock-in record updated"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")
