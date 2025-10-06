from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class WishlistEventType(str, Enum):
    CREATED = "wishlist.created"
    UPDATED = "wishlist.updated"
    DELETED = "wishlist.deleted"

class WishlistEventData(BaseModel):
    wishlist_id: int
    user_id: int
    product_variation_id: int
    timestamp: datetime

class WishlistEvent(BaseModel):
    event_type: WishlistEventType
    data: WishlistEventData
    service: str = "wishlist-service"
    version: str = "1.0"