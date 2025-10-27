import os
from typing import List
from sentence_transformers import SentenceTransformer
import torch
from config import settings


class EmbeddingService:
    """Service for generating embeddings using configurable models."""
    
    def __init__(self):
        self.model = None
        self.model_path = settings.MODEL_PATH
        self.model_type = settings.MODEL_TYPE
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model based on configuration."""
        try:
            if self.model_type == "custom":
                # Load custom fine-tuned model
                if not os.path.exists(self.model_path):
                    raise FileNotFoundError(f"Custom model not found at: {self.model_path}")
                
                print(f"Loading custom model from: {self.model_path}")
                self.model = SentenceTransformer(self.model_path)
                
            elif self.model_type == "huggingface":
                # Load model from HuggingFace
                print(f"Loading HuggingFace model: {self.model_path}")
                self.model = SentenceTransformer(self.model_path, trust_remote_code=True)
            
            else:
                raise ValueError(f"Unsupported model type: {self.model_type}")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = self.model.to(device)
            print(f"Model loaded successfully on device: {device}")
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        return self.model.get_sentence_embedding_dimension()


# Singleton instance
embedding_service = EmbeddingService()
