import os
import sys
from sqlalchemy import create_engine, text
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Get DB URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ Error: DATABASE_URL not found in .env")
    sys.exit(1)

# Fix pooler URL for stability if needed, though pooler is fine for this script
if "pooler" in DATABASE_URL:
    print("ℹ️  Using pooler connection string...")

print(f"🔌 Connecting to database...")

try:
    # Setup password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Generate new hash for 'admin123'
    password_to_set = "admin123"
    hashed_password = pwd_context.hash(password_to_set)
    print(f"🔑 Generated new hash for '{password_to_set}'")

    # Connect to DB
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Check if user exists
        result = connection.execute(text("SELECT username FROM users WHERE username = 'admin'"))
        user = result.fetchone()
        
        if user:
            # Update existing user
            print("👤 User 'admin' found. Updating password...")
            connection.execute(
                text("UPDATE users SET hashed_password = :pwd WHERE username = 'admin'"),
                {"pwd": hashed_password}
            )
            print("✅ Password updated successfully!")
        else:
            # Create user if missing
            print("⚠️  User 'admin' not found. Creating new user...")
            connection.execute(
                text("""
                    INSERT INTO users (username, email, hashed_password, full_name, role, is_active, created_at)
                    VALUES ('admin', 'admin@enterprise.com', :pwd, 'System Admin', 'admin', true, NOW())
                """),
                {"pwd": hashed_password}
            )
            print("✅ New admin user created successfully!")
            
        connection.commit()
        print("🎉 Done! You can now login with 'admin' / 'admin123'")

except Exception as e:
    print(f"❌ Error: {e}")
