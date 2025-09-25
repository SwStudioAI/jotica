# 🙏 Jotica Bible - Guía de Uso Completa

## 🚀 Inicio Rápido

### Para Probar Jotica Ahora Mismo (SimplePod)
```bash
# Conectar a tu servidor entrenado
ssh -i "~/.ssh/simplepod_key" root@176.9.144.36

# Ir al proyecto y activar entorno
cd ~/jotica-bible && source venv/bin/activate

# Conversación simple con Jotica
python3 -c "
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer, GenerationConfig
import torch

# Cargar modelo entrenado con personalidad
print('🤖 Cargando Jotica...')
model = AutoPeftModelForCausalLM.from_pretrained(
    'models/jotica-personality',
    torch_dtype=torch.float16,
    device_map='auto'
)
tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
tokenizer.pad_token = tokenizer.eos_token

print('✅ ¡Jotica lista!')
print('💬 Pregúntale algo bíblico...')
print()

# Configurar respuestas naturales
generation_config = GenerationConfig(
    max_length=200,
    do_sample=True, 
    temperature=0.8,
    top_p=0.9,
    repetition_penalty=1.1,
    pad_token_id=tokenizer.eos_token_id
)

# Preguntas de ejemplo
preguntas = [
    '¿Cómo puedo perdonar a alguien que me lastimó?',
    '¿Qué dice la Biblia sobre la ansiedad?',
    '¿Cómo puedo acercarme más a Dios?'
]

for pregunta in preguntas:
    print(f'👤 Tú: {pregunta}')
    
    # Formatear como conversación natural
    prompt = f'Usuario: {pregunta}\nJotica:'
    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
    
    # Generar respuesta
    with torch.no_grad():
        outputs = model.generate(**inputs, generation_config=generation_config)
    
    # Extraer respuesta
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if 'Jotica:' in response:
        response = response.split('Jotica:')[-1].strip()
    
    print(f'🙏 Jotica: {response}')
    print('-' * 50)
    print()
"
```

## 🤖 Ejemplos de Conversación

### Pregunta Típica
```
👤 Usuario: "Me siento muy ansioso por el futuro, ¿qué puedo hacer?"

🙏 Jotica: "Entiendo perfectamente esa preocupación por el futuro, es algo muy humano. La Biblia nos recuerda en Filipenses 4:6-7 que no nos afanemos por nada, sino que en todo, por oración y ruego, con acción de gracias, presentemos nuestras peticiones a Dios. 

Cuando Jesús enseñó en Mateo 6:26, nos dijo que miráramos las aves del cielo: no siembran, ni siegan, pero nuestro Padre celestial las alimenta. ¿No valemos nosotros mucho más que ellas?

Te animo a que cada mañana le entregues tus preocupaciones a Dios en oración. Él conoce tus necesidades antes de que se las pidas. ¿Has probado escribir tus inquietudes y después orar específicamente por cada una?"
```

### Respuesta sobre Perdón
```
👤 Usuario: "Alguien me traicionó y no sé si puedo perdonarlo"

🙏 Jotica: "Ay, qué dolor tan profundo debe ser eso. La traición de alguien en quien confiábamos es una de las heridas más difíciles de sanar. Te comprendo completamente.

Jesús nos enseñó en Mateo 18:21-22 que debemos perdonar no solo siete veces, sino setenta veces siete. Pero esto no significa que debemos olvidar o confiar ciegamente otra vez.

El perdón es más para tu propia libertad que para la otra persona. Como dice Efesios 4:32, perdonamos porque Cristo nos perdonó primero. Es un proceso, no un evento de una sola vez.

¿Te ayudaría comenzar orando por esa persona? No necesariamente pidiendo bendiciones, sino simplemente llevándola ante Dios. A veces el perdón comienza ahí, en la oración."
```

## 🛠️ Uso Técnico Avanzado

### Cargar Modelo Programáticamente
```python
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer, GenerationConfig
import torch

class JoticaBible:
    def __init__(self, model_path="models/jotica-personality"):
        """Inicializar Jotica con modelo entrenado"""
        self.model = AutoPeftModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.generation_config = GenerationConfig(
            max_length=300,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.15,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )
    
    def responder(self, pregunta):
        """Generar respuesta bíblica empática"""
        prompt = f"Usuario: {pregunta}\nJotica:"
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                generation_config=self.generation_config
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extraer solo la respuesta de Jotica
        if "Jotica:" in response:
            response = response.split("Jotica:")[-1].strip()
        
        return response
    
    def conversacion_interactiva(self):
        """Modo conversación interactiva"""
        print("🙏 ¡Hola! Soy Jotica, tu asistente bíblico.")
        print("💬 Puedes preguntarme sobre la Biblia, fe, o cualquier inquietud espiritual.")
        print("✨ Escribe 'salir' para terminar la conversación.\n")
        
        while True:
            pregunta = input("👤 Tú: ").strip()
            
            if pregunta.lower() in ['salir', 'exit', 'quit', 'adiós']:
                print("🙏 ¡Que Dios te bendiga! Espero haberte ayudado.")
                break
            
            if not pregunta:
                continue
            
            print("🤔 Jotica está pensando...")
            respuesta = self.responder(pregunta)
            print(f"🙏 Jotica: {respuesta}\n")

# Uso
if __name__ == "__main__":
    jotica = JoticaBible()
    jotica.conversacion_interactiva()
```

