#!/usr/bin/env python3
"""
🧪 Script de prueba para Jotica - Modelo LoRA entrenado
Prueba las respuestas del modelo entrenado con preguntas bíblicas
"""

import torch
import json
from pathlib import Path

def test_jotica_responses():
    """
    Prueba las respuestas de Jotica con preguntas bíblicas comunes
    """
    print("🤖 === Test de Respuestas de Jotica ===")
    print()
    
    # Verificar si existe el modelo entrenado
    model_path = Path("models/jotica-ultra-safe")
    if not model_path.exists():
        print(f"❌ Error: No se encontró el modelo en {model_path}")
        print("💡 Asegúrate de haber entrenado el modelo primero con:")
        print("   python3 train_lora_safe.py")
        return
    
    try:
        from peft import AutoPeftModelForCausalLM
        from transformers import AutoTokenizer, GenerationConfig
        
        print("🔄 Cargando modelo entrenado...")
        model = AutoPeftModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        print("🔄 Cargando tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        tokenizer.pad_token = tokenizer.eos_token
        
        print("✅ Modelo cargado exitosamente!")
        print("🧪 Iniciando pruebas de respuestas...")
        print("=" * 60)
        print()
        
        # Configuración de generación
        generation_config = GenerationConfig(
            max_length=200,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            top_k=50,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1
        )
        
        # Preguntas de prueba
        preguntas_biblicas = [
            "¿Qué dice la Biblia sobre el amor?",
            "¿Cómo puedo orar mejor?", 
            "¿Cuál es el propósito de la vida según la Biblia?",
            "¿Qué es el perdón cristiano?",
            "¿Cómo puedo tener paz en tiempos difíciles?"
        ]
        
        for i, pregunta in enumerate(preguntas_biblicas, 1):
            print(f"📝 Pregunta {i}: {pregunta}")
            
            # Formatear como conversación
            prompt = f"Usuario: {pregunta}\nJotica:"
            
            # Tokenizar
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Mover a GPU si está disponible
            if torch.cuda.is_available():
                inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            # Generar respuesta
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    generation_config=generation_config,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decodificar respuesta
            full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extraer solo la respuesta de Jotica
            if "Jotica:" in full_response:
                response = full_response.split("Jotica:")[-1].strip()
            else:
                response = full_response.replace(prompt, "").strip()
            
            # Limpiar respuesta
            response = response.replace("Usuario:", "").strip()
            if response.startswith(pregunta):
                response = response[len(pregunta):].strip()
            
            print(f"💬 Jotica: {response}")
            print("-" * 60)
            print()
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Instala las dependencias con: pip install transformers peft torch accelerate")
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        print("💡 Verifica que el modelo esté correctamente entrenado")

def test_model_info():
    """
    Muestra información del modelo entrenado
    """
    print("📊 === Información del Modelo ===")
    
    model_path = Path("models/jotica-ultra-safe")
    if model_path.exists():
        print(f"✅ Modelo encontrado en: {model_path}")
        
        # Verificar archivos del modelo
        files = list(model_path.glob("*"))
        print(f"📁 Archivos del modelo ({len(files)}):")
        for file in files:
            print(f"   - {file.name}")
        
        # Verificar configuración
        config_path = model_path / "adapter_config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("⚙️ Configuración LoRA:")
            print(f"   - Rank (r): {config.get('r', 'N/A')}")
            print(f"   - Alpha: {config.get('lora_alpha', 'N/A')}")
            print(f"   - Dropout: {config.get('lora_dropout', 'N/A')}")
            print(f"   - Módulos objetivo: {config.get('target_modules', 'N/A')}")
    else:
        print(f"❌ Modelo no encontrado en: {model_path}")
    
    print()

if __name__ == "__main__":
    print("🙏 Jotica Bible LoRA - Test de Respuestas")
    print("=" * 50)
    print()
    
    # Mostrar información del sistema
    print("🖥️ Información del sistema:")
    print(f"   - PyTorch: {torch.__version__}")
    print(f"   - CUDA disponible: {'Sí' if torch.cuda.is_available() else 'No'}")
    if torch.cuda.is_available():
        print(f"   - GPU: {torch.cuda.get_device_name(0)}")
    print()
    
    # Probar información del modelo
    test_model_info()
    
    # Probar respuestas
    test_jotica_responses()
    
    print("🎉 ¡Prueba completada!")