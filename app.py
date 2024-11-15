import streamlit as st
from datetime import datetime, timedelta
from utils.database import execute_query
import pandas as pd

# Page configuration
st.set_page_config(page_title="Movie Ticket Booking System", page_icon="🎬", layout="wide")

def get_movies():
    """Fetch all available movies"""
    query = """
    SELECT DISTINCT m.movie_id, m.title, m.description, m.release_date, 
           m.duration, m.language, m.image_url, s.show_timing
    FROM movies m
    LEFT JOIN shows s ON m.movie_id = s.movie_id
    WHERE s.show_date = CURRENT_DATE
    """
    return execute_query(query)

def get_available_seats(show_id):
    """Get available seats for a show"""
    query = """
    SELECT seat_number 
    FROM seats 
    WHERE show_id = %s AND booking_status = 'available'
    ORDER BY seat_number
    """
    return execute_query(query, (show_id,))

def display_movie_info(movie):
    """Display movie information in a clean format"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if movie['image_url']:
            st.image(movie['image_url'], width=200)
        else:
            st.image("https://via.placeholder.com/200x300?text=No+Image", width=200)
            
    with col2:
        st.subheader(movie['title'])
        st.write(f"**Duration:** {movie['duration']} minutes")
        st.write(f"**Language:** {movie['language']}")
        if movie['description']:
            st.write(f"**Description:** {movie['description']}")
        st.write(f"**Release Date:** {movie['release_date'].strftime('%Y-%m-%d')}")

def create_booking(user_id, show_id, selected_seats, total_price):
    """Create a new booking"""
    try:
        # Insert booking record
        booking_query = """
        INSERT INTO bookings (user_id, show_id, booking_date, total_amount)
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
        RETURNING booking_id
        """
        booking_result = execute_query(
            booking_query, 
            (user_id, show_id, total_price),
            fetch=True
        )
        
        if not booking_result:
            raise Exception("Failed to create booking")
            
        booking_id = booking_result[0]['booking_id']
        
        # Update seats status
        seats_query = """
        UPDATE seats 
        SET booking_status = 'booked', 
            booking_id = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE show_id = %s 
        AND seat_number = ANY(%s)
        AND booking_status = 'available'
        """
        execute_query(
            seats_query, 
            (booking_id, show_id, selected_seats),
            fetch=False
        )
        
        return booking_id
    except Exception as e:
        st.error(f"Booking failed: {str(e)}")
        return None

def main():
    st.title("🎬 Movie Ticket Booking System")
    
    # Initialize session state for booking flow
    if 'booking_stage' not in st.session_state:
        st.session_state.booking_stage = 'movie_selection'
    
    # Fetch movies
    movies = get_movies()
    if not movies:
        st.warning("No movies available for today")
        return
        
    # Convert to DataFrame for easier handling
    movies_df = pd.DataFrame(movies)
    
    # Movie Selection Stage
    if st.session_state.booking_stage == 'movie_selection':
        st.subheader("Available Movies")
        
        for _, movie in movies_df.iterrows():
            st.container()
            display_movie_info(movie)
            
            if st.button(f"Book Now - {movie['title']}", key=f"book_{movie['movie_id']}"):
                st.session_state.selected_movie = movie
                st.session_state.booking_stage = 'show_selection'
                st.experimental_rerun()
                
    # Show Selection Stage
    elif st.session_state.booking_stage == 'show_selection':
        movie = st.session_state.selected_movie
        display_movie_info(movie)
        
        show_query = """
        SELECT show_id, show_timing, price
        FROM shows
        WHERE movie_id = %s AND show_date = CURRENT_DATE
        ORDER BY show_timing
        """
        shows = execute_query(show_query, (movie['movie_id'],))
        
        if shows:
            selected_show = st.selectbox(
                "Select Show Time",
                options=shows,
                format_func=lambda x: f"{x['show_timing'].strftime('%I:%M %p')} - ₹{x['price']}"
            )
            
            if st.button("Select Seats"):
                st.session_state.selected_show = selected_show
                st.session_state.booking_stage = 'seat_selection'
                st.experimental_rerun()
        else:
            st.error("No shows available for this movie today")
            
    # Seat Selection Stage
    elif st.session_state.booking_stage == 'seat_selection':
        show = st.session_state.selected_show
        available_seats = get_available_seats(show['show_id'])
        
        st.subheader("Select Seats")
        selected_seats = st.multiselect(
            "Choose your seats",
            options=[seat['seat_number'] for seat in available_seats]
        )
        
        if selected_seats:
            total_price = len(selected_seats) * show['price']
            st.write(f"Total Price: ₹{total_price}")
            
            if st.button("Confirm Booking"):
                # In production, get user_id from authentication
                user_id = 1  # Placeholder
                booking_id = create_booking(
                    user_id, 
                    show['show_id'],
                    selected_seats,
                    total_price
                )
                
                if booking_id:
                    st.success(f"""
                    Booking Successful!
                    Booking ID: {booking_id}
                    Movie: {st.session_state.selected_movie['title']}
                    Show Time: {show['show_timing'].strftime('%I:%M %p')}
                    Seats: {', '.join(selected_seats)}
                    Total Amount: ₹{total_price}
                    """)
                    # Reset booking flow
                    st.session_state.booking_stage = 'movie_selection'
                    if st.button("Book Another Ticket"):
                        st.experimental_rerun()
                        
    # Back button (except for initial stage)
    if st.session_state.booking_stage != 'movie_selection':
        if st.button("← Back"):
            if st.session_state.booking_stage == 'show_selection':
                st.session_state.booking_stage = 'movie_selection'
            elif st.session_state.booking_stage == 'seat_selection':
                st.session_state.booking_stage = 'show_selection'
            st.experimental_rerun()

if __name__ == "__main__":
    main()