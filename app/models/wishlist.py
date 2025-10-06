from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Wishlist(Base):
    __tablename__ = "wishlists"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    product_variation_id = Column(BigInteger, nullable=False, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional fields for better data consistency
    product_name = Column(String(255))  # Cache product name
    product_price = Column(BigInteger)  # Cache product price
    product_image = Column(String(500)) # Cache product image URL
    
    def __repr__(self):
        return f"<Wishlist(user_id={self.user_id}, product_variation_id={self.product_variation_id})>"