from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

import sys

# Get DATABASE_URL, strictly enforce it (no SQLite fallback)
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL environment variable is not set.")
    print("Please set it to your PostgreSQL connection string.")
    print("Example: postgresql://user:password@localhost:5432/dbname")
    # For now, we raise an error so valid deployment fails if env var missing
    # In production config, this is good.
    sys.exit(1)

# Fix for Render providing 'postgres://' instead of 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure engine with SSL and connection pooling for Neon
connect_args = {}
if "neon.tech" in DATABASE_URL:
    # Neon-specific SSL configuration
    connect_args = {
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=300,     # Recycle connections every 5 minutes
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    from . import models
    from ..core.security import get_password_hash
    
    Base.metadata.create_all(bind=engine)
    
    # Seed default admin
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            admin_user = models.User(
                username="admin",
                email="admin@enterprise.com",
                hashed_password=get_password_hash("admin123"),
                full_name="System Admin",
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created: admin / admin123")
    except Exception as e:
        print(f"Error seeding admin user: {e}")
    finally:
        db.close()
