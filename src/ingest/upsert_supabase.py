import argparse
from ..utils.io_utils import read_jsonl
from ..utils.emb import embed
from ..utils import io_utils
from ..config import cfg
from supabase import create_client

sb = create_client(cfg.supabase_url, cfg.supabase_service)

def upsert_bible(rows):
    for r in rows:
        e = embed(r["text"])
        sb.table("bible_verses").upsert({
            "book": r["book"], "chapter": r["chapter"], "verse": r["verse"],
            "text": r["text"], "embedding": e
        }).execute()

def upsert_refs(rows):
    for r in rows:
        e = embed(r["content"])
        sb.table("bible_refs").insert({
            "work": r["work"], "ref_key": r["ref_key"],
            "content": r["content"], "embedding": e
        }).execute()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bible", required=True)
    ap.add_argument("--refs", required=True)
    args = ap.parse_args()
    upsert_bible(read_jsonl(args.bible))
    upsert_refs(read_jsonl(args.refs))