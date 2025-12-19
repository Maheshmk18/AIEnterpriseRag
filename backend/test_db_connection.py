"""
Test Supabase database connection
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

print("Testing Supabase connection...")
print(f"Database URL present: {bool(DATABASE_URL)}")

if DATABASE_URL:
    # Mask sensitive parts
    parts = DATABASE_URL.split('@')
    if len(parts) == 2:
        print(f"Host part: {parts[1]}")
    
try:
    import psycopg2
    
    # Parse the connection string
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    print("\nAttempting to connect...")
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")
    
    # Test query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0][:100]}")
    
    # List existing tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    print(f"\nExisting tables: {[t[0] for t in tables] if tables else 'None'}")
    
    cur.close()
    conn.close()
    
except ImportError:
    print("❌ psycopg2 not installed. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "psycopg2-binary"])
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()
