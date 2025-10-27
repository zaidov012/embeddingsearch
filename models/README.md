# Models Directory

This directory is for storing custom embedding models locally.

## 📝 Important

**Model files are not included in the Git repository** due to their large size (typically 100MB - 1GB+).

## Setup Options

### Option 1: Use HuggingFace Models (Recommended)

No setup needed! Models are automatically downloaded when you configure:

```env
MODEL_TYPE=huggingface
MODEL_PATH=sentence-transformers/all-MiniLM-L6-v2
```

### Option 2: Custom Models

If you have custom model files:

1. Create a subdirectory for your model:
   ```
   models/
   └── your-model-name/
       ├── config.json
       ├── model.safetensors
       ├── tokenizer.json
       ├── vocab.txt
       └── ... (other model files)
   ```

2. Configure in `.env`:
   ```env
   MODEL_TYPE=custom
   MODEL_PATH=models/your-model-name
   ```

## Current Project

This project was developed with a custom fine-tuned **Nomic Embed Text v1.5** model. To use similar capabilities with HuggingFace:

```env
MODEL_TYPE=huggingface
MODEL_PATH=nomic-ai/nomic-embed-text-v1.5
EMBEDDING_DIMENSION=768
```

## More Information

See [MODEL_SETUP.md](../MODEL_SETUP.md) for detailed instructions.
