from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# Base schemas
class WishlistBase(BaseModel):
    user_id: int
    product_variation_id: int
    product_name: Optional[str] = None
    product_price: Optional[int] = None
    product_image: Optional[str] = None

class WishlistCreate(WishlistBase):
    pass

class WishlistUpdate(BaseModel):
    product_name: Optional[str] = None
    product_price: Optional[int] = None
    product_image: Optional[str] = None

# Response schemas
class WishlistResponse(WishlistBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class WishlistListResponse(BaseModel):
    items: List[WishlistResponse]
    total: int
    page: int
    size: int