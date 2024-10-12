from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models import Item, UpdateItem, FilterItemsRequest, AggregationResult
from database import items_collection
from datetime import datetime
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def is_valid_object_id(oid: str) -> bool:
    """Check if the provided string is a valid ObjectId."""
    return isinstance(oid, str) and len(oid) == 24 and all(c in '0123456789abcdefABCDEF' for c in oid)

# POST: Create a new item
@router.post("/items")
def create_item(item: Item):
    item_data = item.dict()
    item_data["insert_date"] = datetime.utcnow()  # Use UTC for consistency
    result = items_collection.insert_one(item_data)
    return {"id": str(result.inserted_id)}

# MongoDB Aggregation: Group by email and count items
@router.get("/items/aggregation", response_model=List[AggregationResult])
def aggregate_items():
    try:
        logger.info("Executing aggregation pipeline to count items grouped by email.")
        
        # Aggregation pipeline to count items grouped by email
        pipeline = [
            {
                "$group": {
                    "_id": "$email",  # Group by email
                    "count": {"$sum": 1}  # Count the number of items
                }
            },
            {
                "$project": {
                    "email": "$_id",  # Rename _id to email
                    "count": 1,  # Keep the count field
                    "_id": 0  # Exclude the original _id field
                }
            }
        ]

        # Execute the aggregation pipeline
        result = list(items_collection.aggregate(pipeline))
        
        # Log the result of the aggregation
        logger.info("Aggregation result: %s", result)
        
        return result

    except Exception as e:
        logger.error("Error during aggregation: %s", str(e))
        raise HTTPException(status_code=500, detail="Error during aggregation: " + str(e))

# GET: Retrieve an item by ID
@router.get("/items/{id}")
def get_item(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
    item = items_collection.find_one({"_id": ObjectId(id)})
    if item:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items/filter", response_model=List[dict])
def filter_items(filter_request: FilterItemsRequest):
    query = {}

    logger.info("Filter Items called with: %s", filter_request.dict())

    if filter_request.email:
        query["email"] = filter_request.email

    if filter_request.expiry_date:
        try:
            expiry_date = datetime.fromisoformat(filter_request.expiry_date)
            query["expiry_date"] = {"$gte": expiry_date}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid expiry_date format. Use YYYY-MM-DD.")

    if filter_request.insert_date:
        try:
            insert_date = datetime.fromisoformat(filter_request.insert_date)
            query["insert_date"] = {"$gte": insert_date}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid insert_date format. Use YYYY-MM-DD.")

    if filter_request.quantity is not None:
        if isinstance(filter_request.quantity, int):
            query["quantity"] = {"$gte": filter_request.quantity}
        else:
            raise HTTPException(status_code=400, detail="Quantity must be an integer.")

    logger.info("Executing MongoDB query: %s", query)

    try:
        items = list(items_collection.find(query))
        for item in items:
            item["_id"] = str(item["_id"])  # Convert ObjectId to string
        return items
    except Exception as e:
        logger.error("Error fetching items: %s", str(e))
        raise HTTPException(status_code=500, detail="Error fetching items")

# DELETE: Delete an item by ID
@router.delete("/items/{id}")
def delete_item(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
    result = items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"msg": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# PUT: Update an item by ID
@router.put("/items/{id}")
def update_item(id: str, item: UpdateItem):
    if not is_valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
    update_data = {k: v for k, v in item.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = items_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 1:
        return {"msg": "Item updated"}
    raise HTTPException(status_code=404, detail="Item not found")
