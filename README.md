# Jotica Bible - Biblical LoRA Training

Un sistema completo para entrenar modelos LoRA (Low-Rank Adaptation) en textos bíblicos usando la Reina-Valera 1909. Este proyecto está diseñado para funcionar en entornos SimplePod Docker con aceleración GPU.

## Estructura del Proyecto

```
jotica-bible/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ Dockerfile
├─ scripts/
│  ├─ bootstrap_simplepod.sh
│  ├─ ingest_bible.sh
│  └─ train_lora.sh
├─ data/
│  ├─ bible_rva1909/            # TXT/JSON por versículo
│  └─ refs/                     # Comentarios/TSK/Diccionarios
├─ datasets/
│  └─ bible_qa.jsonl            # Q&A curados
└─ src/
   ├─ config.py
   ├─ utils/
   │  ├─ supa.py
   │  ├─ emb.py
   │  └─ io_utils.py
   ├─ ingest/
   │  ├─ parse_bible.py
   │  ├─ parse_refs.py
   │  └─ upsert_supabase.py
   ├─ train/
   │  ├─ formatters.py
   │  ├─ lora_runner.py
   │  └─ eval_smoke.py
   └─ inference/
      └─ generate.py
```

## Inicio Rápido en SimplePod

### 1. Configuración del Entorno

```bash
# Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus claves API
```

### 2. Bootstrap Inicial

```bash
# Ejecutar una sola vez en SimplePod
bash scripts/bootstrap_simplepod.sh
```

### 3. Ingesta de Datos

```bash
# Procesar textos bíblicos y crear embeddings
bash scripts/ingest_bible.sh
```

### 4. Entrenar LoRA

```bash
# Iniciar entrenamiento LoRA
bash scripts/train_lora.sh
```

## Checkpoints y Almacenamiento

Los checkpoints se guardan en `/workspace/jotica/checkpoints` y se suben automáticamente a **Supabase Storage** en el bucket configurado (`jotica-models` por defecto).

## Variables de Entorno

Todas las variables importantes están definidas en `.env.example`. Las principales:

- `OPENAI_API_KEY`: Para generar embeddings
- `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE`: Para almacenar vectores y checkpoints
- `BASE_MODEL`: Modelo base (por defecto `meta-llama/Llama-3-8B-Instruct`)
- `OUTPUT_DIR`: Directorio de checkpoints
- Parámetros de entrenamiento: `EPOCHS`, `BATCH_SIZE`, `LR`, etc.

## Datos de Entrada

1. **bible_rva1909/**: Coloca aquí los textos de la RVA 1909 (formato a implementar en `parse_bible.py`)
2. **refs/**: Comentarios, diccionarios y materiales de referencia en formato TXT
3. **datasets/bible_qa.jsonl**: Dataset de preguntas y respuestas currado para el entrenamiento

## Testing del Modelo

Una vez entrenado, puedes probar el modelo con:

```bash
python -m src.inference.generate "Explica Juan 1:1 con citas."
```
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