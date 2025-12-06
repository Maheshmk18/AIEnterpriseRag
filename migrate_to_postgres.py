import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# SQLite connection
sqlite_db = "sql_app.db"

# PostgreSQL connection
pg_config = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "mahesh",
    "database": "enterprise_rag"
}

print("=" * 60)
print("MIGRATING DATA FROM SQLite TO PostgreSQL")
print("=" * 60)

try:
    # Connect to SQLite
    print("\n1. Connecting to SQLite...")
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    print("2. Connecting to PostgreSQL...")
    pg_conn = psycopg2.connect(**pg_config)
    pg_cur = pg_conn.cursor()
    
    # Create tables in PostgreSQL
    print("3. Creating tables in PostgreSQL...")
    
    pg_cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            role VARCHAR(50) DEFAULT 'employee',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    
    pg_cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_type VARCHAR(50),
            file_size INTEGER,
            content_hash VARCHAR(64),
            chunk_count INTEGER DEFAULT 0,
            status VARCHAR(50) DEFAULT 'pending',
            owner_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    
    pg_cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            user_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    
    pg_cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            session_id INTEGER REFERENCES chat_sessions(id),
            role VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    pg_conn.commit()
    print("   ✓ Tables created successfully")
    
    # Migrate Users
    print("\n4. Migrating users...")
    sqlite_cur.execute("SELECT * FROM users")
    users = sqlite_cur.fetchall()
    
    if users:
        user_data = []
        for user in users:
            user_data.append((
                user['username'],
                user['email'],
                user['hashed_password'],
                user['full_name'],
                bool(user['is_active']),
                user.get('role', 'employee'),
                user.get('created_at'),
                user.get('updated_at')
            ))
        
        execute_values(pg_cur, """
            INSERT INTO users (username, email, hashed_password, full_name, is_active, role, created_at, updated_at)
            VALUES %s
            ON CONFLICT (username) DO NOTHING
        """, user_data)
        pg_conn.commit()
        print(f"   ✓ Migrated {len(users)} users")
    else:
        print("   - No users to migrate")
    
    # Migrate Documents
    print("\n5. Migrating documents...")
    sqlite_cur.execute("SELECT * FROM documents")
    documents = sqlite_cur.fetchall()
    
    if documents:
        doc_data = []
        for doc in documents:
            doc_data.append((
                doc['filename'],
                doc['original_filename'],
                doc['file_type'],
                doc['file_size'],
                doc.get('content_hash'),
                doc.get('chunk_count', 0),
                doc.get('status', 'pending'),
                doc['owner_id'],
                doc.get('created_at'),
                doc.get('updated_at')
            ))
        
        execute_values(pg_cur, """
            INSERT INTO documents (filename, original_filename, file_type, file_size, content_hash, 
                                 chunk_count, status, owner_id, created_at, updated_at)
            VALUES %s
        """, doc_data)
        pg_conn.commit()
        print(f"   ✓ Migrated {len(documents)} documents")
    else:
        print("   - No documents to migrate")
    
    # Migrate Chat Sessions
    print("\n6. Migrating chat sessions...")
    sqlite_cur.execute("SELECT * FROM chat_sessions")
    sessions = sqlite_cur.fetchall()
    
    if sessions:
        session_data = []
        for session in sessions:
            session_data.append((
                session['title'],
                session['user_id'],
                session.get('created_at'),
                session.get('updated_at')
            ))
        
        execute_values(pg_cur, """
            INSERT INTO chat_sessions (title, user_id, created_at, updated_at)
            VALUES %s
        """, session_data)
        pg_conn.commit()
        print(f"   ✓ Migrated {len(sessions)} chat sessions")
    else:
        print("   - No chat sessions to migrate")
    
    # Migrate Chat Messages
    print("\n7. Migrating chat messages...")
    sqlite_cur.execute("SELECT * FROM chat_messages")
    messages = sqlite_cur.fetchall()
    
    if messages:
        message_data = []
        for msg in messages:
            message_data.append((
                msg['session_id'],
                msg['role'],
                msg['content'],
                msg.get('created_at')
            ))
        
        execute_values(pg_cur, """
            INSERT INTO chat_messages (session_id, role, content, created_at)
            VALUES %s
        """, message_data)
        pg_conn.commit()
        print(f"   ✓ Migrated {len(messages)} chat messages")
    else:
        print("   - No chat messages to migrate")
    
    # Verify migration
    print("\n8. Verifying migration...")
    pg_cur.execute("SELECT COUNT(*) FROM users")
    user_count = pg_cur.fetchone()[0]
    pg_cur.execute("SELECT COUNT(*) FROM documents")
    doc_count = pg_cur.fetchone()[0]
    pg_cur.execute("SELECT COUNT(*) FROM chat_sessions")
    session_count = pg_cur.fetchone()[0]
    pg_cur.execute("SELECT COUNT(*) FROM chat_messages")
    message_count = pg_cur.fetchone()[0]
    
    print(f"   ✓ Users: {user_count}")
    print(f"   ✓ Documents: {doc_count}")
    print(f"   ✓ Chat Sessions: {session_count}")
    print(f"   ✓ Chat Messages: {message_count}")
    
    print("\n" + "=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nYour data is now in PostgreSQL!")
    print("Restart the backend to use PostgreSQL.")
    
except sqlite3.Error as e:
    print(f"SQLite Error: {e}")
except psycopg2.Error as e:
    print(f"PostgreSQL Error: {e}")
finally:
    if 'sqlite_conn' in locals():
        sqlite_conn.close()
    if 'pg_conn' in locals():
        pg_conn.close()
