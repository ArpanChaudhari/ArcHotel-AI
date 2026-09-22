from app.db.connection import get_connection
from app.db.schema import create_tables
from app.db.data import HOTELS_DATA, ROOM_TYPES


def seed_database():
    """Insert sample hotels and their room types safely."""

    with get_connection() as conn:

        conn.executemany(
            """
            INSERT OR IGNORE INTO hotels
            (
                name, city, price_per_night, stars,
                distance_to_center, amenities, rating
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            HOTELS_DATA,
        )

        hotels = conn.execute("SELECT id FROM hotels").fetchall()

        for hotel in hotels:
            for room_type, multiplier in ROOM_TYPES:

                conn.execute(
                    """
                    INSERT OR IGNORE INTO rooms
                    (
                        hotel_id, room_type,
                        price_multiplier, available_rooms
                    )
                    VALUES (?, ?, ?, ?)
                """,
                    (hotel["id"], room_type, multiplier, 10),
                )


def initialize_database():
    """Create tables and insert initial sample data."""

    create_tables()
    seed_database()
