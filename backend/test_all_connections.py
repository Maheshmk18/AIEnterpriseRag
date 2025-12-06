"""
Try multiple Supabase connection string formats
"""
import psycopg2

# Your credentials
PROJECT_REF = "cvdoboqcxqqzirawupca"
PASSWORD = "%23Enterprice123"  # URL encoded

# Different connection string formats to try
connection_strings = [
    # Format 1: Direct connection (original)
    f"postgresql://postgres:{PASSWORD}@db.{PROJECT_REF}.supabase.co:5432/postgres",
    
    # Format 2: Transaction pooler (new format)
    f"postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-us-east-1.pooler.supabase.com:6543/postgres",
    
    # Format 3: Session pooler
    f"postgresql://postgres:{PASSWORD}@aws-0-us-east-1.pooler.supabase.com:5432/postgres?options=project%3D{PROJECT_REF}",
    
    # Format 4: Supavisor pooler (newer)
    f"postgresql://postgres.{PROJECT_REF}:{PASSWORD}@{PROJECT_REF}.pooler.supabase.com:6543/postgres",
    
    # Format 5: Alternative region (us-west)
    f"postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-us-west-1.pooler.supabase.com:6543/postgres",
    
    # Format 6: Alternative region (ap-southeast)
    f"postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres",
]

print("=" * 80)
print("TESTING MULTIPLE SUPABASE CONNECTION FORMATS")
print("=" * 80)

for i, conn_str in enumerate(connection_strings, 1):
    # Mask password for display
    display_str = conn_str.replace(PASSWORD, "[PASSWORD]")
    print(f"\n{i}. Testing: {display_str}")
    
    try:
        conn = psycopg2.connect(conn_str, connect_timeout=5)
        print("   ✅ ✅ ✅ CONNECTION SUCCESSFUL! ✅ ✅ ✅")
        
        # Test query
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"   PostgreSQL version: {version[0][:60]}...")
        
        # Check tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"   Tables: {[t[0] for t in tables] if tables else 'None'}")
        
        cur.close()
        conn.close()
        
        print(f"\n{'=' * 80}")
        print("✅ WORKING CONNECTION STRING FOUND!")
        print(f"{'=' * 80}")
        print(f"\nUse this in your .env file:")
        print(f"DATABASE_URL={conn_str}")
        print(f"\n{'=' * 80}")
        break
        
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        if "could not translate host name" in error_msg or "getaddrinfo failed" in error_msg:
            print("   ❌ DNS resolution failed")
        elif "Tenant or user not found" in error_msg:
            print("   ❌ Authentication/tenant error")
        elif "timeout" in error_msg.lower():
            print("   ❌ Connection timeout")
        else:
            print(f"   ❌ Error: {error_msg[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

print(f"\n{'=' * 80}")
print("If none of the above worked, your options are:")
print("1. Wait for DNS propagation (if project was just created/restarted)")
print("2. Try restarting your Supabase project")
print("3. Check your network/firewall settings")
print("4. Contact Supabase support")
print("5. Use a local database temporarily (SQLite/PostgreSQL)")
print(f"{'=' * 80}")
