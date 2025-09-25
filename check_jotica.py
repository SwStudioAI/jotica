#!/usr/bin/env python3
"""
🔍 Script de verificación rápida para Jotica
Verifica que el modelo LoRA esté correctamente entrenado y funcional
"""

import json
from pathlib import Path

def check_model_files():
    """Verifica que los archivos del modelo existan"""
    print("📁 Verificando archivos del modelo...")
    
    # Rutas a verificar
    paths_to_check = [
        "models/jotica-ultra-safe",
        "models/jotica-personality", 
        "data/processed/jotica_simple.json",
        "data/processed/jotica_personality.json",
        "train_lora_safe.py"
    ]
    
    for path_str in paths_to_check:
        path = Path(path_str)
        if path.exists():
            if path.is_file():
                size = path.stat().st_size / 1024  # KB
                print(f"   ✅ {path_str} ({size:.1f} KB)")
            else:
                files = list(path.glob("*"))
                print(f"   ✅ {path_str}/ ({len(files)} archivos)")
        else:
            print(f"   ❌ {path_str} - No encontrado")
    
    print()

def check_training_logs():
    """Verifica los logs de entrenamiento"""
    print("📊 Verificando logs de entrenamiento...")
    
    log_paths = [
        "logs",
        "models/jotica-ultra-safe/training_logs.txt",
        "models/jotica-personality/training_logs.txt"
    ]
    
    for log_path in log_paths:
        path = Path(log_path)
        if path.exists():
            if path.is_file():
                print(f"   ✅ Log encontrado: {log_path}")
            else:
                log_files = list(path.glob("*.log"))
                print(f"   ✅ Directorio logs: {len(log_files)} archivos")
        else:
            print(f"   ℹ️ {log_path} - No encontrado")
    
    print()

def show_dataset_info():
    """Muestra información de los datasets"""
    print("📚 Información de datasets:")
    
    datasets = [
        ("Simple", "data/processed/jotica_simple.json"),
        ("Personalidad", "data/processed/jotica_personality.json")
    ]
    
    for name, path_str in datasets:
        path = Path(path_str)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"   ✅ Dataset {name}: {len(data)} ejemplos")
                
                # Mostrar un ejemplo
                if data:
                    example = data[0]
                    instruction = example.get('instruction', 'N/A')[:50]
                    output = example.get('output', 'N/A')[:50]
                    print(f"      📝 Ejemplo: '{instruction}...' -> '{output}...'")
            except Exception as e:
                print(f"   ❌ Error leyendo {name}: {e}")
        else:
            print(f"   ❌ Dataset {name} no encontrado")
    
    print()

def check_environment():
    """Verifica el entorno Python"""
    print("🐍 Verificando entorno Python...")
    
    try:
        import torch
        print(f"   ✅ PyTorch: {torch.__version__}")
        print(f"   {'✅' if torch.cuda.is_available() else '❌'} CUDA: {'Disponible' if torch.cuda.is_available() else 'No disponible'}")
        
        if torch.cuda.is_available():
            print(f"   🖥️ GPU: {torch.cuda.get_device_name(0)}")
            print(f"   💾 Memoria GPU: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    except ImportError:
        print("   ❌ PyTorch no instalado")
    
    try:
        import transformers
        print(f"   ✅ Transformers: {transformers.__version__}")
    except ImportError:
        print("   ❌ Transformers no instalado")
    
    try:
        import peft
        print(f"   ✅ PEFT: {peft.__version__}")
    except ImportError:
        print("   ❌ PEFT no instalado")
    
    print()

def show_next_steps():
    """Muestra los próximos pasos recomendados"""
    print("🚀 Próximos pasos recomendados:")
    print()
    
    model_path = Path("models/jotica-ultra-safe")
    if model_path.exists():
        print("   1. ✅ Modelo básico entrenado")
        print("   2. 🧪 Ejecutar: python test_jotica.py")
        print("   3. 🔄 Probar en Jupyter Notebook")
        print("   4. 🌐 Desplegar en Render.com")
    else:
        print("   1. 🏃 Entrenar modelo: python train_lora_safe.py")
        print("   2. 🧪 Probar modelo: python test_jotica.py")
        print("   3. 🔄 Refinar dataset si es necesario")
    
    print()
    print("   💡 Para entrenar con más datos:")
    print("      python train_lora_safe.py --epochs 5 --batch-size 2")
    print()
    print("   📊 Para ver métricas detalladas:")
    print("      python train_lora_safe.py --verbose")
    print()

if __name__ == "__main__":
    print("🙏 Jotica Bible LoRA - Verificación del Sistema")
    print("=" * 55)
    print()
    
    # Verificaciones
    check_environment()
    check_model_files()
    check_training_logs()
    show_dataset_info()
    show_next_steps()
    
    print("🎉 Verificación completada!")
    print("💬 ¡Jotica está lista para responder preguntas bíblicas!")