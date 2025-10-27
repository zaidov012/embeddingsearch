# Model Setup Guide

This project supports both custom fine-tuned models and pre-trained models from HuggingFace.

## ⚠️ Important Note About Model Files

The `models/` directory contains large model files (typically 100MB - 1GB+) that **should not be committed to GitHub** due to size constraints. Instead, users should download or reference models separately.

## Option 1: Using HuggingFace Models (Recommended for GitHub)

The easiest way to get started is to use pre-trained models from HuggingFace Hub. These are automatically downloaded when the application starts.

**Configure in `.env`:**
```env
MODEL_TYPE=huggingface
MODEL_PATH=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

Popular embedding models:
- `sentence-transformers/all-MiniLM-L6-v2` - Fast and efficient (384 dim)
- `sentence-transformers/all-mpnet-base-v2` - High quality (768 dim)
- `BAAI/bge-small-en-v1.5` - Good balance (384 dim)
- `BAAI/bge-base-en-v1.5` - Better quality (768 dim)

## Option 2: Using Custom Models

If you have a custom fine-tuned model:

### For Development (Local)

1. Place your model files in `models/your-model-name/`
2. Configure in `.env`:
```env
MODEL_TYPE=custom
MODEL_PATH=models/your-model-name
EMBEDDING_DIMENSION=768
```

### For Distribution (GitHub)

**Option A: Model on HuggingFace Hub**

1. Upload your model to HuggingFace Hub
2. Users can reference it directly:
```env
MODEL_TYPE=huggingface
MODEL_PATH=your-username/your-model-name
```

**Option B: External Storage**

1. Upload model to cloud storage (Google Drive, Dropbox, AWS S3, etc.)
2. Provide download link in README
3. Users download and place in `models/` directory

**Option C: Git LFS (for smaller models < 100MB)**

1. Install Git LFS: `git lfs install`
2. Track model files: `git lfs track "models/**/*.safetensors"`
3. Commit `.gitattributes` file

## Current Project Setup

This repository is configured to use the **Nomic Embed Text v1.5** model. Due to file size, the model files are not included in the repository.

### To use this project:

**Option 1: Use HuggingFace alternative**
```env
MODEL_TYPE=huggingface
MODEL_PATH=nomic-ai/nomic-embed-text-v1.5
EMBEDDING_DIMENSION=768
```

**Option 2: Download the custom model**

If you have access to the custom fine-tuned model:
1. Download the model files
2. Place them in `models/nomic-embed-text-v1.5/nomic-embed-text-v1.5-az/`
3. Ensure these files are present:
   - `config.json`
   - `model.safetensors`
   - `tokenizer.json`
   - `vocab.txt`
   - Other configuration files

## Verifying Model Setup

After configuration, test the model loading:

```bash
python main.py
```

You should see:
```
============================================================
Starting Document Search API
============================================================
Model Type: huggingface
Model Path: sentence-transformers/all-MiniLM-L6-v2
ChromaDB Directory: ./chroma_db
============================================================
```

If the model loads successfully, you're ready to go!

## Troubleshooting

**"Model files not found"**
- Check that MODEL_PATH in `.env` points to the correct location
- For HuggingFace models, ensure you have internet connection
- For local models, verify all required files are present

**"Out of memory"**
- Try a smaller model (e.g., all-MiniLM-L6-v2)
- Reduce batch size in processing
- Use CPU instead of GPU if GPU memory is limited

**"Model dimension mismatch"**
- Update EMBEDDING_DIMENSION in `.env` to match your model
- Check model documentation for the correct dimension

## Questions?

Open an issue on GitHub if you need help with model setup!
