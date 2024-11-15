-- Example Table Creation
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(50),
    duration INTEGER,
    release_date DATE
);

CREATE TABLE cinemas (
    cinema_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(movie_id),
    cinema_id INTEGER REFERENCES cinemas(cinema_id),
    seat_number VARCHAR(10),
    show_time TIMESTAMP,
    price NUMERIC(10, 2)
);
