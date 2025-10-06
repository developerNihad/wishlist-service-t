from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import wishlist
from app.events.publisher import event_publisher
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await event_publisher.connect()
    
    # Create database tables (development only)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    await event_publisher.close()
    await engine.dispose()

app = FastAPI(
    title="Wishlist Service",
    description="E-commerce Platform Wishlist Microservice",
    version="1.0.0",
    lifespan=lifespan
)

# API routes
app.include_router(
    wishlist.router,
    prefix="/api/v1/wishlist",
    tags=["wishlist"]
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "wishlist"}

@app.get("/")
async def root():
    return {"message": "Wishlist Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)