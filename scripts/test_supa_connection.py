#!/usr/bin/env python3
"""
🧪 Simple Supabase Connection Test
Quick test to verify Supabase setup and bucket access
"""

import os
import sys
from supabase import create_client
from dotenv import load_dotenv

def test_supabase_connection():
    """Test basic Supabase connection and bucket access"""
    
    load_dotenv()
    
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    print("🧪 Jotica Bible - Supabase Connection Test")
    print("=" * 50)
    print(f"🔗 URL: {url}")
    print(f"🔑 Key: {service_key[:20]}..." if service_key else "❌ No service key")
    
    try:
        # Create client
        supabase = create_client(url, service_key)
        print("✅ Supabase client created successfully")
        
        # List buckets
        buckets = supabase.storage.list_buckets()
        print(f"\n📦 Available buckets ({len(buckets)}):")
        
        jotica_buckets = []
        for bucket in buckets:
            if 'jotica' in bucket.name:
                jotica_buckets.append(bucket.name)
                print(f"  ✅ {bucket.name} - {'Public' if bucket.public else 'Private'}")
        
        if not jotica_buckets:
            print("  ❌ No jotica buckets found")
            return False
            
        # Test simple bucket access (list files)
        print(f"\n📋 Testing bucket access...")
        for bucket_name in jotica_buckets[:1]:  # Test first bucket only
            try:
                files = supabase.storage.from_(bucket_name).list()
                print(f"  ✅ {bucket_name}: {len(files)} files")
            except Exception as e:
                print(f"  ⚠️ {bucket_name}: {str(e)}")
        
        print("\n🎉 Connection test completed!")
        print("\n🔗 Supabase Dashboard: https://app.supabase.com/project/jmtrhukymrhzrmqmgrfq")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    
    if success:
        print("\n✅ Supabase is ready for Jotica!")
        print("\n📋 Next steps:")
        print("1. Add your biblical data to data/bible_rva1909/")
        print("2. Run: bash scripts/ingest_bible.sh")
        print("3. Run: bash scripts/train_lora.sh")
    else:
        print("\n❌ Please check your Supabase configuration")
        sys.exit(1)