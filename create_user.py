import psycopg2
import bcrypt

conn = psycopg2.connect('postgresql://postgres:mahesh@localhost:5432/enterprise_rag')
cur = conn.cursor()

# List existing users
cur.execute('SELECT id, username, full_name, role, department, is_active FROM users')
print("Existing users:")
for r in cur.fetchall():
    print(f"  {r}")

# Create test employee user using bcrypt
password = 'test123'
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

try:
    cur.execute("""
        INSERT INTO users (username, email, hashed_password, full_name, role, department, is_active) 
        VALUES ('employee1', 'employee1@test.com', %s, 'John Employee', 'employee', 'hr', true) 
        ON CONFLICT (username) DO NOTHING
    """, (password_hash,))
    conn.commit()
    print("\nCreated employee1 user with password 'test123'")
except Exception as e:
    print(f"Error: {e}")

cur.execute('SELECT id, username, full_name, role, department, is_active FROM users')
print("\nUpdated users list:")
for r in cur.fetchall():
    print(f"  {r}")
    
conn.close()
