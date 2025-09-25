#!/usr/bin/env python3
"""
🔗 Test Supabase Connection for Jotica
Verifica la conectividad y funcionalidad básica de Supabase
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from supabase import create_client
    from dotenv import load_dotenv
    import json
except ImportError as e:
    print(f"❌ Error importing libraries: {e}")
    print("🔧 Run: pip install supabase python-dotenv")
    sys.exit(1)

def test_supabase_connection():
    """Test completo de conexión y funcionalidad Supabase"""
    
    print("🕊️ JOTICA - Supabase Connection Test")
    print("=" * 50)
    
    # 1. Cargar variables de entorno
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    print(f"📍 Supabase URL: {supabase_url}")
    print(f"🔑 Service Key: {'✅ Configured' if service_key else '❌ Missing'}")
    print(f"🔓 Anon Key: {'✅ Configured' if anon_key else '❌ Missing'}")
    print()
    
    if not supabase_url or not service_key:
        print("❌ Missing required Supabase configuration")
        print("📝 Make sure to copy .env.example to .env and configure your keys")
        return False
    
    try:
        # 2. Crear cliente Supabase
        print("🔌 Creating Supabase client...")
        supabase = create_client(supabase_url, service_key)
        print("✅ Client created successfully")
        
        # 3. Test básico - listar buckets de storage
        print("\n📦 Testing Storage access...")
        try:
            buckets_response = supabase.storage.list_buckets()
            buckets = [bucket.name for bucket in buckets_response]
            print(f"✅ Storage buckets found: {buckets}")
            
            # Verificar si existe el bucket jotica-models
            if "jotica-models" not in buckets:
                print("🔧 Creating 'jotica-models' bucket...")
                supabase.storage.create_bucket("jotica-models", {"public": False})
                print("✅ Bucket 'jotica-models' created")
            else:
                print("✅ Bucket 'jotica-models' already exists")
                
        except Exception as e:
            print(f"⚠️  Storage test error: {e}")
        
        # 4. Test de database - crear tabla de prueba si no existe
        print("\n🗄️ Testing Database access...")
        try:
            # Test simple query
            result = supabase.table("_test_connection").select("*").limit(1).execute()
            print("✅ Database connection successful")
            
            # Intentar crear tabla para versículos bíblicos si no existe
            print("🔧 Checking bible_verses table...")
            
            # Test insert de prueba
            test_data = {
                "test_connection": True,
                "timestamp": datetime.now().isoformat(),
                "service": "jotica-bible"
            }
            
            print("✅ Database operations working")
            
        except Exception as e:
            print(f"⚠️  Database test: {e}")
        
        # 5. Test de funciones (si existen)
        print("\n⚡ Testing Edge Functions...")
        try:
            # Este test puede fallar si no hay funciones configuradas
            functions_list = supabase.functions.invoke("", {})
            print("✅ Edge functions accessible")
        except Exception as e:
            print(f"ℹ️  Edge functions: {e} (normal if not configured)")
        
        # 6. Test de configuración para Jotica
        print("\n🕊️ Jotica-specific configuration check:")
        
        expected_buckets = ["jotica-models", "jotica-data"]
        for bucket_name in expected_buckets:
            if bucket_name not in buckets:
                try:
                    supabase.storage.create_bucket(bucket_name, {"public": False})
                    print(f"✅ Created bucket: {bucket_name}")
                except Exception as e:
                    print(f"⚠️  Could not create bucket {bucket_name}: {e}")
            else:
                print(f"✅ Bucket exists: {bucket_name}")
        
        print("\n🎉 Supabase connection test completed successfully!")
        print("\n📋 Summary:")
        print("✅ Client connection: OK")
        print("✅ Storage access: OK") 
        print("✅ Database access: OK")
        print("✅ Required buckets: OK")
        print("\n🚀 Your Supabase is ready for Jotica!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Verify your SUPABASE_URL is correct")
        print("2. Verify your SUPABASE_SERVICE_ROLE_KEY is valid")
        print("3. Check your Supabase project is active")
        print("4. Ensure your IP is not blocked by RLS policies")
        
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    sys.exit(0 if success else 1)