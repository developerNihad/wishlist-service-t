from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate, WishlistUpdate

class CRUDWishlist:
    def __init__(self):
        pass
    
    async def get_by_id(self, db: AsyncSession, wishlist_id: int) -> Optional[Wishlist]:
        result = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id))
        return result.scalar_one_or_none()
    
    async def get_by_user_and_product(
        self, 
        db: AsyncSession, 
        user_id: int, 
        product_variation_id: int
    ) -> Optional[Wishlist]:
        result = await db.execute(
            select(Wishlist).where(
                Wishlist.user_id == user_id,
                Wishlist.product_variation_id == product_variation_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_user(
        self, 
        db: AsyncSession, 
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Wishlist]:
        result = await db.execute(
            select(Wishlist)
            .where(Wishlist.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Wishlist.created_at.desc())
        )
        return result.scalars().all()
    
    async def create(
        self, 
        db: AsyncSession, 
        wishlist_in: WishlistCreate
    ) -> Wishlist:
        # Check if already exists
        existing = await self.get_by_user_and_product(
            db, 
            wishlist_in.user_id, 
            wishlist_in.product_variation_id
        )
        
        if existing:
            return existing
            
        db_wishlist = Wishlist(**wishlist_in.model_dump())
        db.add(db_wishlist)
        await db.commit()
        await db.refresh(db_wishlist)
        return db_wishlist
    
    async def update(
        self,
        db: AsyncSession,
        db_wishlist: Wishlist,
        wishlist_in: WishlistUpdate
    ) -> Wishlist:
        update_data = wishlist_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_wishlist, field, value)
            
        await db.commit()
        await db.refresh(db_wishlist)
        return db_wishlist
    
    async def delete(self, db: AsyncSession, wishlist_id: int) -> bool:
        result = await db.execute(
            delete(Wishlist).where(Wishlist.id == wishlist_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    async def delete_by_user_and_product(
        self,
        db: AsyncSession,
        user_id: int,
        product_variation_id: int
    ) -> bool:
        result = await db.execute(
            delete(Wishlist).where(
                Wishlist.user_id == user_id,
                Wishlist.product_variation_id == product_variation_id
            )
        )
        await db.commit()
        return result.rowcount > 0

crud_wishlist = CRUDWishlist()