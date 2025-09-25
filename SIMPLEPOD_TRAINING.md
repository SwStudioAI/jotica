# 🚀 Guía Completa: Entrenar LoRA Bíblico en SimplePod.ai

## 📋 Prerrequisitos

1. **Cuenta en SimplePod.ai**: Regístrate en https://simplepod.ai/
2. **Créditos GPU**: Asegúrate de tener créditos para GPU (recomendado: A100 40GB)
3. **Archivos del repositorio**: Todos los archivos de `jotica-bible` listos

---

## 🏃‍♂️ Pasos para Entrenar

### 1️⃣ **Crear Nuevo Pod en SimplePod**

1. **Navega a SimplePod.ai**:
   - Ve a https://simplepod.ai/dashboard
   - Haz clic en "New Pod"

2. **Configuración del Pod**:
   ```
   Pod Name: jotica-bible-training
   Image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel
   GPU: A100 40GB (recomendado) o RTX 4090
   Storage: 50GB mínimo
   ```

3. **Variables de Entorno**:
   ```bash
   SUPABASE_URL=https://jmtrhukymrhzrmqmgrfq.supabase.co
   SUPABASE_SERVICE_ROLE=tu_service_role_key_aqui
   HUGGING_FACE_HUB_TOKEN=tu_hf_token_aqui  # opcional
   ```

### 2️⃣ **Subir Archivos al Pod**

**Opción A: Clonar desde GitHub**
```bash
git clone https://github.com/tu-usuario/jotica-bible.git
cd jotica-bible
```

**Opción B: Subir archivos manualmente**
- Usa la interfaz de SimplePod para subir el zip del repositorio
- Extrae en `/workspace/jotica-bible/`

### 3️⃣ **Configuración Inicial**

1. **Conecta al Pod**:
   - Haz clic en "Connect" en tu pod
   - Abre terminal o Jupyter

2. **Ejecuta el bootstrap**:
   ```bash
   cd /workspace/jotica-bible
   chmod +x scripts/*.sh
   ./scripts/bootstrap_simplepod.sh
   ```

   Esto instalará:
   - ✅ Dependencias Python
   - ✅ Datos bíblicos procesados
   - ✅ Configuración de entorno

### 4️⃣ **Preparar Datos Bíblicos**

```bash
# Procesar la Biblia RVA 1909
./scripts/ingest_bible.sh

# Verificar datos procesados
ls -la data/processed/
```

Deberías ver:
```
bible_qa_alpaca.json    # Dataset en formato Alpaca
bible_embeddings.npz    # Embeddings vectoriales  
bible_metadata.json    # Metadatos y estadísticas
```

### 5️⃣ **Iniciar Entrenamiento LoRA**

**Entrenamiento Rápido (Prueba)**:
```bash
./scripts/train_lora.sh --quick
```

**Entrenamiento Completo**:
```bash
./scripts/train_lora.sh \
  --model meta-llama/Llama-3-8B-Instruct \
  --epochs 3 \
  --batch-size 4 \
  --lr 2e-4 \
  --run-name "jotica-v1"
```

**Entrenamiento Personalizado**:
```bash
python src/train/lora_runner.py \
  --base-model meta-llama/Llama-3-8B-Instruct \
  --data data/processed/bible_qa_alpaca.json \
  --output models/jotica-lora \
  --run-name jotica-experimental \
  --epochs 5 \
  --batch-size 8 \
  --lr 1e-4 \
  --max-seq-len 2048
```

---

## 📊 Monitoreo del Entrenamiento

### **Logs en Tiempo Real**
```bash
# Ver progreso
tail -f logs/training.log

# Monitorear GPU
nvidia-smi -l 1
```

