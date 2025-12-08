import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .database.connection import init_db
from .api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
        "https://ai-enterprise-rag.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    init_db()
    # Verify Google API key is loaded
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print(f"✓ Google API Key loaded (starts with: {api_key[:20]}...)")
    else:
        print("⚠ Warning: GOOGLE_API_KEY not found in environment")


@app.get("/")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    api_key = os.environ.get("GOOGLE_API_KEY")
    return {
        "status": "healthy",
        "google_api_configured": bool(api_key)
    }
