import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database='chef_agent',
    user="postgres",
    password="kuldip@311",
    port=5432   
)

cursor = conn.cursor()


def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        role TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        recipe TEXT,
        rating INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    

    conn.commit()
    
def save_message(user_id, role, message):

    cursor.execute(
        "INSERT INTO conversations (user_id, role, message) VALUES (%s,%s,%s)",
        (user_id, role, message)
    )

    conn.commit()

def get_last_messages(conn, user_id):

    query = """
    SELECT role, content
    FROM messages
    WHERE user_id = %s
    ORDER BY id DESC
    LIMIT 5
    """

    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    rows.reverse()  # maintain chat order

    return [
        {"role": r[0], "content": r[1]}
        for r in rows
    ]

        