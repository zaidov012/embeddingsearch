from pydantic import BaseModel
from typing import List, Optional


class UploadResponse(BaseModel):
    """Response model for file upload."""
    message: str
    filename: str
    chunks_created: int
    document_ids: List[str]


class SearchResult(BaseModel):
    """Individual search result."""
    document_name: str
    chunk_text: str
    chunk_index: int
    similarity: float
    header: Optional[str] = None  # Section header if available
    header_level: Optional[int] = None  # Header level (1-3)
    chunk_type: Optional[str] = None  # Type if no header (e.g., 'paragraph_group')


class SearchResponse(BaseModel):
    """Response model for search."""
    query: str
    results: List[SearchResult]
    total_results: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    model_type: str
    model_path: str
    total_chunks: int
    total_documents: int
    available_files: List[str]


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str
    detail: Optional[str] = None
