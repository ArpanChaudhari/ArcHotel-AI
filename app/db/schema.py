from app.db.connection import get_connection


def create_tables():
    """Create all database tables if they don't exist."""

    with get_connection() as conn:

        # HOTELS
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL,
                price_per_night REAL NOT NULL CHECK(price_per_night > 0),
                stars INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                distance_to_center REAL NOT NULL CHECK(distance_to_center >= 0),
                amenities TEXT NOT NULL DEFAULT '',
                rating REAL NOT NULL CHECK(rating BETWEEN 0 AND 5)
            )
        """)

        # ROOMS
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hotel_id INTEGER NOT NULL,
                room_type TEXT NOT NULL,
                price_multiplier REAL NOT NULL
                    CHECK(price_multiplier > 0),
                available_rooms INTEGER NOT NULL
                    CHECK(available_rooms >= 0),

                FOREIGN KEY (hotel_id)
                    REFERENCES hotels(id)
                    ON DELETE CASCADE,

                UNIQUE(hotel_id, room_type)
            )
        """)

        # BOOKINGS
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hotel_id INTEGER NOT NULL,
                room_type TEXT NOT NULL,
                guest_name TEXT NOT NULL,
                checkin TEXT NOT NULL,
                checkout TEXT NOT NULL,
                total_price REAL NOT NULL
                    CHECK(total_price > 0),
                confirmation_code TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'confirmed'
                    CHECK(status IN ('confirmed', 'cancelled')),

                FOREIGN KEY (hotel_id)
                    REFERENCES hotels(id)
            )
        """)
