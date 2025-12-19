"""
Test IPv6 connection to Supabase
"""
import os
from dotenv import load_dotenv
import socket

load_dotenv()

print("Testing IPv6 connectivity to Supabase...")

# Test if system supports IPv6
print("\n1. Checking IPv6 support on this system...")
try:
    # Try to create an IPv6 socket
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.close()
    print("   ✅ IPv6 is supported on this system")
except Exception as e:
    print(f"   ❌ IPv6 not supported: {e}")

# Try to resolve the Supabase hostname with IPv6
print("\n2. Resolving Supabase hostname (IPv6)...")
hostname = "db.cvdoboqcxqqzirawupca.supabase.co"
try:
    # Get all addresses (IPv4 and IPv6)
    addr_info = socket.getaddrinfo(hostname, 5432, socket.AF_UNSPEC, socket.SOCK_STREAM)
    print(f"   Found {len(addr_info)} address(es):")
    for info in addr_info:
        family, socktype, proto, canonname, sockaddr = info
        family_name = "IPv6" if family == socket.AF_INET6 else "IPv4"
        print(f"   - {family_name}: {sockaddr[0]}")
except Exception as e:
    print(f"   ❌ Cannot resolve: {e}")

# Try direct connection with original URL
print("\n3. Testing direct connection with original URL...")
DATABASE_URL = "postgresql://postgres:%23Enterprice123@db.cvdoboqcxqqzirawupca.supabase.co:5432/postgres"

try:
    import psycopg2
    print("   Attempting connection...")
    conn = psycopg2.connect(DATABASE_URL)
    print("   ✅ CONNECTION SUCCESSFUL!")
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"   PostgreSQL version: {version[0][:80]}")
    
    # List tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    print(f"   Existing tables: {[t[0] for t in tables] if tables else 'None'}")
    
    cur.close()
    conn.close()
    
    print("\n✅ SUCCESS! The direct connection works!")
    print("Your system supports IPv6 and can connect to Supabase.")
    
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    print("\n⚠️  Your system cannot connect via IPv6.")
    print("You need to either:")
    print("  1. Enable IPv6 on your network")
    print("  2. Purchase Supabase IPv4 add-on")
    print("  3. Use a different database provider")
