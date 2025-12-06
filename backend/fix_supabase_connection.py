"""
Script to help diagnose and fix Supabase connection issues
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("SUPABASE CONNECTION DIAGNOSTIC TOOL")
print("=" * 70)

# Current connection string
current_url = os.environ.get("DATABASE_URL")
print(f"\n📋 Current DATABASE_URL in .env:")
if current_url:
    # Mask password
    if '@' in current_url:
        user_part, host_part = current_url.split('@')
        user_info = user_part.split('://')[-1]
        if ':' in user_info:
            username = user_info.split(':')[0]
            print(f"   Username: {username}")
            print(f"   Host: {host_part}")
    print(f"   Full (masked): {current_url[:30]}...{current_url[-30:]}")
else:
    print("   ❌ Not set!")

print("\n" + "=" * 70)
print("POSSIBLE SOLUTIONS")
print("=" * 70)

print("\n1️⃣  **Use Connection Pooling (Recommended)**")
print("   Modern Supabase projects use connection pooling.")
print("   Format:")
print("   postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres")
print("\n   Your project reference: cvdoboqcxqqzirawupca")
print("   Your password: #Enterprice123 (needs URL encoding: %23Enterprice123)")

print("\n2️⃣  **Try IPv6 Connection**")
print("   Some networks have issues with IPv4 DNS resolution.")
print("   You might need to use IPv6 or a different DNS server.")

print("\n3️⃣  **Check Project Status**")
print("   - Is your project paused? (Free tier projects pause after inactivity)")
print("   - Is your project deleted?")
print("   - Did Supabase migrate your project to a new URL?")

print("\n4️⃣  **Get Fresh Connection String**")
print("   Steps:")
print("   a. Go to: https://supabase.com/dashboard")
print("   b. Select your project")
print("   c. Settings → Database")
print("   d. Copy the 'Connection Pooling' URI (Transaction mode)")

print("\n" + "=" * 70)
print("TESTING CONNECTION")
print("=" * 70)

# Try to resolve hostname
print("\n🔍 Testing DNS resolution...")
import socket

hostnames_to_test = [
    "db.cvdoboqcxqqzirawupca.supabase.co",
    "aws-0-us-east-1.pooler.supabase.com",
    "aws-0-us-west-1.pooler.supabase.com",
    "aws-0-ap-southeast-1.pooler.supabase.com",
]

for hostname in hostnames_to_test:
    try:
        ip = socket.gethostbyname(hostname)
        print(f"   ✅ {hostname} → {ip}")
    except socket.gaierror:
        print(f"   ❌ {hostname} → Cannot resolve")

print("\n" + "=" * 70)
print("RECOMMENDED ACTION")
print("=" * 70)

print("\n📝 Please do the following:")
print("\n1. Open Supabase Dashboard in your browser")
print("2. Go to your project settings")
print("3. Navigate to Database section")
print("4. Look for 'Connection Pooling' or 'Connection String'")
print("5. Copy the COMPLETE connection string")
print("6. Share it here (I'll help you format it correctly)")
print("\n⚠️  If your project is paused, you'll need to unpause it first!")

print("\n" + "=" * 70)
