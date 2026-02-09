# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import YOUR actual application
# ⭐️ Choose ONE based on your structure ⭐️

# If you have app/__init__.py with app creation:
# from app import app

# If you have app/api.py or similar:
# from app.api import router as api_router

# If you have routes in separate files:
# from app.routes import items, users, predictions

# Create main app
app = FastAPI(
    title="Your AI API",
    description="Machine Learning and Data Processing API",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⭐️ ADD YOUR ACTUAL ROUTES HERE ⭐️
# Example:
# from .routes import ml_routes, data_routes, auth_routes
# app.include_router(ml_routes.router, prefix="/api/v1")
# app.include_router(data_routes.router, prefix="/api/v1")
# app.include_router(auth_routes.router, prefix="/auth")

@app.get("/")
async def root():
    return {
        "message": "AI API is running",
        "status": "active",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api": "/api/v1/..."
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-api"}
