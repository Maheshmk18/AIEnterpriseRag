from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sql_app.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
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
