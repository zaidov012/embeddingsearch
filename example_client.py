"""
Example client for the Document Search API.
Demonstrates how to integrate the search system into your application.
"""

import requests
from typing import List, Dict, Optional
import os


class DocumentSearchClient:
    """Client for interacting with the Document Search API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api"
    
    def health_check(self) -> Dict:
        """
        Check the health status of the API.
        
        Returns:
            Dict with system information
        """
        response = requests.get(f"{self.api_base}/health")
        response.raise_for_status()
        return response.json()
    
    def upload_pdf(self, file_path: str) -> Dict:
        """
        Upload a PDF file for processing.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dict with upload results
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise ValueError("Only PDF files are supported")
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
            response = requests.post(f"{self.api_base}/upload", files=files)
        
        response.raise_for_status()
        return response.json()
    
    def search(self, query: str, top_k: int = 10) -> Dict:
        """
        Search for documents matching the query.
        
        Args:
            query: Search query text
            top_k: Number of results to return (max 100)
            
        Returns:
            Dict with search results
        """
        params = {'query': query, 'top_k': min(top_k, 100)}
        response = requests.get(f"{self.api_base}/search", params=params)
        response.raise_for_status()
        return response.json()
    
    def list_documents(self) -> Dict:
        """
        List all uploaded documents.
        
        Returns:
            Dict with document list
        """
        response = requests.get(f"{self.api_base}/documents")
        response.raise_for_status()
        return response.json()
    
    def delete_document(self, filename: str) -> Dict:
        """
        Delete a document and all its chunks.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Dict with deletion result
        """
        response = requests.delete(f"{self.api_base}/documents/{filename}")
        response.raise_for_status()
        return response.json()


def example_usage():
    """Example usage of the Document Search Client."""
    
    # Initialize client
    client = DocumentSearchClient("http://localhost:8000")
    
    print("="*60)
    print("Document Search Client - Example Usage")
    print("="*60)
    
    # 1. Check health
    print("\n1. Checking system health...")
    try:
        health = client.health_check()
        print(f"✓ System is healthy")
        print(f"  Model: {health['model_type']} - {health['model_path']}")
        print(f"  Documents: {health['total_documents']}")
        print(f"  Total chunks: {health['total_chunks']}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # 2. List existing documents
    print("\n2. Listing existing documents...")
    try:
        docs = client.list_documents()
        if docs['documents']:
            print(f"✓ Found {docs['total_documents']} documents:")
            for doc in docs['documents']:
                print(f"  - {doc}")
        else:
            print("  No documents found")
    except Exception as e:
        print(f"✗ Failed to list documents: {e}")
    
    # 3. Upload a PDF (if path provided)
    print("\n3. Upload PDF...")
    pdf_path = input("Enter path to PDF file (or press Enter to skip): ").strip()
    
    if pdf_path:
        try:
            result = client.upload_pdf(pdf_path)
            print(f"✓ Uploaded successfully!")
            print(f"  File: {result['filename']}")
            print(f"  Chunks created: {result['chunks_created']}")
        except Exception as e:
            print(f"✗ Upload failed: {e}")
    
    # 4. Search
    print("\n4. Search documents...")
    query = input("Enter search query (or press Enter to skip): ").strip()
    
    if query:
        try:
            results = client.search(query, top_k=5)
            print(f"\n✓ Search completed!")
            print(f"  Query: '{results['query']}'")
            print(f"  Results found: {results['total_results']}")
            
            if results['results']:
                print("\n  Top matches:")
                for i, result in enumerate(results['results'], 1):
                    print(f"\n  {i}. {result['document_name']}")
                    print(f"     Similarity: {result['similarity']:.4f}")
                    print(f"     Chunk #{result['chunk_index']}")
                    print(f"     Text: {result['chunk_text'][:150]}...")
            else:
                print("  No results found")
        except Exception as e:
            print(f"✗ Search failed: {e}")
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    example_usage()
