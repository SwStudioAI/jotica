#!/usr/bin/env bash
set -e

echo "[+] Cargando .env"
export $(grep -v '^#' .env | xargs)

echo "[+] Verificando GPU"
nvidia-smi || true

echo "[+] Instalando deps (si hace falta)"
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Estructura OK. Usa:"
echo "  bash scripts/ingest_bible.sh"
echo "  bash scripts/train_lora.sh"