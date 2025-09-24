<div align="center">

# 🕊️ Jotica - Biblical LoRA Training Platform

*Advanced AI training system for biblical texts using LoRA fine-tuning*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![GPU](https://img.shields.io/badge/CUDA-12.1+-green.svg?logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)

[🚀 Quick Start](#-quick-start-on-simplepod) • [📖 Documentation](#-project-structure) • [⚡ Features](#-key-features) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 Overview

**Jotica** is a comprehensive system for training **LoRA (Low-Rank Adaptation)** models on biblical texts, specifically designed for the **Reina-Valera 1909** Spanish Bible. Built for **SimplePod Docker environments** with **GPU acceleration**, it enables efficient fine-tuning of large language models for theological and biblical applications.

### 🌟 Key Features

- 🔥 **LoRA Fine-tuning** - Parameter-efficient training with PEFT
- 🐳 **SimplePod Ready** - Optimized for Docker + GPU environments  
- 📚 **Biblical Focus** - Specialized for Reina-Valera 1909 texts
- 🎯 **Alpaca Format** - Industry-standard instruction formatting
- ☁️ **Supabase Integration** - Vector storage and model checkpoints
- ⚡ **OpenAI Embeddings** - High-quality semantic representations
- 📊 **Automated Pipeline** - From ingestion to deployment

## 🏗️ Project Structure

```
jotica/
├── 🔧 config/
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Environment template
│   └── Dockerfile           # SimplePod container
├── 🚀 scripts/
│   ├── bootstrap_simplepod.sh   # One-time setup
│   ├── ingest_bible.sh         # Data processing
│   └── train_lora.sh           # Training pipeline
├── 📂 data/
│   ├── bible_rva1909/          # Raw biblical texts
│   └── refs/                   # Reference materials
├── 🎓 datasets/
│   └── bible_qa.jsonl          # Curated Q&A training data
└── 💻 src/
    ├── config.py               # Configuration management
    ├── utils/                  # Core utilities
    │   ├── supa.py            # Supabase client
    │   ├── emb.py             # Embedding generation
    │   └── io_utils.py        # File I/O helpers
    ├── ingest/                 # Data processing
    │   ├── parse_bible.py     # Bible text parser
    │   ├── parse_refs.py      # Reference processing
    │   └── upsert_supabase.py # Vector database
    ├── train/                  # Training modules
    │   ├── formatters.py      # Alpaca formatting
    │   ├── lora_runner.py     # LoRA training engine
    │   └── eval_smoke.py      # Model evaluation
    └── inference/              # Model serving
        └── generate.py        # Text generation
```

## 🚀 Quick Start on SimplePod

### Prerequisites
- 🐳 **SimplePod** environment with GPU support
- 🔑 **API Keys**: OpenAI, Supabase
- 💾 **Storage**: ~10GB for models and data

### 1️⃣ Clone & Setup
```bash
# Clone the repository
git clone https://github.com/SwStudioAI/jotica.git
cd jotica

# Configure environment
cp .env.example .env
# ✏️ Edit .env with your API keys
```

### 2️⃣ Bootstrap Environment
```bash
# One-time setup in SimplePod
bash scripts/bootstrap_simplepod.sh
```

### 3️⃣ Data Preparation
```bash
# Add your biblical texts to data/bible_rva1909/
# Add reference materials to data/refs/

# Process and create embeddings
bash scripts/ingest_bible.sh
```

### 4️⃣ Train LoRA Model
```bash
# Start training pipeline
bash scripts/train_lora.sh
```

### 5️⃣ Test Your Model
```bash
# Interactive testing
python -m src.inference.generate "Explica Juan 1:1 con citas bíblicas"
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# 🔑 API Keys
OPENAI_API_KEY=your_openai_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE=your_service_key

# ☁️ Storage
SUPABASE_BUCKET=jotica-models        # Model checkpoints
SUPABASE_DATA_BUCKET=jotica-data     # Optional corpus storage

# 🤖 Model Configuration  
BASE_MODEL=meta-llama/Llama-3-8B-Instruct
RUN_NAME=jotica-bible-lora-001
OUTPUT_DIR=/workspace/jotica/checkpoints

# 🎯 Training Parameters
EPOCHS=2
BATCH_SIZE=2
LR=2e-4
SAVE_STEPS=200
SAVE_TOTAL=3
MAX_SEQ_LEN=1024
```

### LoRA Configuration
```python
LoraConfig(
    r=16,                    # Low-rank dimension
    lora_alpha=32,          # Scaling parameter
    lora_dropout=0.05,      # Dropout rate
    target_modules=["q_proj", "v_proj"]  # Target attention layers
)
```

## 📊 Training Pipeline

```mermaid
graph LR
    A[📚 Raw Texts] --> B[🔄 Parse Bible]
    B --> C[🧠 Generate Embeddings]
    C --> D[☁️ Supabase Storage]
    D --> E[🎓 Format Training Data]
    E --> F[🔥 LoRA Training]
    F --> G[💾 Save Checkpoint]
    G --> H[☁️ Upload to Storage]
```

## 🎯 Model Architecture

- **Base Model**: Llama-3-8B-Instruct
- **Fine-tuning**: LoRA (Low-Rank Adaptation)
- **Format**: Alpaca instruction format
- **Context Length**: 1024 tokens
- **Precision**: FP16 for efficiency

## 📈 Performance & Monitoring

- ✅ **Automatic checkpointing** every 200 steps
- ✅ **Supabase storage** backup
- ✅ **Training logs** with loss tracking
- ✅ **Smoke testing** for validation

## 🐳 Docker Deployment

```dockerfile
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
# Optimized for SimplePod GPU environments
```

Run with:
```bash
docker build -t jotica .
docker run --gpus all -v $(pwd):/workspace jotica
```

## 🤝 Contributing

1. Fork the repository on the `main` branch
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request to `main`

## 📋 Data Format

### Training Data (bible_qa.jsonl)
```json
{
  "instruction": "Explica Juan 1:1 con enfoque en la deidad del Verbo",
  "input": "",
  "output": "Juan 1:1 (RVA1909): \"En el principio era el Verbo...\"",
  "topic": "cristología"
}
```

### Biblical Verses
```json
{
  "book": "Juan",
  "chapter": 1,
  "verse": 1,
  "text": "En el principio era el Verbo, y el Verbo era con Dios..."
}
```

## 🔧 Troubleshooting

### Common Issues
- **GPU Memory**: Reduce `BATCH_SIZE` if OOM errors occur
- **API Limits**: Check OpenAI rate limits for embeddings
- **Supabase**: Verify connection and storage permissions

### Debug Mode
```bash
# Enable verbose logging
export DEBUG=1
bash scripts/train_lora.sh
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 📖 **Reina-Valera 1909** - Public domain biblical text
- 🤗 **Hugging Face** - Transformers and PEFT libraries
- 🦙 **Meta AI** - Llama model architecture
- ☁️ **Supabase** - Vector database and storage

---

<div align="center">

**Made with ❤️ for Biblical AI Research**

[⭐ Star this repo](https://github.com/SwStudioAI/jotica) • [🐛 Report Bug](https://github.com/SwStudioAI/jotica/issues) • [💡 Request Feature](https://github.com/SwStudioAI/jotica/issues)

</div>
python src/ingest/create_embeddings.py
```

### 3. Generate Training Dataset

```bash
# Create Q&A pairs from biblical passages
python src/ingest/create_qa_dataset.py
```

### 4. Train LoRA Model

```bash
# Train on biblical Q&A dataset
python src/train/train_lora.py
```

### 5. Test Inference

```bash
# Test the trained model
python src/inference/test_model.py
```

## Docker Usage (SimplePod)

### Build Container

```bash
docker build -t jotica-bible .
```

### Run Training

```bash
docker run --gpus all \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/datasets:/app/datasets \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  jotica-bible
```

### Interactive Development

```bash
docker run --gpus all -it \
  -v $(pwd):/app \
  --env-file .env \
  jotica-bible bash
```

## Configuration

### Environment Variables

Required environment variables (see `.env.example`):

- `OPENAI_API_KEY`: For generating embeddings and Q&A pairs
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_SERVICE_KEY`: Supabase service key
- `WANDB_API_KEY`: (Optional) For experiment tracking

### Training Configuration

Edit `src/train/config.py` to customize:
- Base model selection
- LoRA parameters (rank, alpha, dropout)
- Training hyperparameters
- Dataset configuration

## Features

### Data Processing
- **Biblical Text Parsing**: Extracts verses, chapters, and books from RVA 1909
- **Embedding Generation**: Creates vector embeddings using OpenAI's text-embedding-ada-002
- **Vector Storage**: Stores embeddings in Supabase for semantic search

### Q&A Dataset Creation
- **Automated Generation**: Creates question-answer pairs from biblical passages
- **Context Integration**: Includes surrounding verses for better context
- **Commentary Integration**: Incorporates biblical commentary and cross-references

### LoRA Training
- **Parameter Efficient**: Uses PEFT library for memory-efficient training
- **Multiple Base Models**: Supports various Spanish language models
- **Quantization Support**: 4-bit and 8-bit quantization for GPU efficiency

### Inference Pipeline
- **Semantic Search**: Find relevant biblical passages
- **Contextual Responses**: Generate responses based on biblical context
- **Multi-turn Conversations**: Support for extended biblical discussions

## Training Details

### Base Models Supported
- `microsoft/DialoGPT-medium` (Spanish fine-tuned)
- `PlanTL-GOB-ES/gpt2-base-bne`
- `huggingface/CodeBERTa-small-v1`

### LoRA Configuration
- Rank: 16-64 (configurable)
- Alpha: 32-128 (configurable)
- Target modules: All attention layers
- Dropout: 0.1

### Training Parameters
- Batch size: 4-8 (depending on GPU memory)
- Learning rate: 1e-4 to 5e-4
- Epochs: 3-10
- Gradient accumulation: 4-8 steps

## Monitoring and Logging

### Weights & Biases Integration
- Training metrics tracking
- Model performance monitoring
- Hyperparameter optimization

### Local Logging
- Training progress logs in `logs/`
- Model checkpoints in `models/`
- Dataset statistics and validation

## Data Sources

### Biblical Texts
- **Primary**: Reina-Valera 1909 Spanish Bible
- **Format**: JSON with book/chapter/verse structure
- **Processing**: Automatic verse parsing and validation

### Training Data Generation
- Context-aware Q&A pairs
- Cross-reference integration
- Commentary incorporation
- Thematic grouping

## GPU Requirements

### Recommended Setup
- **VRAM**: 16GB+ for full precision training
- **VRAM**: 8GB+ with quantization
- **Compute**: CUDA 11.8+ compatible

### SimplePod Compatibility
- Designed for SimplePod Docker GPU environments
- Automatic GPU detection and utilization
- Memory optimization for cloud instances

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/biblical-enhancement`)
3. Commit changes (`git commit -am 'Add biblical feature'`)
4. Push to branch (`git push origin feature/biblical-enhancement`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Reina-Valera 1909 Bible text
- Hugging Face Transformers library
- PEFT (Parameter Efficient Fine-Tuning)
- OpenAI API for embeddings
- Supabase for vector storage