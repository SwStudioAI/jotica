def format_row(r):
    inst = r["instruction"].strip()
    inp  = (r.get("input") or "").strip()
    out  = r["output"].strip()
    if inp:
        prompt = f"### Instrucción:\n{inst}\n\n### Entrada:\n{inp}\n\n### Respuesta:\n{out}"
    else:
        prompt = f"### Instrucción:\n{inst}\n\n### Respuesta:\n{out}"
    return prompt