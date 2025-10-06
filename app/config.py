from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/wishlist_db"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    
    # Service URLs
    USER_SERVICE_URL: str = "http://user-service:8000"
    PRODUCT_SERVICE_URL: str = "http://product-service:8000"
    
    class Config:
        env_file = ".env"

settings = Settings()