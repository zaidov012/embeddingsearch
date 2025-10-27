# Document Search API

> A production-ready semantic search system for PDF documents using custom embedding models and vector similarity search.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5.20-orange.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Overview

A FastAPI-based document search system that enables semantic search across PDF documents using state-of-the-art embedding models. Upload PDFs, and search them using natural language queries with intelligent header-based chunking for better context preservation.

## ✨ Features

- **📄 PDF Upload & Processing**: Automatic text extraction and intelligent chunking
- **🔍 Semantic Search**: Natural language queries with embedding-based similarity
- **🧠 Smart Chunking**: Header-aware document segmentation preserving semantic context
- **🔧 Flexible Models**: Support for custom fine-tuned models and HuggingFace models
- **💾 Persistent Storage**: ChromaDB-backed vector store survives restarts
- **🚀 RESTful API**: Clean, documented REST API with interactive Swagger UI
- **⚡ GPU Acceleration**: Automatic GPU support for faster embeddings

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Smart Chunking](#-smart-chunking-strategy)
- [Architecture](#-architecture)
- [Usage Examples](#-usage-examples)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) GPU with CUDA for acceleration

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/zaidov012/EmbeddingSearch.git
cd EmbeddingSearch
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
```

Edit `.env` to configure your setup:
```env
# Model Configuration
MODEL_TYPE=custom              # Options: custom, huggingface
MODEL_PATH=models/nomic-embed-text-v1.5/nomic-embed-text-v1.5-az
EMBEDDING_DIMENSION=768

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=document_embeddings

# Document Processing
CHUNK_SIZE=500                 # Characters per chunk
CHUNK_OVERLAP=50               # Character overlap

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## 🚀 Quick Start

### Start the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Access Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test the API

```bash
# Check system health
curl http://localhost:8000/api/health

# Upload a PDF
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf"

# Search documents
curl "http://localhost:8000/api/search?query=machine%20learning&top_k=5"
```

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```
Returns system status, model information, and document statistics.

**Response:**
```json
{
  "status": "healthy",
  "model_type": "custom",
  "model_path": "models/nomic-embed-text-v1.5/nomic-embed-text-v1.5-az",
  "total_documents": 5,
  "total_chunks": 127
}
```

### Upload PDF
```http
POST /api/upload
```
Upload a PDF file for processing and indexing.

**Request:** Multipart form data with PDF file

**Response:**
```json
{
  "message": "File uploaded and processed successfully",
  "filename": "document.pdf",
  "chunks_created": 42,
  "document_ids": ["uuid1", "uuid2", ...]
}
```

### Search Documents
```http
GET /api/search?query={query}&top_k={top_k}
```
Search for relevant document chunks using natural language.

**Parameters:**
- `query` (required): Search query text
- `top_k` (optional): Number of results (default: 10, max: 100)

**Response:**
```json
{
  "query": "your search query",
  "total_results": 10,
  "results": [
    {
      "document_name": "document.pdf",
      "chunk_text": "Relevant text chunk...",
      "chunk_index": 5,
      "similarity": 0.8542,
      "header": "2.1 Introduction",
      "header_level": 2
    }
  ]
}
```

### List Documents
```http
GET /api/documents
```
List all uploaded documents.

**Response:**
```json
{
  "total_documents": 3,
  "documents": ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
}
```

### Delete Document
```http
DELETE /api/documents/{filename}
```
Delete all chunks of a specific document.

**Response:**
```json
{
  "message": "Document 'doc.pdf' deleted successfully",
  "chunks_deleted": 42
}
```

## ⚙️ Configuration

### Model Selection

> **📝 Note**: See [MODEL_SETUP.md](MODEL_SETUP.md) for detailed instructions on model setup, especially if you're cloning from GitHub.

#### Using HuggingFace Model (Recommended for Quick Start)
```env
MODEL_TYPE=huggingface
MODEL_PATH=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

The model will be automatically downloaded on first run. Popular options:
- `sentence-transformers/all-MiniLM-L6-v2` - Fast and efficient (384 dim)
- `sentence-transformers/all-mpnet-base-v2` - High quality (768 dim)
- `nomic-ai/nomic-embed-text-v1.5` - Latest Nomic model (768 dim)

#### Using Custom Model
If you have a custom fine-tuned model, place it in the `models/` directory and configure:
```env
MODEL_TYPE=custom
MODEL_PATH=models/your-model-name
EMBEDDING_DIMENSION=768
```

**⚠️ Important**: Large model files (>100MB) should not be committed to Git. See [MODEL_SETUP.md](MODEL_SETUP.md) for distribution strategies.

### Chunking Parameters

Adjust document processing behavior:
```env
CHUNK_SIZE=500        # Target chunk size in characters
CHUNK_OVERLAP=50      # Overlap between chunks
```

## 🧩 Smart Chunking Strategy

The system uses **intelligent header-based chunking** to preserve semantic context:

### How It Works

1. **Header Detection**: Automatically identifies section headers
   - Numbered sections: `1. Introduction`, `1.1 Background`
   - Roman numerals: `I. Overview`, `II. Methodology`
   - ALL CAPS: `INTRODUCTION`, `METHODOLOGY`
   - Keyword headers: `Chapter 1`, `Section 2.1`

2. **Semantic Splitting**: Chunks documents at natural boundaries
   - Preserves complete sections
   - Splits large sections by paragraphs
   - Falls back to paragraph-based chunking if no headers detected

3. **Metadata Enrichment**: Each chunk includes:
   - Section header and hierarchy level
   - Position in document
   - Document name and chunk index

### Benefits

- ✅ Better semantic coherence
- ✅ Improved search relevance
- ✅ Context-aware results
- ✅ Natural topic boundaries

### Example

**Input Document:**
```
1. Introduction
This document describes...

2. Methodology
We conducted research...

2.1 Data Collection
The data was collected...
```

**Generated Chunks:**
- Chunk 0: "1. Introduction\nThis document describes..." (header: "1. Introduction", level: 1)
- Chunk 1: "2. Methodology\nWe conducted research..." (header: "2. Methodology", level: 1)
- Chunk 2: "2.1 Data Collection\nThe data was..." (header: "2.1 Data Collection", level: 2)

## 🏗️ Architecture

### Project Structure

```
EmbeddingSearch/
├── api/
│   ├── __init__.py
│   └── routes.py              # API endpoints
├── services/
│   ├── __init__.py
│   ├── embedding_service.py   # Embedding model management
│   ├── document_processor.py  # PDF processing & smart chunking
│   └── vector_db_service.py   # ChromaDB operations
├── models/
│   └── nomic-embed-text-v1.5/ # Custom embedding model
├── chroma_db/                  # Persisted vector database
├── config.py                   # Configuration management
├── models.py                   # Pydantic data models
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment configuration
├── .gitignore                  # Git ignore rules
├── test_api.py                 # API testing script
├── example_client.py           # Python client example
└── README.md                   # This file
```

### Data Flow

**Upload Pipeline:**
```
PDF Upload → Text Extraction → Smart Chunking → Embedding Generation → Vector Storage
```

**Search Pipeline:**
```
Query → Embedding Generation → Vector Similarity Search → Ranking → Results
```

### Key Components

- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **ChromaDB**: Efficient vector database with persistence
- **Sentence-Transformers**: State-of-the-art embedding generation
- **PyPDF**: Reliable PDF text extraction

## 💻 Usage Examples

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload a PDF
def upload_pdf(filepath):
    with open(filepath, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/upload",
            files={'file': f}
        )
    return response.json()

# Search documents
def search(query, top_k=5):
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={'query': query, 'top_k': top_k}
    )
    return response.json()

# List all documents
def list_documents():
    response = requests.get(f"{BASE_URL}/api/documents")
    return response.json()

# Delete a document
def delete_document(filename):
    response = requests.delete(f"{BASE_URL}/api/documents/{filename}")
    return response.json()

# Example usage
result = upload_pdf('research_paper.pdf')
print(f"Uploaded: {result['chunks_created']} chunks created")

results = search("machine learning algorithms", top_k=3)
for i, hit in enumerate(results['results'], 1):
    print(f"{i}. [{hit['document_name']}] {hit['header']} (similarity: {hit['similarity']:.3f})")
    print(f"   {hit['chunk_text'][:100]}...")
```

### PowerShell

```powershell
# Upload PDF
$form = @{
    file = Get-Item -Path "document.pdf"
}
Invoke-RestMethod -Uri "http://localhost:8000/api/upload" -Method Post -Form $form

# Search
$query = "machine learning"
Invoke-RestMethod -Uri "http://localhost:8000/api/search?query=$query&top_k=5" -Method Get

# List documents
Invoke-RestMethod -Uri "http://localhost:8000/api/documents" -Method Get

# Delete document
Invoke-RestMethod -Uri "http://localhost:8000/api/documents/document.pdf" -Method Delete
```

### JavaScript/TypeScript

```javascript
// Upload PDF
async function uploadPDF(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/upload', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// Search
async function search(query, topK = 5) {
  const params = new URLSearchParams({ query, top_k: topK });
  const response = await fetch(`http://localhost:8000/api/search?${params}`);
  return await response.json();
}

// Usage
const results = await search('machine learning', 5);
results.results.forEach((hit, i) => {
  console.log(`${i + 1}. [${hit.document_name}] ${hit.header}`);
  console.log(`   Similarity: ${hit.similarity.toFixed(3)}`);
});
```

## 🐳 Deployment

### Using Docker (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t document-search .
docker run -p 8000:8000 -v ./chroma_db:/app/chroma_db document-search
```

### Production Considerations

1. **Security**:
   - Add API key authentication
   - Configure CORS properly
   - Implement rate limiting
   - Use HTTPS
   - Add file size limits

2. **Performance**:
   - Use Gunicorn with multiple workers
   - Enable caching for frequently accessed embeddings
   - Consider Redis for session management

3. **Monitoring**:
   - Add logging (structured logs)
   - Implement health checks
   - Monitor API metrics
   - Track embedding generation times

4. **Scaling**:
   - Deploy behind a load balancer
   - Use external PostgreSQL with pgvector
   - Separate compute for embedding generation
   - Implement async background processing

## 🧪 Testing

Run the included test script:
```bash
python test_api.py
```

Run the example client:
```bash
python example_client.py
```

## 📊 Performance

- **Upload Speed**: Processes PDFs in seconds
- **Search Latency**: Sub-second response for large collections
- **Storage**: ~3KB per chunk (768-dim embeddings)
- **GPU Acceleration**: Automatic when available
- **Scalability**: Handles 1M+ document chunks efficiently

## 🔒 Security Notes

This implementation is designed for development and testing. For production:

- ⚠️ Add authentication (OAuth2, JWT, API keys)
- ⚠️ Configure CORS for specific origins only
- ⚠️ Implement rate limiting
- ⚠️ Add input validation and sanitization
- ⚠️ Use HTTPS in production
- ⚠️ Implement file size and type validation
- ⚠️ Add virus scanning for uploaded files

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

**Quick Start for Contributors:**

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [Sentence-Transformers](https://www.sbert.net/) for embedding models
- [Nomic AI](https://www.nomic.ai/) for the nomic-embed-text model

## 📧 Contact

For questions, issues, or suggestions, please [open an issue](https://github.com/zaidov012/EmbeddingSearch/issues) on GitHub.

---

**Built with ❤️ using FastAPI, ChromaDB, and state-of-the-art embedding models**
