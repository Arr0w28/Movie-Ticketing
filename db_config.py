def create_tables():
    connection = get_rds_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        email VARCHAR(255) UNIQUE,
        password_hash VARCHAR(255)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        poster_url TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        movie_id INTEGER REFERENCES movies(movie_id),
        seat_number VARCHAR(5),
        payment_status VARCHAR(50),
        booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
