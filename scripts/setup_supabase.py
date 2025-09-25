#!/usr/bin/env python3
"""
🗄️ Supabase Bucket Setup Script
Creates jotica-bible bucket and configures storage for the project
"""

import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def setup_supabase_storage():
    """Create and configure Supabase storage buckets"""
    
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found in .env")
        print("Make sure to create .env file with your Supabase credentials")
        return False
        
    print(f"🔗 Connecting to Supabase: {url}")
    
    try:
        # Create Supabase client
        supabase = create_client(url, service_key)
        
        # Buckets to create
        buckets_config = [
            {
                "name": "jotica-bible",
                "public": False,
                "file_size_limit": 52428800,  # 50MB
                "allowed_mime_types": ["application/gzip", "application/zip", "application/octet-stream", "text/plain"]
            },
            {
                "name": "jotica-models", 
                "public": False,
                "file_size_limit": 1073741824,  # 1GB
                "allowed_mime_types": ["application/gzip", "application/zip", "application/octet-stream"]
            },
            {
                "name": "jotica-data",
                "public": False, 
                "file_size_limit": 104857600,  # 100MB
                "allowed_mime_types": ["text/plain", "application/json", "text/csv"]
            }
        ]
        
        for bucket in buckets_config:
            bucket_name = bucket["name"]
            
            try:
                # Check if bucket already exists
                existing_buckets = supabase.storage.list_buckets()
                bucket_exists = any(b.name == bucket_name for b in existing_buckets)
                
                if bucket_exists:
                    print(f"✅ Bucket '{bucket_name}' already exists")
                else:
                    # Create bucket
                    result = supabase.storage.create_bucket(
                        bucket_name,
                        options={
                            "public": bucket["public"],
                            "file_size_limit": bucket["file_size_limit"],
                            "allowed_mime_types": bucket["allowed_mime_types"]
                        }
                    )
                    print(f"✅ Created bucket '{bucket_name}': {result}")
                    
            except Exception as e:
                print(f"⚠️  Warning creating bucket '{bucket_name}': {str(e)}")
                continue
                
        # Test upload to verify permissions
        print("\n🧪 Testing bucket access...")
        
        test_content = "Jotica Bible Project - Test File"
        test_file_path = "test/connection_test.txt"
        
        try:
            # Upload test file
            result = supabase.storage.from_("jotica-bible").upload(
                test_file_path,
                test_content.encode('utf-8'),
                file_options={"content-type": "text/plain", "upsert": True}
            )
            print(f"✅ Test upload successful: {result}")
            
            # Download test file
            download = supabase.storage.from_("jotica-bible").download(test_file_path)
            print(f"✅ Test download successful: {len(download)} bytes")
            
            # Delete test file
            supabase.storage.from_("jotica-bible").remove([test_file_path])
            print("✅ Test file cleanup completed")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            return False
            
        print("\n🎉 Supabase storage setup completed successfully!")
        print("\n📋 Available buckets:")
        
        buckets = supabase.storage.list_buckets()
        for bucket in buckets:
            if bucket.name.startswith("jotica"):
                print(f"  • {bucket.name} - {'Public' if bucket.public else 'Private'}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {str(e)}")
        return False

def create_database_tables():
    """Create database tables for biblical data"""
    
    load_dotenv()
    url = os.getenv("SUPABASE_URL") 
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        print("❌ Missing Supabase credentials for database setup")
        return False
        
    try:
        supabase = create_client(url, service_key)
        
        print("\n📊 Setting up database tables...")
        
        # Bible verses table
        bible_verses_sql = """
        CREATE TABLE IF NOT EXISTS bible_verses (
            id SERIAL PRIMARY KEY,
            book VARCHAR(50) NOT NULL,
            chapter INTEGER NOT NULL,
            verse INTEGER NOT NULL,
            text TEXT NOT NULL,
            embedding VECTOR(1536),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(book, chapter, verse)
        );
        
        CREATE INDEX IF NOT EXISTS idx_bible_verses_book ON bible_verses(book);
        CREATE INDEX IF NOT EXISTS idx_bible_verses_chapter ON bible_verses(book, chapter);
        """
        
        # Bible references table  
        bible_refs_sql = """
        CREATE TABLE IF NOT EXISTS bible_refs (
            id SERIAL PRIMARY KEY,
            work VARCHAR(100) NOT NULL,
            ref_key VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            embedding VECTOR(1536),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_bible_refs_work ON bible_refs(work);
        CREATE INDEX IF NOT EXISTS idx_bible_refs_key ON bible_refs(ref_key);
        """
        
        # Execute SQL (Note: Direct SQL execution might need RPC function)
        print("📋 Tables SQL prepared (may need manual execution in Supabase dashboard)")
        print("SQL for bible_verses table:")
        print(bible_verses_sql)
        print("\nSQL for bible_refs table:")
        print(bible_refs_sql)
        
        return True
        
    except Exception as e:
        print(f"⚠️  Database setup info: {str(e)}")
        return True  # Continue even if DB setup has issues

if __name__ == "__main__":
    print("🗄️ Jotica Bible - Supabase Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("📋 Create .env file from .env.example:")
        print("   cp .env.example .env")
        print("   # Edit .env with your real credentials")
        sys.exit(1)
    
    # Setup storage buckets
    storage_success = setup_supabase_storage()
    
    # Setup database tables
    db_success = create_database_tables()
    
    if storage_success:
        print("\n🎯 Next steps:")
        print("1. Buckets are ready for file uploads")
        print("2. Run: bash scripts/ingest_bible.sh") 
        print("3. Run: bash scripts/train_lora.sh")
        print("\n🔗 Supabase Dashboard: https://app.supabase.com/")
    else:
        print("\n❌ Setup failed. Check your Supabase credentials.")
        sys.exit(1)