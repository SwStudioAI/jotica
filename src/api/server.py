#!/usr/bin/env python3
"""
🚀 Jotica Bible API Server for Render Deployment
Simple FastAPI server for biblical AI inference
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import logging
from typing import Optional

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = FastAPI(
    title="🕊️ Jotica Bible API",
    description="Biblical AI inference using LoRA fine-tuned models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class GenerateResponse(BaseModel):
    response: str
    model: str
    tokens_used: int

@app.get("/")
async def root():
    """Root endpoint with project information"""
    return {
        "message": "🕊️ Jotica Bible API",
        "description": "Biblical AI inference using LoRA fine-tuned models",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate",
            "health": "/health", 
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {
        "status": "healthy",
        "service": "jotica-bible-api",
        "timestamp": "2025-09-24T00:00:00Z"
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate biblical AI responses"""
    try:
        # For now, return a mock response
        # In production, this would use the actual LoRA model
        mock_response = f"""
### Respuesta Bíblica:

Basado en tu pregunta: "{request.prompt}"

Esta es una respuesta generada por el sistema Jotica Bible LoRA. 
En la implementación completa, aquí se cargaría el modelo fine-tuned 
y se generaría una respuesta teológicamente informada basada en la RVA 1909.

📖 *Versículo relacionado*: "En el principio era el Verbo, y el Verbo era con Dios, y el Verbo era Dios" (Juan 1:1 RVA1909)

🔍 *Análisis*: Esta respuesta sería generada por un modelo LoRA especializado en textos bíblicos.
        """.strip()
        
        return GenerateResponse(
            response=mock_response,
            model="jotica-bible-lora-001",
            tokens_used=len(mock_response.split())
        )
        
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/train/trigger")
async def trigger_training():
    """Trigger model training (for worker service)"""
    if not os.getenv("WORKER_MODE"):
        raise HTTPException(status_code=403, detail="Training only available on worker service")
    
    # In production, this would trigger the training pipeline
    return {
        "message": "Training pipeline triggered",
        "status": "queued",
        "estimated_time": "2-4 hours"
    }

@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "available_models": [
            {
                "name": "jotica-bible-lora-001",
                "type": "LoRA fine-tuned",
                "base_model": "meta-llama/Llama-3-8B-Instruct",
                "status": "ready",
                "specialized_in": "Biblical texts (RVA 1909)"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)