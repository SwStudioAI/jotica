#!/bin/bash

# 🚀 SimplePod Training Automation Script
# Uso: ./simplepod_train.sh [quick|full|custom]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'  
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_color() {
    echo -e "${1}${2}${NC}"
}

# Default parameters
MODE="full"
BASE_MODEL="meta-llama/Llama-3-8B-Instruct"
EPOCHS=3
BATCH_SIZE=4
LEARNING_RATE="2e-4"
RUN_NAME="jotica-$(date +%Y%m%d-%H%M)"
MAX_SEQ_LEN=2048

# Parse command line arguments
if [ $# -gt 0 ]; then
    MODE=$1
fi

case $MODE in
    "quick")
        echo_color $YELLOW "🏃‍♂️ Quick Training Mode (prueba rápida)"
        EPOCHS=1
        BATCH_SIZE=2
        RUN_NAME="jotica-quick-$(date +%H%M)"
        ;;
    "full")
        echo_color $GREEN "🎯 Full Training Mode (entrenamiento completo)"
        EPOCHS=3
        BATCH_SIZE=4
        ;;
    "custom")
        echo_color $BLUE "⚙️ Custom Training Mode"
        echo "Modify parameters in this script as needed"
        ;;
    *)
        echo_color $RED "❌ Unknown mode: $MODE"
        echo "Usage: $0 [quick|full|custom]"
        exit 1
        ;;
esac

echo_color $BLUE "==============================================="
echo_color $BLUE "🚀 JOTICA BIBLE LoRA TRAINING - SimplePod.ai"
echo_color $BLUE "==============================================="

# Check if running in SimplePod environment
if [[ ! -d "/workspace" ]]; then
    echo_color $RED "⚠️ Warning: Not detected SimplePod environment"
    echo_color $YELLOW "Make sure you're running this in SimplePod.ai"
fi

# Set working directory
WORKSPACE="/workspace/jotica-bible"
if [[ -d "/workspace/jotica-bible" ]]; then
    cd "$WORKSPACE"
else
    echo_color $RED "❌ Repository not found in /workspace/jotica-bible"
    echo_color $YELLOW "Please clone or upload the repository first"
    exit 1
fi

echo_color $GREEN "📂 Working directory: $WORKSPACE"

# Check GPU availability
echo_color $BLUE "\n🔍 Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits
    echo_color $GREEN "✅ GPU detected"
else
    echo_color $RED "❌ No GPU detected. Make sure you selected GPU instance in SimplePod"
    exit 1
fi

# Check environment variables
echo_color $BLUE "\n🔐 Checking environment variables..."
if [[ -z "$SUPABASE_URL" ]] || [[ -z "$SUPABASE_SERVICE_ROLE" ]]; then
    echo_color $YELLOW "⚠️ Supabase variables not set. Checkpoint backup will be disabled."
    echo "Set SUPABASE_URL and SUPABASE_SERVICE_ROLE in SimplePod environment"
else
    echo_color $GREEN "✅ Supabase configuration found"
fi

# Install dependencies if needed
echo_color $BLUE "\n📦 Installing dependencies..."
if [[ ! -f ".simplepod_setup_done" ]]; then
    echo_color $YELLOW "Installing requirements..."
    pip install -r requirements.txt --quiet
    touch .simplepod_setup_done
    echo_color $GREEN "✅ Dependencies installed"
else
    echo_color $GREEN "✅ Dependencies already installed"
fi

# Prepare data if needed
echo_color $BLUE "\n📚 Preparing biblical data..."
DATA_FILE="data/processed/bible_qa_alpaca.json"
if [[ ! -f "$DATA_FILE" ]]; then
    echo_color $YELLOW "Processing Bible data..."
    ./scripts/ingest_bible.sh
    echo_color $GREEN "✅ Bible data processed"
else
    echo_color $GREEN "✅ Bible data already available"
    SAMPLE_COUNT=$(jq length "$DATA_FILE" 2>/dev/null || echo "unknown")
    echo_color $BLUE "   Samples available: $SAMPLE_COUNT"
fi

# Memory optimization based on GPU
echo_color $BLUE "\n🧠 Optimizing for available memory..."
GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
if [[ $GPU_MEMORY -lt 20000 ]]; then
    echo_color $YELLOW "   Low GPU memory detected (<20GB), reducing batch size"
    BATCH_SIZE=2
elif [[ $GPU_MEMORY -gt 40000 ]]; then
    echo_color $GREEN "   High GPU memory detected (>40GB), increasing batch size"
    BATCH_SIZE=8
fi
echo_color $BLUE "   Using batch size: $BATCH_SIZE"

# Display training configuration
echo_color $BLUE "\n⚙️ Training Configuration:"
echo "   Mode: $MODE"
echo "   Model: $BASE_MODEL"
echo "   Run name: $RUN_NAME" 
echo "   Epochs: $EPOCHS"
echo "   Batch size: $BATCH_SIZE"
echo "   Learning rate: $LEARNING_RATE"
echo "   Max sequence length: $MAX_SEQ_LEN"

# Confirm before starting
echo_color $YELLOW "\n⏰ Training will start in 10 seconds..."
echo_color $YELLOW "Press Ctrl+C to cancel"
sleep 10

# Start training
echo_color $GREEN "\n🚀 Starting LoRA training..."
echo_color $BLUE "═══════════════════════════════════════════════"

# Create logs directory
mkdir -p logs

# Start training with all parameters
python src/train/lora_runner.py \
    --base-model "$BASE_MODEL" \
    --data "$DATA_FILE" \
    --output "models/$RUN_NAME" \
    --run-name "$RUN_NAME" \
    --epochs $EPOCHS \
    --batch-size $BATCH_SIZE \
    --lr "$LEARNING_RATE" \
    --max-seq-len $MAX_SEQ_LEN \
    --save-steps 500 \
    2>&1 | tee "logs/training_${RUN_NAME}.log"

# Training completed
TRAINING_EXIT_CODE=$?

echo_color $BLUE "\n═══════════════════════════════════════════════"

if [[ $TRAINING_EXIT_CODE -eq 0 ]]; then
    echo_color $GREEN "🎉 Training completed successfully!"
    
    # Show final model info
    if [[ -d "models/$RUN_NAME" ]]; then
        echo_color $BLUE "\n📊 Final Model Info:"
        echo "   Location: models/$RUN_NAME"
        echo "   Files:"
        ls -la "models/$RUN_NAME/" | head -10
        
        MODEL_SIZE=$(du -sh "models/$RUN_NAME" | cut -f1)
        echo "   Total size: $MODEL_SIZE"
    fi
    
    # Show Supabase backup status
    if [[ -n "$SUPABASE_URL" ]]; then
        echo_color $GREEN "☁️ Model automatically backed up to Supabase Storage"
        echo_color $BLUE "   Check: https://app.supabase.com/project/jmtrhukymrhzrmqmgrfq/storage/buckets"
    fi
    
    echo_color $GREEN "\n✨ Next steps:"
    echo "   1. Test the model: python src/api/server.py --model-path models/$RUN_NAME"
    echo "   2. Download from Supabase: Check the bucket for your checkpoint"
    echo "   3. Train another version: ./simplepod_train.sh custom"
    
else
    echo_color $RED "❌ Training failed with exit code: $TRAINING_EXIT_CODE"
    echo_color $YELLOW "Check the logs: logs/training_${RUN_NAME}.log"
fi

echo_color $BLUE "\n💡 Training session completed at $(date)"
echo_color $BLUE "📝 Logs saved to: logs/training_${RUN_NAME}.log"