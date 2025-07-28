"""Smart Lock System Cloud Backend API.

This FastAPI application provides a cloud backend for a smart lock system
with separated data models, business logic, and API endpoints.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.core.config import settings
from app.api import (
    auth_router,
    permissions_router,
    users_router,
    access_logs_router,
    gateways_router,
    reports_router
)
from app.services import GatewayCommService

# Global gateway service instance
gateway_service = GatewayCommService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    gateway_service.start()
    
    yield
    
    # Shutdown
    gateway_service.stop()


# Create FastAPI application
app = FastAPI(
    title="Smart Lock System API",
    version="1.0.0",
    description="Cloud backend API for smart lock system with permission management, gateway communication, and access logging.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router)
app.include_router(permissions_router)
app.include_router(users_router)
app.include_router(access_logs_router)
app.include_router(gateways_router)
app.include_router(reports_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Smart Lock System Cloud Backend API",
        "version": "0.1.0",
        "status": "running",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-07-28T12:00:00Z",
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Changed to 8001 to avoid conflicts
        reload=True
    )
