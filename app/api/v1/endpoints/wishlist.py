from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.schemas.wishlist import (
    WishlistCreate, 
    WishlistResponse, 
    WishlistListResponse,
    WishlistUpdate
)
from app.crud.wishlist import crud_wishlist
from app.events.publisher import event_publisher
from app.events.event_models import WishlistEvent, WishlistEventType, WishlistEventData
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
async def create_wishlist_item(
    wishlist_item: WishlistCreate,
    db: AsyncSession = Depends(get_db)
):
    """Yeni bir wishlist öğesi ekle"""
    db_item = await crud_wishlist.create(db, wishlist_item)
    
    # Event yayınla
    event_data = WishlistEventData(
        wishlist_id=db_item.id,
        user_id=db_item.user_id,
        product_variation_id=db_item.product_variation_id,
        timestamp=datetime.utcnow()
    )
    
    event = WishlistEvent(
        event_type=WishlistEventType.CREATED,
        data=event_data
    )
    
    await event_publisher.publish_wishlist_event(event)
    
    return db_item

@router.get("/user/{user_id}", response_model=WishlistListResponse)
async def get_user_wishlist(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Kullanıcının wishlist'ini getir"""
    items = await crud_wishlist.get_by_user(db, user_id, skip, limit)
    total = len(items)  # Gerçek projede count query'si eklenmeli
    
    return WishlistListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist_item(
    wishlist_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Wishlist öğesini sil"""
    db_item = await crud_wishlist.get_by_id(db, wishlist_id)
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )
    
    success = await crud_wishlist.delete(db, wishlist_id)
    
    if success:
        # Event yayınla
        event_data = WishlistEventData(
            wishlist_id=wishlist_id,
            user_id=db_item.user_id,
            product_variation_id=db_item.product_variation_id,
            timestamp=datetime.utcnow()
        )
        
        event = WishlistEvent(
            event_type=WishlistEventType.DELETED,
            data=event_data
        )
        
        await event_publisher.publish_wishlist_event(event)
    
    return None

@router.delete("/user/{user_id}/product/{product_variation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist_item_by_user_product(
    user_id: int,
    product_variation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Kullanıcı ve ürün varyasyonuna göre wishlist öğesini sil"""
    success = await crud_wishlist.delete_by_user_and_product(
        db, user_id, product_variation_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )
    
    # Event yayınlama burada da yapılabilir
    return None