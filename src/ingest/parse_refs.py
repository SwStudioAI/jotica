import argparse
import os
import glob
from ..utils.io_utils import read_text, write_jsonl

def chunk_text(txt, max_chars=2000, overlap=200):
    out, i = [], 0
    while i < len(txt):
        out.append(txt[i:i+max_chars])
        i += max_chars - overlap
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--emit", required=True)
    args = ap.parse_args()

    rows = []
    for p in glob.glob(os.path.join(args.root,"**","*.txt"), recursive=True):
        txt = read_text(p)
        work = "Unknown"  # ej: "Matthew Henry"
        ref_key = os.path.basename(p).replace(".txt","")  # ej: "Jn_1_1" o "Simbolos_Agua"
        for ch in chunk_text(txt):
            rows.append({"work":work,"ref_key":ref_key,"content":ch})
    write_jsonl(args.emit, rows)