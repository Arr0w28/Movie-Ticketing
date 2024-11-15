-- Function to check if tables exist
DO $$ 
BEGIN
    -- Check if tables exist
    PERFORM FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'movies';
    
    IF NOT FOUND THEN
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
        
        RAISE NOTICE 'Created movies table';
    END IF;

    PERFORM FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'shows';
    
    IF NOT FOUND THEN
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
        
        RAISE NOTICE 'Created shows table';
    END IF;

    PERFORM FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'seats';
    
    IF NOT FOUND THEN
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
        
        RAISE NOTICE 'Created seats table';
    END IF;

    PERFORM FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'bookings';
    
    IF NOT FOUND THEN
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
        
        RAISE NOTICE 'Created bookings table';
    END IF;

    -- Check if trigger function exists
    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'update_updated_at_column') THEN
        CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        RAISE NOTICE 'Created trigger function';
    END IF;

    -- Create triggers if they don't exist
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_movies_updated_at') THEN
        CREATE TRIGGER update_movies_updated_at
            BEFORE UPDATE ON movies
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            
        RAISE NOTICE 'Created movies trigger';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_shows_updated_at') THEN
        CREATE TRIGGER update_shows_updated_at
            BEFORE UPDATE ON shows
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            
        RAISE NOTICE 'Created shows trigger';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_seats_updated_at') THEN
        CREATE TRIGGER update_seats_updated_at
            BEFORE UPDATE ON seats
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            
        RAISE NOTICE 'Created seats trigger';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_bookings_updated_at') THEN
        CREATE TRIGGER update_bookings_updated_at
            BEFORE UPDATE ON bookings
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            
        RAISE NOTICE 'Created bookings trigger';
    END IF;

END $$;

-- Add some indexes for better performanc
CREATE INDEX IF NOT EXISTS idx_shows_movie_id ON shows(movie_id);
CREATE INDEX IF NOT EXISTS idx_seats_show_id ON seats(show_id);
CREATE INDEX IF NOT EXISTS idx_bookings_show_id ON bookings(show_id);
CREATE INDEX IF NOT EXISTS idx_bookings_user_id ON bookings(user_id);