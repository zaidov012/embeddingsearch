from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from config import settings
import uuid


class VectorDBService:
    """Service for managing ChromaDB vector database."""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize ChromaDB with persistence."""
        try:
            # Create persistent client
            self.client = chromadb.Client(
                ChromaSettings(
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                    is_persistent=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=settings.COLLECTION_NAME,
                metadata={"description": "Document embeddings for search"}
            )
            
            print(f"ChromaDB initialized. Collection '{settings.COLLECTION_NAME}' ready.")
            print(f"Existing documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error initializing ChromaDB: {str(e)}")
            raise
    
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Add documents to the vector database.
        Returns list of document IDs.
        """
        # Generate unique IDs for each chunk
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
        return ids
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for similar documents.
        Returns documents with their metadata and distances.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
    
    def delete_by_filename(self, filename: str) -> int:
        """
        Delete all chunks associated with a filename.
        Returns number of deleted documents.
        """
        # Query all documents with the filename
        results = self.collection.get(
            where={"filename": filename}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            return len(results['ids'])
        
        return 0
    
    def get_all_filenames(self) -> List[str]:
        """Get list of all unique filenames in the database."""
        # Get all documents
        all_docs = self.collection.get()
        
        if not all_docs['metadatas']:
            return []
        
        # Extract unique filenames
        filenames = set()
        for metadata in all_docs['metadatas']:
            if 'filename' in metadata:
                filenames.add(metadata['filename'])
        
        return sorted(list(filenames))
    
    def count_documents(self) -> int:
        """Get total count of chunks in the database."""
        return self.collection.count()
    
    def clear_collection(self):
        """Delete all documents from the collection."""
        # Delete the collection and recreate it
        self.client.delete_collection(name=settings.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            metadata={"description": "Document embeddings for search"}
        )


# Singleton instance
vector_db_service = VectorDBService()
