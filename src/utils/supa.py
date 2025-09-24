from supabase import create_client
from . import io_utils
from ..config import cfg

sb = create_client(cfg.supabase_url, cfg.supabase_service)

def upload_ckpt(local_path:str, prefix:str=""):
    with open(local_path, "rb") as f:
        sb.storage.from_(cfg.bucket_ckpt).upload(
            file=f"{prefix}{io_utils.basename(local_path)}",
            file_content=f.read(),
            file_options={"upsert": True, "content-type":"application/gzip"}
        )