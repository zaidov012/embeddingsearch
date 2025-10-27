from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from config import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Document Search API",
    description="API for uploading PDFs, processing them with embeddings, and semantic search",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["Document Search"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Document Search API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("=" * 60)
    print("Starting Document Search API")
    print("=" * 60)
    print(f"Model Type: {settings.MODEL_TYPE}")
    print(f"Model Path: {settings.MODEL_PATH}")
    print(f"ChromaDB Directory: {settings.CHROMA_PERSIST_DIRECTORY}")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("Shutting down Document Search API")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False  # Disabled reload for Python 3.13 compatibility
    )
