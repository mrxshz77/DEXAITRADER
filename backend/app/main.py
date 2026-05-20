"""
DEXAITRADER Backend - Main FastAPI Application

This is the core backend server that handles:
- Order execution and management
- Position tracking
- Real-time price feeds via WebSocket
- Integration with DEX protocols
- Backtesting engine
- Communication with AI Agent
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routes (we'll create these next)
# from app.routes import orders, positions, backtest, websocket

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting DEXAITRADER Backend...")
    # TODO: Initialize database connections
    # TODO: Initialize Redis connection
    # TODO: Initialize price feeds
    yield
    # Shutdown
    logger.info("Shutting down DEXAITRADER Backend...")
    # TODO: Close connections


# Create FastAPI application
app = FastAPI(
    title="DEXAITRADER Backend",
    description="Advanced DEX Trading Platform with AI Agent",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# Health Check Endpoint
# ================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers"""
    return {
        "status": "healthy",
        "service": "DEXAITRADER Backend",
        "version": "1.0.0"
    }


# ================================
# Root Endpoint
# ================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "DEXAITRADER Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "components": {
            "orders": "/api/orders",
            "positions": "/api/positions",
            "backtest": "/api/backtest",
            "price_feed": "/api/price-feed",
            "websocket": "/ws"
        }
    }


# ================================
# Include Routes
# ================================

# TODO: Include route modules
# app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
# app.include_router(positions.router, prefix="/api/positions", tags=["Positions"])
# app.include_router(backtest.router, prefix="/api/backtest", tags=["Backtest"])


# ================================
# Error Handlers
# ================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return {
        "error": "Internal server error",
        "detail": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=os.getenv("BACKEND_DEBUG", "false").lower() == "true"
    )
