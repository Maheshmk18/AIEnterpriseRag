"""
Database initialization script for Supabase PostgreSQL
This script creates all necessary tables and seeds the default admin user.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.database.connection import engine, SessionLocal, Base
from app.database.models import User, Document, ChatSession, ChatMessage
from app.core.security import get_password_hash

def init_database():
    """Initialize the database with all tables and seed data"""
    
    print("🔄 Starting database initialization...")
    
    # Verify DATABASE_URL is set
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable is not set!")
        print("Please check your .env file.")
        return False
    
    # Mask password in URL for display
    display_url = database_url.split('@')[1] if '@' in database_url else database_url
    print(f"📊 Connecting to database: {display_url}")
    
    try:
        # Create all tables
        print("📝 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {', '.join(tables)}")
        
        # Seed default admin user
        print("\n👤 Seeding default admin user...")
        db = SessionLocal()
        try:
            # Check if any users exist
            user_count = db.query(User).count()
            
            if user_count == 0:
                admin_user = User(
                    username="admin",
                    email="admin@enterprise.com",
                    hashed_password=get_password_hash("admin123"),
                    full_name="System Administrator",
                    role="admin",
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                print("✅ Default admin user created successfully!")
                print("   Username: admin")
                print("   Password: admin123")
                print("   Email: admin@enterprise.com")
            else:
                print(f"ℹ️  Database already has {user_count} user(s). Skipping admin creation.")
                
        except Exception as e:
            print(f"❌ Error seeding admin user: {e}")
            db.rollback()
            return False
        finally:
            db.close()
        
        print("\n✅ Database initialization completed successfully!")
        print("🚀 You can now start your application.")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)
