import psycopg2
from utils.database import get_db_connection

def sign_up_user(user_name, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_name, password) VALUES (%s, %s)", (user_name, password))
    conn.commit()
    conn.close()

def login_user(user_name, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_name = %s AND password = %s", (user_name, password))
    user = cursor.fetchone()
    conn.close()
    return user
