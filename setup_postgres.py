import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
HOST = "localhost"
PORT = "5432"
USER = "postgres"
PASSWORD = input("Enter PostgreSQL password: ")
DATABASE = "enterprise_rag"

print(f"Connecting to PostgreSQL at {HOST}:{PORT}...")

try:
    # Connect to default postgres database to create our database
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DATABASE,))
    exists = cursor.fetchone()
    
    if exists:
        print(f"Database '{DATABASE}' already exists!")
    else:
        # Create database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(DATABASE)
        ))
        print(f"Database '{DATABASE}' created successfully!")
    
    cursor.close()
    conn.close()
    
    # Test connection to new database
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    print(f"Successfully connected to '{DATABASE}'!")
    conn.close()
    
    # Create .env entry
    db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    print(f"\nAdd this to your backend/.env file:")
    print(f"DATABASE_URL={db_url}")
    
except psycopg2.Error as e:
    print(f"Error: {e}")
