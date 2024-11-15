from aws_config import get_rds_connection

def get_movies():
    connection = get_rds_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT movie_id, title, description, poster_url FROM movies;")
    movies = cursor.fetchall()
    cursor.close()
    connection.close()
    return movies

def book_ticket(user_id, movie_id, seat_number):
    connection = get_rds_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO bookings (user_id, movie_id, seat_number, payment_status) VALUES (%s, %s, %s, %s)",
        (user_id, movie_id, seat_number, 'Pending')
    )
    connection.commit()
    cursor.close()
    connection.close()
