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


        