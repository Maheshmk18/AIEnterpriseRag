import psycopg2
from psycopg2.extras import RealDictCursor

# PostgreSQL connection
pg_config = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "mahesh",
    "database": "enterprise_rag"
}

def view_data():
    """View all data in PostgreSQL database"""
    
    try:
        conn = psycopg2.connect(**pg_config, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        
        print("\n" + "=" * 80)
        print("ENTERPRISE RAG - PostgreSQL DATABASE")
        print("=" * 80)
        
        # Users
        print("\n📊 USERS")
        print("-" * 80)
        cur.execute("""
            SELECT id, username, email, full_name, role, is_active, created_at 
            FROM users 
            ORDER BY id
        """)
        users = cur.fetchall()
        
        if users:
            print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Role':<10} {'Active':<8} {'Created'}")
            print("-" * 80)
            for user in users:
                print(f"{user['id']:<5} {user['username']:<15} {user['email']:<25} "
                      f"{user['role']:<10} {str(user['is_active']):<8} {user['created_at']}")
        else:
            print("No users found")
        
        # Documents
        print("\n📄 DOCUMENTS")
        print("-" * 80)
        cur.execute("""
            SELECT id, original_filename, file_type, chunk_count, status, owner_id, created_at 
            FROM documents 
            ORDER BY id
        """)
        documents = cur.fetchall()
        
        if documents:
            print(f"{'ID':<5} {'Filename':<30} {'Type':<8} {'Chunks':<8} {'Status':<12} {'Owner':<7}")
            print("-" * 80)
            for doc in documents:
                print(f"{doc['id']:<5} {doc['original_filename']:<30} {doc['file_type']:<8} "
                      f"{doc['chunk_count']:<8} {doc['status']:<12} {doc['owner_id']:<7}")
        else:
            print("No documents found")
        
        # Chat Sessions
        print("\n💬 CHAT SESSIONS")
        print("-" * 80)
        cur.execute("""
            SELECT cs.id, cs.title, cs.user_id, u.username, cs.created_at,
                   (SELECT COUNT(*) FROM chat_messages WHERE session_id = cs.id) as message_count
            FROM chat_sessions cs
            LEFT JOIN users u ON cs.user_id = u.id
            ORDER BY cs.id DESC
            LIMIT 10
        """)
        sessions = cur.fetchall()
        
        if sessions:
            print(f"{'ID':<5} {'Title':<30} {'User':<15} {'Messages':<10} {'Created'}")
            print("-" * 80)
            for session in sessions:
                print(f"{session['id']:<5} {session['title']:<30} {session['username']:<15} "
                      f"{session['message_count']:<10} {session['created_at']}")
        else:
            print("No chat sessions found")
        
        # Summary
        print("\n📈 SUMMARY")
        print("-" * 80)
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()['count']
        cur.execute("SELECT COUNT(*) FROM documents")
        doc_count = cur.fetchone()['count']
        cur.execute("SELECT COUNT(*) FROM chat_sessions")
        session_count = cur.fetchone()['count']
        cur.execute("SELECT COUNT(*) FROM chat_messages")
        message_count = cur.fetchone()['count']
        
        print(f"Total Users: {user_count}")
        print(f"Total Documents: {doc_count}")
        print(f"Total Chat Sessions: {session_count}")
        print(f"Total Messages: {message_count}")
        
        print("\n" + "=" * 80)
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"PostgreSQL Error: {e}")

if __name__ == "__main__":
    view_data()