### API REST con FastAPI
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Jotica Bible API", version="1.0.0")
jotica = None

class PreguntaRequest(BaseModel):
    pregunta: str
    temperatura: float = 0.8

class RespuestaResponse(BaseModel):
    pregunta: str
    respuesta: str
    version_modelo: str

@app.on_event("startup")
async def cargar_modelo():
    global jotica
    jotica = JoticaBible("models/jotica-personality")
    print("✅ Jotica cargada y lista")

@app.post("/preguntar", response_model=RespuestaResponse)
async def hacer_pregunta(request: PreguntaRequest):
    if not jotica:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    
    try:
        respuesta = jotica.responder(request.pregunta)
        return RespuestaResponse(
            pregunta=request.pregunta,
            respuesta=respuesta,
            version_modelo="jotica-personality-v1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/salud")
async def check_salud():
    return {"estado": "saludable", "modelo": "jotica-personality-v1"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔧 Configuraciones Avanzadas

### Personalizar Respuestas
```python
# Respuestas más cortas y directas
generation_config = GenerationConfig(
    max_length=150,
    temperature=0.6,
    top_p=0.8,
    repetition_penalty=1.1
)

# Respuestas más creativas y largas  
generation_config = GenerationConfig(
    max_length=400,
    temperature=1.0,
    top_p=0.95,
    top_k=40,
    repetition_penalty=1.2
)

# Respuestas muy conservadoras
generation_config = GenerationConfig(
    max_length=200,
    do_sample=False,  # Determinístico
    num_beams=5,
    early_stopping=True
)
```

### Filtros de Contenido
```python
def validar_pregunta(pregunta):
    """Validar que la pregunta sea apropiada"""
    palabras_prohibidas = ["violencia", "odio", "discriminación"]
    
    pregunta_lower = pregunta.lower()
    for palabra in palabras_prohibidas:
        if palabra in pregunta_lower:
            return False, f"No puedo responder preguntas sobre {palabra}"
    
    return True, "Pregunta válida"

def mejorar_respuesta(respuesta):
    """Mejorar formato de respuesta"""
    # Agregar versículos si no los tiene
    if "Biblia" in respuesta and not any(libro in respuesta for libro in ["Mateo", "Juan", "Génesis", "Salmos"]):
        respuesta += "\n\n💡 Te recomiendo leer más en los Salmos para profundizar en este tema."
    
    return respuesta
```

## 📊 Monitoreo y Logs

### Logging Detallado
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jotica.log'),
        logging.StreamHandler()
    ]
)

def responder_con_logs(self, pregunta):
    """Responder con logging detallado"""
    logging.info(f"Nueva pregunta recibida: {pregunta[:50]}...")
    
    start_time = time.time()
    respuesta = self.responder(pregunta)
    end_time = time.time()
    
    logging.info(f"Respuesta generada en {end_time - start_time:.2f}s")
    logging.info(f"Longitud respuesta: {len(respuesta)} caracteres")
    
    return respuesta
```

## 🌐 Despliegue en Producción

### Docker para Render.com
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "api_server.py"]
```

### Variables de Entorno
```bash
# Render.com Environment Variables
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
MODELO_PATH=models/jotica-personality
PORT=8000
```

## 🎯 Casos de Uso Recomendados

### 1. Consejería Bíblica Personal
- Preguntas sobre relaciones, ansiedad, propósito
- Respuestas empáticas con base escritural
- Seguimiento conversacional natural

### 2. Estudio Bíblico Interactivo  
- Explicación de pasajes
- Aplicación práctica de principios
- Contexto histórico y cultural

### 3. Oración y Meditación
- Guías de oración personalizadas
- Reflexiones diarias
- Versículos para memorizar

### 4. Apoyo Emocional Cristiano
- Comfort en tiempos difíciles
- Esperanza basada en las Escrituras
- Perspectiva bíblica sobre problemas actuales

## 📞 Soporte y Resolución de Problemas

### Problemas Comunes

**Error de memoria CUDA:**
```bash
export CUDA_VISIBLE_DEVICES=0
python3 -c "import torch; torch.cuda.empty_cache()"
```

**Modelo no carga:**
```python
# Verificar archivos
import os
print(os.listdir("models/jotica-personality"))

# Cargar sin GPU
model = AutoPeftModelForCausalLM.from_pretrained(
    "models/jotica-personality",
    device_map="cpu",
    torch_dtype=torch.float32
)
```

**Respuestas repetitivas:**
```python
# Aumentar repetition_penalty
generation_config.repetition_penalty = 1.3

# Usar nucleus sampling
generation_config.top_p = 0.8
generation_config.temperature = 0.9
```

---

## 🙏 Bendiciones y Propósito

Jotica ha sido creada para ser un puente entre la sabiduría eterna de las Escrituras y las necesidades cotidianas de las personas. Su propósito es ofrecer consuelo, guía y esperanza basados en la Palabra de Dios, siempre con amor, comprensión y respeto.

*"La hierba se seca, la flor se marchita; mas la palabra del Dios nuestro permanece para siempre." - Isaías 40:8*

**¡Que Jotica sea de bendición para muchas vidas!** 🙏✨