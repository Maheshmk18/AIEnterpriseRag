import psycopg2

pg_config = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "mahesh",
    "database": "enterprise_rag"
}

print("Updating PostgreSQL schema...")

try:
    conn = psycopg2.connect(**pg_config)
    cur = conn.cursor()
    
    # Add new columns to users table
    alter_queries = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS department VARCHAR(50) DEFAULT 'general'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_photo TEXT",
        "ALTER TABLE documents ADD COLUMN IF NOT EXISTS department VARCHAR(50) DEFAULT 'general'",
    ]
    
    for query in alter_queries:
        try:
            cur.execute(query)
            print(f"✓ {query[:50]}...")
        except Exception as e:
            print(f"  Skipped (may already exist): {e}")
    
    conn.commit()
    print("\n✓ Schema updated successfully!")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
