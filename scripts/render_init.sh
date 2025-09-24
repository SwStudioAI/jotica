#!/bin/bash
# 🚀 Render.com Initialization Script for Jotica

set -e

echo "🕊️ Initializing Jotica Bible LoRA Training Platform on Render..."

# Check if we're in production
if [ "$NODE_ENV" = "production" ] || [ "$RENDER" = "true" ]; then
    echo "📦 Production environment detected"
    export PYTHONPATH="/opt/render/project/src:$PYTHONPATH"
else
    echo "🛠️  Development environment"
    export PYTHONPATH="./src:$PYTHONPATH"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p src/models/.cache
mkdir -p src/checkpoints
mkdir -p data/bible_rva1909
mkdir -p data/refs
mkdir -p logs

# Set permissions
chmod -R 755 src/
chmod +x scripts/*.sh

# Check Python installation
echo "🐍 Python version:"
python3 --version

# Check GPU availability (if CUDA available)
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU Status:"
    nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
else
    echo "⚠️  No GPU detected (CPU-only mode)"
fi

# Verify key dependencies
echo "📦 Verifying dependencies..."
python3 -c "import transformers; print(f'✅ Transformers: {transformers.__version__}')"
python3 -c "import fastapi; print(f'✅ FastAPI installed')" 
python3 -c "import openai; print(f'✅ OpenAI client ready')"

# Check environment variables
echo "🔧 Environment check:"
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
else
    echo "✅ OpenAI API key configured"
fi

if [ -z "$SUPABASE_URL" ]; then
    echo "⚠️  SUPABASE_URL not set"
else
    echo "✅ Supabase URL configured"
fi

echo "🎉 Jotica initialization complete!"
echo "🔗 API will be available at: https://your-app.onrender.com"
echo "📖 Documentation: https://your-app.onrender.com/docs"

# Start the application based on service type
if [ "$WORKER_MODE" = "true" ]; then
    echo "👷 Starting as training worker..."
    exec python3 -m src.train.worker
else
    echo "🌐 Starting API server..."
    exec python3 -m src.api.server
fi