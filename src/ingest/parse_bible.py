import argparse
import os
import json
import re
from ..utils.io_utils import write_jsonl

# Asume archivos por libro o un único TXT formateado (tú lo provees).
# Ajusta el parser a tu formato real.
def parse_rva1909(root):
    # MOCK: aquí iría el parser real; emitiré ejemplo mínimo
    # Estructura final: {"book":"Génesis","chapter":1,"verse":1,"text":"En el principio..."}
    raise NotImplementedError("Implementa parsing según tu fuente RVA1909.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--emit", required=True)
    args = ap.parse_args()
    rows = parse_rva1909(args.root)
    write_jsonl(args.emit, rows)