import streamlit as st
import psycopg2
from utils.database import get_db_connection

# Set Streamlit page config
st.set_page_config(page_title="Movie Ticket Booking", layout="centered")

# Title
st.title("Welcome to the Movie Ticket Booking System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose Option", ["Home", "Book Ticket", "My Bookings"])

# Database connection
conn = get_db_connection()

if page == "Home":
    st.header("Available Movies")
    # Fetch available movies from the database
    cursor = conn.cursor()
    cursor.execute("SELECT title, genre, release_date FROM movies")
    movies = cursor.fetchall()
    for movie in movies:
        st.write(f"{movie[0]} - {movie[1]} - {movie[2]}")

elif page == "Book Ticket":
    st.header("Book a Movie Ticket")
    movie_choices = [movie[0] for movie in conn.cursor().execute("SELECT title FROM movies").fetchall()]
    selected_movie = st.selectbox("Choose a movie", movie_choices)

    if st.button("Book Ticket"):
        user_name = st.text_input("Enter your name")
        if user_name:
            # Insert ticket booking into the database
            cursor.execute("INSERT INTO bookings (movie_title, user_name) VALUES (%s, %s)", (selected_movie, user_name))
            conn.commit()
            st.success(f"Ticket booked for {selected_movie}!")

elif page == "My Bookings":
    st.header("Your Bookings")
    user_name = st.text_input("Enter your name to view bookings")
    if user_name:
        cursor.execute("SELECT movie_title FROM bookings WHERE user_name = %s", (user_name,))
        bookings = cursor.fetchall()
        if bookings:
            st.write("Your Bookings:")
            for booking in bookings:
                st.write(f"- {booking[0]}")
        else:
            st.write("No bookings found.")

# Close the connection
conn.close()