### **Métricas Esperadas**
```
🚀 Starting LoRA training: jotica-v1
   Model: meta-llama/Llama-3-8B-Instruct
   Dataset: 15,847 samples
   Epochs: 3
   Batch size: 4
   Output: models/jotica-lora

Epoch 1/3: 100%|██████| 3962/3962 [45:32<00:00, 1.45it/s]
Training Loss: 1.234

📦 Creating archive: jotica_jotica-v1_20241220_143022.tar.gz
☁️ Uploading to Supabase Storage...
🎉 Checkpoint successfully backed up to Supabase!
```

### **Tiempos Estimados** (A100 40GB)
- Dataset completo (15K samples): ~2-3 horas
- Prueba rápida (1K samples): ~15-20 minutos
- Upload a Supabase: ~2-5 minutos

---

## ☁️ Respaldo Automático

El sistema **guarda automáticamente** en Supabase:

### **¿Qué se guarda?**
- ✅ Modelo LoRA entrenado (`adapter_model.bin`)
- ✅ Configuración (`adapter_config.json`) 
- ✅ Tokenizer completo
- ✅ Metadatos de entrenamiento (`training_info.json`)
- ✅ Logs de entrenamiento

### **¿Dónde se guarda?**
```
Supabase Storage > jotica-models bucket:
├── jotica-v1/
│   └── jotica_jotica-v1_20241220_143022.tar.gz
├── jotica-experimental/  
│   └── jotica_jotica-experimental_20241220_154511.tar.gz
└── ...
```

### **Verificar Backup**
```bash
# Listar checkpoints en Supabase
python -c "from src.utils.supa import list_checkpoints; print(list_checkpoints())"
```

---

## 🔧 Solución de Problemas

### **Error: CUDA Out of Memory**
```bash
# Reducir batch size
python src/train/lora_runner.py --batch-size 2

# O usar gradient accumulation  
python src/train/lora_runner.py --batch-size 1 --gradient-accumulation-steps 4
```

### **Error: Supabase Connection**
```bash
# Verificar variables de entorno
echo $SUPABASE_URL
echo $SUPABASE_SERVICE_ROLE

# Probar conexión
python -c "from src.utils.supa import test_connection; test_connection()"
```

### **Error: Modelo No Encontrado**
```bash
# Verificar acceso HuggingFace
huggingface-cli login

# O usar modelo local
python src/train/lora_runner.py --base-model ./models/llama-3-8b-local/
```

---

## 🚀 Siguientes Pasos

### **1. Probar el Modelo Entrenado**
```bash
# Descargar desde Supabase
python src/utils/supa.py download jotica_jotica-v1_20241220_143022.tar.gz

# Extraer e iniciar API
tar -xzf jotica_*.tar.gz
python src/api/server.py --model-path ./models/jotica-lora/
```

### **2. Hacer Inferencia**
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "¿Qué dice la Biblia sobre el amor?",
    "max_length": 200
  }'
```

### **3. Entrenar Nuevas Versiones**
- Ajusta hiperparámetros
- Usa diferentes conjuntos de datos  
- Experimenta con otros modelos base

---

## 💡 Tips de Optimización

### **Para Entrenamiento Más Rápido**
- Usar A100 80GB si está disponible
- Aumentar `batch_size` a 8-16
- Usar `fp16=True` para ahorrar memoria

### **Para Mejor Calidad**
- Aumentar `epochs` a 5-10
- Usar `lr=1e-4` (learning rate más bajo)
- Aumentar `max_seq_len` a 4096

### **Para Experimentar**
- Cambiar `base_model` a otros modelos
- Modificar datos en `data/processed/`
- Ajustar parámetros LoRA en `src/config.py`

---

## 🆘 Soporte

- **Logs**: Revisa `logs/training.log` 
- **GitHub Issues**: Abre issue en el repositorio
- **SimplePod Support**: Contacta support@simplepod.ai
- **Supabase Dashboard**: https://app.supabase.com/project/jmtrhukymrhzrmqmgrfq/

---

¡**Feliz entrenamiento!** 🎉 Tu LoRA bíblico estará listo en unas horas y respaldado automáticamente en Supabase. ✨