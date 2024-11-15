-- schema.sql

-- Drop existing tables and trigger function (if they exist)
DROP TRIGGER IF EXISTS update_bookings_updated_at ON bookings;
DROP TRIGGER IF EXISTS update_seats_updated_at ON seats;
DROP TRIGGER IF EXISTS update_shows_updated_at ON shows;
DROP TRIGGER IF EXISTS update_movies_updated_at ON movies;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS seats;
DROP TABLE IF EXISTS shows;
DROP TABLE IF EXISTS movies;

-- Create movies table
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration INTEGER,
    language VARCHAR(50),
    release_date DATE,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create shows table
CREATE TABLE shows (
    show_id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(movie_id),
    show_date DATE,
    show_timing TIME,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create seats table
CREATE TABLE seats (
    seat_id SERIAL PRIMARY KEY,
    show_id INTEGER REFERENCES shows(show_id),
    seat_number VARCHAR(10),
    booking_status VARCHAR(20) DEFAULT 'available',
    booking_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(show_id, seat_number)
);

-- Create bookings table
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    show_id INTEGER REFERENCES shows(show_id),
    booking_date TIMESTAMP,
    total_amount DECIMAL(10,2),
    booking_status VARCHAR(20) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
CREATE TRIGGER update_movies_updated_at
    BEFORE UPDATE ON movies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_shows_updated_at
    BEFORE UPDATE ON shows
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_seats_updated_at
    BEFORE UPDATE ON seats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at
    BEFORE UPDATE ON bookings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample movies
INSERT INTO movies (title, description, duration, language, release_date) 
VALUES 
    ('Inception', 'A thief who steals corporate secrets through dream-sharing technology', 148, 'English', '2010-07-16'),
    ('The Dark Knight', 'Batman fights crime in Gotham City', 152, 'English', '2008-07-18'),
    ('Interstellar', 'Astronauts travel through a wormhole in search of a new home', 169, 'English', '2014-11-07');

-- Insert sample shows
INSERT INTO shows (movie_id, show_date, show_timing, price)
VALUES 
    (1, CURRENT_DATE, '14:00', 12.99),
    (1, CURRENT_DATE, '18:00', 14.99),
    (2, CURRENT_DATE, '15:00', 12.99),
    (2, CURRENT_DATE, '19:00', 14.99),
    (3, CURRENT_DATE, '16:00', 12.99),
    (3, CURRENT_DATE, '20:00', 14.99);