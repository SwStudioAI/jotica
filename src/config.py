from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()

class Cfg(BaseModel):
    openai_key: str = os.getenv("OPENAI_API_KEY","")
    supabase_url: str = os.getenv("SUPABASE_URL","")
    supabase_service: str = os.getenv("SUPABASE_SERVICE_ROLE","")
    bucket_ckpt: str = os.getenv("SUPABASE_BUCKET","jotica-models")
    base_model: str = os.getenv("BASE_MODEL","meta-llama/Llama-3-8B-Instruct")
    output_dir: str = os.getenv("OUTPUT_DIR","/workspace/jotica/checkpoints")
    run_name: str = os.getenv("RUN_NAME","jotica-bible-lora-001")

cfg = Cfg()