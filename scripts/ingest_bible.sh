#!/usr/bin/env bash
set -e
export $(grep -v '^#' .env | xargs)
python -m src.ingest.parse_bible --root ./data/bible_rva1909/ --emit ./data/_parsed_bible.jsonl
python -m src.ingest.parse_refs  --root ./data/refs/          --emit ./data/_parsed_refs.jsonl
python -m src.ingest.upsert_supabase \
  --bible ./data/_parsed_bible.jsonl \
  --refs  ./data/_parsed_refs.jsonl