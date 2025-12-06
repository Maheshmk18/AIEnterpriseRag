"""
Migration script to remove department column from users and documents tables
Run this script to update your existing database schema
"""
import sqlite3
import os

def migrate_database():
    db_path = "backend/sql_app.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting migration...")
        
        # Check if department column exists in users table
        cursor.execute("PRAGMA table_info(users)")
        users_columns = [col[1] for col in cursor.fetchall()]
        
        if 'department' in users_columns:
            print("Removing department column from users table...")
            
            # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
            # First, create a new table without the department column
            cursor.execute("""
                CREATE TABLE users_new (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    is_active BOOLEAN DEFAULT 1,
                    role VARCHAR(50) DEFAULT 'employee',
                    phone VARCHAR(20),
                    profile_photo TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME
                )
            """)
            
            # Copy data from old table to new table (excluding department)
            cursor.execute("""
                INSERT INTO users_new (id, username, email, hashed_password, full_name, 
                                      is_active, role, phone, profile_photo, created_at, updated_at)
                SELECT id, username, email, hashed_password, full_name, 
                       is_active, role, phone, profile_photo, created_at, updated_at
                FROM users
            """)
            
            # Drop old table and rename new table
            cursor.execute("DROP TABLE users")
            cursor.execute("ALTER TABLE users_new RENAME TO users")
            
            # Recreate indexes
            cursor.execute("CREATE UNIQUE INDEX ix_users_username ON users (username)")
            cursor.execute("CREATE UNIQUE INDEX ix_users_email ON users (email)")
            cursor.execute("CREATE INDEX ix_users_id ON users (id)")
            
            print("✓ Removed department column from users table")
        else:
            print("✓ Department column not found in users table (already migrated)")
        
        # Check if department column exists in documents table
        cursor.execute("PRAGMA table_info(documents)")
        docs_columns = [col[1] for col in cursor.fetchall()]
        
        if 'department' in docs_columns:
            print("Removing department column from documents table...")
            
            # Create new documents table without department
            cursor.execute("""
                CREATE TABLE documents_new (
                    id INTEGER PRIMARY KEY,
                    filename VARCHAR(255),
                    original_filename VARCHAR(255),
                    file_type VARCHAR(50),
                    file_size INTEGER,
                    content_hash VARCHAR(64),
                    chunk_count INTEGER DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'pending',
                    owner_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME,
                    FOREIGN KEY (owner_id) REFERENCES users (id)
                )
            """)
            
            # Copy data from old table to new table (excluding department)
            cursor.execute("""
                INSERT INTO documents_new (id, filename, original_filename, file_type, 
                                          file_size, content_hash, chunk_count, status, 
                                          owner_id, created_at, updated_at)
                SELECT id, filename, original_filename, file_type, 
                       file_size, content_hash, chunk_count, status, 
                       owner_id, created_at, updated_at
                FROM documents
            """)
            
            # Drop old table and rename new table
            cursor.execute("DROP TABLE documents")
            cursor.execute("ALTER TABLE documents_new RENAME TO documents")
            
            # Recreate indexes
            cursor.execute("CREATE INDEX ix_documents_id ON documents (id)")
            
            print("✓ Removed department column from documents table")
        else:
            print("✓ Department column not found in documents table (already migrated)")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
