from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import sys

BASE = "meta-llama/Llama-3-8B-Instruct"
tok = AutoTokenizer.from_pretrained(BASE)
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype="auto", device_map="auto")

def run(q:str):
    prompt = f"### Instrucción:\n{q}\n\n### Respuesta:\n"
    x = tok(prompt, return_tensors="pt").to(model.device)
    y = model.generate(**x, max_new_tokens=512, temperature=0.7, top_p=0.9)
    print(tok.decode(y[0], skip_special_tokens=True))

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv)>1 else "Explica Juan 1:1 con citas.")