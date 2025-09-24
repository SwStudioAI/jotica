# Pequeño test de inferencia (carga base + LoRA vía from_pretrained si guardas adapters, 
# o directo del checkpoint full si lo unes después).
# 
# Nota: La carga de LoRA puede hacerse con PEFT si se guardan adapters.
# Por ejemplo:
# from peft import PeftModel
# model = AutoModelForCausalLM.from_pretrained(base_model)
# model = PeftModel.from_pretrained(model, lora_adapter_path)

print("eval_smoke.py - Test de inferencia básica")
print("Implementar carga de LoRA + test con prompts de prueba")