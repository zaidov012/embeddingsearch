from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Model Configuration
    MODEL_TYPE: Literal["custom", "huggingface"] = "custom"
    MODEL_PATH: str = "models/nomic-embed-text-v1.5/nomic-embed-text-v1.5-az"
    EMBEDDING_DIMENSION: int = 768
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    COLLECTION_NAME: str = "document_embeddings"
    
    # Document Processing Configuration
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
