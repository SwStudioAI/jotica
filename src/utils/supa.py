from supabase import create_client
from . import io_utils
from ..config import cfg
import os
import json
from datetime import datetime

# Create Supabase client
sb = create_client(cfg.supabase_url, cfg.supabase_service)

def upload_ckpt(local_path: str, prefix: str = "", bucket: str = None):
    """Upload checkpoint to Supabase Storage with detailed logging"""
    
    if bucket is None:
        bucket = cfg.bucket_ckpt
    
    try:
        print(f"📦 Uploading checkpoint to Supabase...")
        print(f"   Local file: {local_path}")
        print(f"   Bucket: {bucket}")
        
        # Check if file exists
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Checkpoint file not found: {local_path}")
        
        # Get file info
        file_size = os.path.getsize(local_path)
        print(f"   File size: {file_size / (1024*1024):.2f} MB")
        
        # Prepare remote path
        filename = io_utils.basename(local_path)
        remote_path = f"{prefix}{filename}" if prefix else filename
        print(f"   Remote path: {remote_path}")
        
        # Upload file
        with open(local_path, "rb") as f:
            result = sb.storage.from_(bucket).upload(
                path=remote_path,
                file=f,
                file_options={
                    "content-type": "application/gzip",
                    "upsert": True  # Overwrite if exists
                }
            )
        
        print(f"✅ Upload successful: {result}")
        
        # Save metadata
        metadata = {
            "filename": filename,
            "remote_path": remote_path,
            "bucket": bucket,
            "file_size_bytes": file_size,
            "upload_timestamp": datetime.now().isoformat(),
            "local_path": local_path,
            "run_prefix": prefix
        }
        
        # Save metadata to bucket
        metadata_path = f"{prefix}metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        metadata_content = json.dumps(metadata, indent=2).encode('utf-8')
        
        sb.storage.from_(bucket).upload(
            path=metadata_path,
            file=metadata_content,
            file_options={
                "content-type": "application/json",
                "upsert": True
            }
        )
        
        print(f"✅ Metadata saved: {metadata_path}")
        
        # Log to Supabase table (if exists)
        try:
            sb.table("training_checkpoints").insert({
                "run_name": cfg.run_name,
                "filename": filename,
                "remote_path": remote_path,
                "bucket": bucket,
                "file_size_bytes": file_size,
                "model_type": "LoRA",
                "status": "completed"
            }).execute()
            print("✅ Checkpoint logged to database")
        except Exception as e:
            print(f"⚠️ Database logging failed (table may not exist): {e}")
        
        return {
            "success": True,
            "remote_path": remote_path,
            "bucket": bucket,
            "file_size": file_size
        }
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def download_ckpt(remote_path: str, local_path: str, bucket: str = None):
    """Download checkpoint from Supabase Storage"""
    
    if bucket is None:
        bucket = cfg.bucket_ckpt
        
    try:
        print(f"📥 Downloading checkpoint from Supabase...")
        print(f"   Remote: {bucket}/{remote_path}")
        print(f"   Local: {local_path}")
        
        # Download file
        result = sb.storage.from_(bucket).download(remote_path)
        
        # Save to local file
        with open(local_path, 'wb') as f:
            f.write(result)
            
        file_size = len(result)
        print(f"✅ Download successful: {file_size / (1024*1024):.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return False

def list_checkpoints(prefix: str = "", bucket: str = None):
    """List available checkpoints in Supabase Storage"""
    
    if bucket is None:
        bucket = cfg.bucket_ckpt
        
    try:
        files = sb.storage.from_(bucket).list(prefix)
        
        checkpoints = []
        for file in files:
            if file.name.endswith('.tar.gz') or file.name.endswith('.zip'):
                checkpoints.append({
                    "name": file.name,
                    "size": file.metadata.get('size', 0) if file.metadata else 0,
                    "created": file.created_at,
                    "path": f"{prefix}/{file.name}" if prefix else file.name
                })
        
        return checkpoints
        
    except Exception as e:
        print(f"❌ Failed to list checkpoints: {str(e)}")
        return []