#!/usr/bin/env python3
"""
🙏 Entrenamiento LoRA Apologético para Jotica
Versión especializada en responder objeciones ateas con fundamentos históricos
"""

import torch
import json
import argparse
from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments, 
    Trainer,
    GenerationConfig
)
from peft import LoraConfig, get_peft_model, TaskType

def setup_model_and_tokenizer(model_name):
    """Configurar modelo y tokenizer"""
    print(f'🤖 Cargando modelo: {model_name}')
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map='auto',
        trust_remote_code=True
    )
    
    # Configurar pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    print('🖥️ Modelo cargado en GPU')
    
    # Configurar LoRA para apologética (parámetros más conservadores)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,  # Rank más pequeño para entrenamiento más estable
        lora_alpha=16,  # Alpha proporcional
        lora_dropout=0.05,
        target_modules=['c_attn', 'c_proj'],  # DialoGPT modules
        bias='none'
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model, tokenizer

def load_apologetic_dataset(dataset_path):
    """Cargar y procesar dataset apologético"""
    print(f'🔍 Cargando dataset: {dataset_path}')
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f'📊 Dataset original: {len(data)} ejemplos')
    
    # Procesar datos para formato de entrenamiento
    processed_data = []
    for item in data:
        # Formato de conversación apologética
        text = f"""### Objeción: {item['instruction']}
### Respuesta Fundamentada: {item['output']}"""
        
        processed_data.append({
            'text': text,
            'input_ids': None,
            'labels': None
        })
    
    print(f'📊 Procesados {len(processed_data)} ejemplos válidos para apologética')
    return processed_data

def tokenize_dataset(data, tokenizer, max_length=1024):
    """Tokenizar dataset con longitud extendida para respuestas apologéticas"""
    print('🔤 Tokenizando dataset apologético...')
    
    def tokenize_function(examples):
        # Tokenizar texto
        tokenized = tokenizer(
            examples['text'],
            truncation=True,
            padding=False,
            max_length=max_length,
            return_tensors=None
        )
        
        # Para entrenamiento causal LM, labels = input_ids
        tokenized['labels'] = tokenized['input_ids'].copy()
        return tokenized
    
    # Convertir a Dataset de HuggingFace
    dataset = Dataset.from_list(data)
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names
    )
    
    print(f'✅ Tokenización completada: {len(tokenized_dataset)} ejemplos')
    return tokenized_dataset

def train_apologetic_model(model, tokenizer, dataset, output_dir, epochs=3):
    """Entrenar modelo apologético"""
    print('🚀 Iniciando entrenamiento apologético...')
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=1,  # Batch pequeño para estabilidad
        gradient_accumulation_steps=4,  # Simular batch size 4
        warmup_steps=50,
        learning_rate=1e-5,  # Learning rate conservador
        fp16=True,
        logging_steps=1,
        save_strategy='epoch',
        evaluation_strategy='no',
        load_best_model_at_end=False,
        report_to=None,
        remove_unused_columns=False,
        dataloader_pin_memory=False
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer
    )
    
    print('📈 Entrenamiento iniciado...')
    trainer.train()
    
    print('💾 Guardando modelo apologético...')
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    print('✅ Entrenamiento apologético completado!')
    return model, tokenizer

def test_apologetic_responses(model, tokenizer):
    """Probar respuestas apologéticas"""
    print('🧪 Probando respuestas apologéticas...')
    
    test_questions = [
        'Un ateo dice que Jesús nunca existió',
        'Me dicen que no hay evidencia arqueológica',
        'Alguien dice que la Biblia tiene contradicciones',
        'Un escéptico pregunta sobre el problema del mal'
    ]
    
    generation_config = GenerationConfig(
        max_length=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    
    for i, question in enumerate(test_questions, 1):
        prompt = f'### Objeción: {question}\n### Respuesta Fundamentada:'
        
        inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
        
        print(f'\n📝 Pregunta {i}: {question}')
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                generation_config=generation_config
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.replace(prompt, '').strip()
        
        print(f'🙏 Jotica Apologética: {response[:200]}...')
        print('-' * 60)

def main():
    parser = argparse.ArgumentParser(description='Entrenar Jotica Apologética')
    parser.add_argument('--model', default='microsoft/DialoGPT-small', 
                       help='Modelo base para entrenamiento')
    parser.add_argument('--dataset', default='data/processed/jotica_apologetica.json',
                       help='Dataset apologético')
    parser.add_argument('--output', default='models/jotica-apologetica',
                       help='Directorio de salida')
    parser.add_argument('--epochs', type=int, default=3,
                       help='Número de épocas')
    parser.add_argument('--test', action='store_true',
                       help='Probar respuestas después del entrenamiento')
    
    args = parser.parse_args()
    
    print('🛡️ Entrenamiento LoRA Apologético para Jotica')
    print(f'🤖 Modelo: {args.model}')
    print(f'📚 Dataset: {args.dataset}')
    print(f'📁 Salida: {args.output}')
    print(f'🔄 Épocas: {args.epochs}')
    print()
    
    # Crear directorio de salida
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    # Configurar modelo y tokenizer
    model, tokenizer = setup_model_and_tokenizer(args.model)
    
    # Cargar dataset apologético
    data = load_apologetic_dataset(args.dataset)
    
    # Tokenizar
    dataset = tokenize_dataset(data, tokenizer)
    
    # Entrenar
    model, tokenizer = train_apologetic_model(
        model, tokenizer, dataset, args.output, args.epochs
    )
    
    # Probar respuestas si se solicita
    if args.test:
        test_apologetic_responses(model, tokenizer)
    
    print('🎉 ¡Jotica Apologética entrenada exitosamente!')
    print('💡 Ahora puede responder objeciones ateas con fundamentos históricos sólidos')

if __name__ == '__main__':
    main()