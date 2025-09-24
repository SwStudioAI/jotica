import os
import json

def read_text(p): 
    return open(p,encoding="utf-8").read()
    
def write_text(p,s): 
    open(p,"w",encoding="utf-8").write(s)
    
def basename(p): 
    return os.path.basename(p)
    
def read_jsonl(p):
    return [json.loads(x) for x in open(p,encoding="utf-8")]
    
def write_jsonl(p,rows):
    with open(p,"w",encoding="utf-8") as f:
        for r in rows: 
            f.write(json.dumps(r,ensure_ascii=False)+"\n")