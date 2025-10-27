"""
Test script to verify the document search system.
Run this after installing dependencies to ensure everything is working.
"""

import requests
import time
import os


BASE_URL = "http://localhost:8000"


def test_health():
    """Test the health endpoint."""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/health")
    if response.status_code == 200:
        data = response.json()
        print("✓ Health check passed")
        print(f"  Model Type: {data['model_type']}")
        print(f"  Model Path: {data['model_path']}")
        print(f"  Total Chunks: {data['total_chunks']}")
        print(f"  Total Documents: {data['total_documents']}")
        print(f"  Available Files: {data['available_files']}")
        return True
    else:
        print("✗ Health check failed")
        print(f"  Status: {response.status_code}")
        return False


def test_upload(pdf_path):
    """Test uploading a PDF file."""
    print("\n" + "="*60)
    print("Testing Upload Endpoint")
    print("="*60)
    
    if not os.path.exists(pdf_path):
        print(f"✗ Test PDF not found at: {pdf_path}")
        print("  Please provide a valid PDF path to test upload")
        return False
    
    with open(pdf_path, 'rb') as f:
        files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Upload successful")
        print(f"  Filename: {data['filename']}")
        print(f"  Chunks Created: {data['chunks_created']}")
        print(f"  Message: {data['message']}")
        return True
    else:
        print("✗ Upload failed")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


def test_search(query, top_k=5):
    """Test the search endpoint."""
    print("\n" + "="*60)
    print("Testing Search Endpoint")
    print("="*60)
    
    params = {'query': query, 'top_k': top_k}
    response = requests.get(f"{BASE_URL}/api/search", params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Search successful")
        print(f"  Query: {data['query']}")
        print(f"  Total Results: {data['total_results']}")
        
        if data['results']:
            print("\n  Top Results:")
            for i, result in enumerate(data['results'][:3], 1):
                print(f"\n  {i}. Document: {result['document_name']}")
                print(f"     Similarity: {result['similarity']:.4f}")
                print(f"     Chunk Index: {result['chunk_index']}")
                print(f"     Text Preview: {result['chunk_text'][:100]}...")
        else:
            print("  No results found")
        
        return True
    else:
        print("✗ Search failed")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


def test_list_documents():
    """Test listing all documents."""
    print("\n" + "="*60)
    print("Testing List Documents Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/documents")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ List documents successful")
        print(f"  Total Documents: {data['total_documents']}")
        if data['documents']:
            print("  Documents:")
            for doc in data['documents']:
                print(f"    - {doc}")
        return True
    else:
        print("✗ List documents failed")
        print(f"  Status: {response.status_code}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Document Search API - System Test")
    print("="*60)
    print("\nMake sure the server is running: python main.py")
    print("Press Enter to continue...")
    input()
    
    # Test health
    if not test_health():
        print("\n✗ Health check failed. Make sure the server is running.")
        return
    
    # Wait a moment
    time.sleep(1)
    
    # Test list documents
    test_list_documents()
    
    # Test upload (you can provide a PDF path here)
    pdf_path = input("\n\nEnter path to a test PDF file (or press Enter to skip): ").strip()
    if pdf_path:
        if test_upload(pdf_path):
            time.sleep(2)  # Wait for indexing
            
            # Test search
            query = input("\nEnter a search query to test: ").strip()
            if query:
                test_search(query)
    
    # Final health check
    time.sleep(1)
    test_health()
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
