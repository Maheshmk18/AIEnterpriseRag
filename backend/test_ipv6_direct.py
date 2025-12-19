"""
Test connection using IPv6 address directly
"""
import psycopg2

# IPv6 address from nslookup
ipv6_address = "2406:da1a:6b0:f60d:2572:5684:cacc:f38b"
password = "#Enterprice123"

# Format for IPv6: use brackets around the IP
connection_strings = [
    # Format 1: IPv6 with brackets
    f"postgresql://postgres:{password}@[{ipv6_address}]:5432/postgres",
    
    # Format 2: IPv6 URL encoded password
    f"postgresql://postgres:%23Enterprice123@[{ipv6_address}]:5432/postgres",
]

print("Testing IPv6 direct connection...")
print(f"IPv6 Address: {ipv6_address}\n")

for i, conn_str in enumerate(connection_strings, 1):
    print(f"{i}. Testing connection...")
    try:
        conn = psycopg2.connect(conn_str, connect_timeout=10)
        print("   ✅ ✅ ✅ CONNECTION SUCCESSFUL! ✅ ✅ ✅\n")
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"   PostgreSQL: {version[0][:60]}...")
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"   Tables: {[t[0] for t in tables] if tables else 'None'}")
        
        cur.close()
        conn.close()
        
        print(f"\n{'='*70}")
        print("✅ IPv6 CONNECTION WORKS!")
        print(f"{'='*70}")
        print("\nHowever, using IP addresses directly is NOT recommended because:")
        print("- The IP can change when Supabase restarts/migrates")
        print("- SSL certificate validation will fail")
        print("\nBetter solution: Fix IPv6 support in your network/application")
        print(f"{'='*70}")
        break
        
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}\n")

print("\n" + "="*70)
print("RECOMMENDED SOLUTIONS:")
print("="*70)
print("\n1. Enable IPv6 on your network adapter:")
print("   - Open Network Connections")
print("   - Right-click your network adapter → Properties")
print("   - Check 'Internet Protocol Version 6 (TCP/IPv6)'")
print("\n2. Use Supabase IPv4 Add-on (paid feature)")
print("\n3. Use a local PostgreSQL database for development")
print("\n4. Use Cloudflare Warp or similar IPv6 tunnel")
print("="*70)
