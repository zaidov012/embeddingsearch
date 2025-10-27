from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
from models import (
    UploadResponse,
    SearchResponse,
    SearchResult,
    HealthResponse,
    ErrorResponse
)
from services import embedding_service, document_processor, vector_db_service
from config import settings

router = APIRouter()


@router.post("/upload", response_model=UploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing and indexing.
    
    - **file**: PDF file to upload
    
    Returns information about the uploaded file and created chunks.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Process PDF: extract text and create chunks
        chunks = document_processor.process_pdf(content, file.filename)
        
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF"
            )
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings = embedding_service.embed_texts(chunk_texts)
        
        # Prepare metadata - include header information
        metadatas = []
        for chunk in chunks:
            metadata = {
                "filename": chunk['filename'],
                "chunk_index": chunk['chunk_index']
            }
            
            # Add header information if available
            if 'header' in chunk:
                metadata['header'] = chunk['header']
                metadata['header_level'] = chunk.get('header_level', 0)
                metadata['is_partial'] = chunk.get('is_partial', False)
            elif 'chunk_type' in chunk:
                metadata['chunk_type'] = chunk['chunk_type']
            
            metadatas.append(metadata)
        
        # Store in vector database
        doc_ids = vector_db_service.add_documents(
            texts=chunk_texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        return UploadResponse(
            message="File uploaded and processed successfully",
            filename=file.filename,
            chunks_created=len(chunks),
            document_ids=doc_ids
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/search", response_model=SearchResponse, responses={400: {"model": ErrorResponse}})
async def search_documents(
    query: str = Query(..., description="Search query", min_length=1),
    top_k: int = Query(10, description="Number of results to return", ge=1, le=100)
):
    """
    Search for documents based on a query.
    
    - **query**: Search query text
    - **top_k**: Number of top results to return (default: 10, max: 100)
    
    Returns matching document chunks with similarity scores.
    """
    try:
        # Generate embedding for the query
        query_embedding = embedding_service.embed_text(query)
        
        # Search in vector database
        results = vector_db_service.search(
            query_embedding=query_embedding,
            n_results=top_k
        )
        
        # Format results
        search_results = []
        
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                # Distance to similarity (ChromaDB returns L2 distance by default)
                # Convert distance to similarity score (0 to 1, higher is better)
                distance = results['distances'][0][i]
                similarity = 1 / (1 + distance)  # Simple conversion
                
                metadata = results['metadatas'][0][i]
                
                search_results.append(
                    SearchResult(
                        document_name=metadata['filename'],
                        chunk_text=results['documents'][0][i],
                        chunk_index=metadata['chunk_index'],
                        similarity=round(similarity, 4),
                        header=metadata.get('header'),
                        header_level=metadata.get('header_level'),
                        chunk_type=metadata.get('chunk_type')
                    )
                )
        
        return SearchResponse(
            query=query,
            results=search_results,
            total_results=len(search_results)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing search: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check the health status of the system.
    
    Returns information about the system configuration and indexed documents.
    """
    try:
        total_chunks = vector_db_service.count_documents()
        available_files = vector_db_service.get_all_filenames()
        
        return HealthResponse(
            status="healthy",
            model_type=settings.MODEL_TYPE,
            model_path=settings.MODEL_PATH,
            total_chunks=total_chunks,
            total_documents=len(available_files),
            available_files=available_files
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """
    Delete all chunks of a specific document.
    
    - **filename**: Name of the file to delete
    
    Returns the number of deleted chunks.
    """
    try:
        deleted_count = vector_db_service.delete_by_filename(filename)
        
        if deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{filename}' not found"
            )
        
        return {
            "message": f"Document '{filename}' deleted successfully",
            "chunks_deleted": deleted_count
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )


@router.get("/documents")
async def list_documents():
    """
    List all uploaded documents.
    
    Returns a list of all document filenames in the system.
    """
    try:
        filenames = vector_db_service.get_all_filenames()
        
        return {
            "total_documents": len(filenames),
            "documents": filenames
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )
