# 🛠️ Configuración Local de Jotica

## ❗ Problema Actual
- **Conectividad SimplePod**: IP 176.9.144.36 no responde (timeout)
- **Python Local**: No instalado o mal configurado en Windows
- **Modelo Entrenado**: Solo disponible en SimplePod (no accesible)

## 🔧 Solución Inmediata: Simulador Local

### 1. Instalar Python (Requerido)

#### Opción A: Microsoft Store (Recomendado)
1. Abrir Microsoft Store
2. Buscar "Python 3.11"
3. Instalar "Python 3.11"
4. Reiniciar terminal

#### Opción B: Descarga Directa
1. Ir a https://python.org/downloads/
2. Descargar Python 3.11+
3. **IMPORTANTE**: Marcar "Add Python to PATH"
4. Instalar y reiniciar

### 2. Verificar Instalación
```bash
python --version
pip --version
```

### 3. Instalar Dependencias Básicas
```bash
pip install transformers torch accelerate peft
```

## 🤖 Simulador de Jotica (Sin Entrenamiento)

Mientras solucionamos la conectividad, puedes usar Jotica en modo básico:

### Script Básico
```python
# jotica_basica.py
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

def crear_jotica_basica():
    print("🤖 Cargando Jotica básica...")
    
    # Usar modelo base sin entrenamiento
    model_name = "microsoft/DialoGPT-small" 
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

def responder_biblico(pregunta, model, tokenizer):
    """Generar respuesta con estilo bíblico"""
    
    # Prefijo para orientar hacia respuestas bíblicas
    contexto_biblico = "Como consejero cristiano, respondo con amor y sabiduría bíblica: "
    prompt = f"{contexto_biblico}{pregunta}"
    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    generation_config = GenerationConfig(
        max_length=150,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    
    with torch.no_grad():
        outputs = model.generate(inputs, generation_config=generation_config)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.replace(prompt, "").strip()

if __name__ == "__main__":
    print("🙏 Jotica Bible - Modo Básico")
    print("=" * 40)
    
    try:
        model, tokenizer = crear_jotica_basica()
        print("✅ Jotica básica cargada")
        print()
        
        preguntas_prueba = [
            "¿Cómo puedo tener paz?",
            "¿Qué dice la Biblia sobre el amor?",
            "¿Cómo puedo orar mejor?"
        ]
        
        for pregunta in preguntas_prueba:
            print(f"👤 Pregunta: {pregunta}")
            respuesta = responder_biblico(pregunta, model, tokenizer)
            print(f"🙏 Jotica: {respuesta}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que Python y las dependencias estén instaladas")
```

## 🔄 Reconectar a SimplePod

### Posibles Soluciones

#### 1. IP Dinámica Cambió
```bash
# Verificar nueva IP en panel de SimplePod
# Actualizar conexión SSH con nueva IP
ssh -i "C:\Users\georg\.ssh\simplepod_key" root@[NUEVA_IP]
```

#### 2. Instancia Pausada/Detenida
- Ir al panel de SimplePod
- Reactivar la instancia
- Esperar a que esté "Running"
- Intentar reconectar

#### 3. Problemas de Red
```bash
# Probar conectividad
ping 176.9.144.36

# Probar puerto SSH
telnet 176.9.144.36 22
```

### 4. Backup del Modelo
Si logras reconectar, hacer backup inmediatamente:

```bash
# Comprimir modelo entrenado
cd ~/jotica-bible
tar -czf jotica-models-backup.tar.gz models/

# Descargar via SCP
scp -i "C:\Users\georg\.ssh\simplepod_key" root@176.9.144.36:~/jotica-bible/jotica-models-backup.tar.gz ./
```

## 🚀 Alternativas de Entrenamiento

### 1. Google Colab (Gratis)
- GPU T4 disponible
- Subir código a Colab
- Entrenar modelo básico

### 2. Kaggle (Gratis) 
- 30 horas GPU/semana
- P100 disponible
- Notebooks públicos

### 3. Hugging Face Spaces
- Despliegue gratuito
- Integración directa
- Modelo público

## 📋 Checklist de Recuperación

### Inmediato (Hoy)
- [ ] Instalar Python localmente
- [ ] Probar simulador básico
- [ ] Verificar estado SimplePod

### Corto Plazo (Esta Semana)  
- [ ] Recuperar acceso a SimplePod
- [ ] Hacer backup completo del modelo
- [ ] Probar modelo entrenado

### Largo Plazo (Próximo Mes)
- [ ] Configurar entrenamiento en plataforma alternativa
- [ ] Desplegar en Render.com
- [ ] Expandir dataset de personalidad

## 💡 Consejos Importantes

1. **SimplePod es temporal** - Siempre haz backups
2. **Modelos locales** - Considera entrenar localmente si tienes GPU
3. **Cloud gratuito** - Google Colab es excelente alternativa
4. **Persistencia** - Guarda todo en GitHub/Supabase

---

**¡No te preocupes! Jotica seguirá funcionando. Solo necesitamos adaptarnos a la situación actual.** 🙏✨