import sqlite3
import random
import string
from datetime import datetime
from app.db.connection import get_connection, DB_PATH


def calculate_nights(checkin, checkout):
    checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
    checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
    return (checkout_date - checkin_date).days


def search_hotels(
    city,
    max_price=None,
    required_amenities=None,
    min_stars=None,
    checkin=None,
    checkout=None,
):
    print(f"DATABASE TOOL CALLED: Searching hotels in {city}", flush=True)

    nights = 1
    if checkin and checkout:
        try:
            nights = max(1, calculate_nights(checkin, checkout))
        except:
            nights = 1

    max_price_per_night = max_price / nights if max_price else None

    with get_connection() as conn:
        query = "SELECT * FROM hotels WHERE LOWER(city) = ?"
        params = [city.lower()]

        if min_stars:
            query += " AND stars >= ?"
            params.append(min_stars)

        results = conn.execute(query, params).fetchall()

    filtered_results = []
    for hotel in results:
        price_per_night = hotel["price_per_night"]

        if max_price_per_night and price_per_night > max_price_per_night:
            continue

        if required_amenities:
            hotel_amenities = hotel["amenities"].lower().split(",")
            if not all(a.lower() in hotel_amenities for a in required_amenities):
                continue

        total_price = price_per_night * nights
        filtered_results.append((hotel, total_price))

    filtered_results.sort(key=lambda x: x[0]["rating"], reverse=True)

    if not filtered_results:
        return f"No matching hotels found in {city} for {nights} night(s) within a total budget of ₹{max_price}."

    response = f"Top matching hotels in {city} for {nights} night(s):\n"
    for hotel, total_price in filtered_results[:3]:
        response += (
            f"{hotel['name']} | ₹{hotel['price_per_night']}/night | Total: ₹{total_price:.2f} | "
            f"{hotel['stars']}⭐ | Rating {hotel['rating']}\n"
        )
    return response


def get_hotel_details(hotel_name):
    print(f"DATABASE TOOL CALLED: Getting details for {hotel_name}", flush=True)
    with get_connection() as conn:
        hotel = conn.execute(
            "SELECT * FROM hotels WHERE name = ?", (hotel_name,)
        ).fetchone()
        if not hotel:
            return "Hotel not found."

        rooms = conn.execute(
            "SELECT room_type, price_multiplier, available_rooms FROM rooms WHERE hotel_id = ?",
            (hotel["id"],),
        ).fetchall()

    response = f"{hotel['name']} Details:\n"
    response += f"{hotel['stars']}⭐ | Rating {hotel['rating']} | ₹{hotel['price_per_night']}/night base price\n"
    response += f"Amenities: {hotel['amenities']}\nRooms:\n"

    for room in rooms:
        final_price = hotel["price_per_night"] * room["price_multiplier"]
        response += f"{room['room_type']} - ₹{final_price:.2f} per night ({room['available_rooms']} available)\n"
    return response


def reserve_room(hotel_name, room_type, guest_name, checkin, checkout):
    print(f"DATABASE TOOL CALLED: Reserving room at {hotel_name}", flush=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        hotel = conn.execute(
            "SELECT * FROM hotels WHERE name = ?", (hotel_name,)
        ).fetchone()

        if not hotel:
            return "Hotel not found."

        room = conn.execute(
            "SELECT price_multiplier, available_rooms FROM rooms WHERE hotel_id = ? AND room_type = ?",
            (hotel["id"], room_type),
        ).fetchone()

        if not room or room["available_rooms"] <= 0:
            return "Room type unavailable."

        nights = max(1, calculate_nights(checkin, checkout))
        total_price = hotel["price_per_night"] * room["price_multiplier"] * nights
        confirmation_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )

        conn.execute(
            """
            INSERT INTO reservations (hotel_id, room_type, guest_name, checkin, checkout, total_price, confirmation_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                hotel["id"],
                room_type,
                guest_name,
                checkin,
                checkout,
                total_price,
                confirmation_code,
            ),
        )

        conn.execute(
            """
            UPDATE rooms SET available_rooms = available_rooms - 1
            WHERE hotel_id = ? AND room_type = ?
        """,
            (hotel["id"], room_type),
        )

    return f"Reservation confirmed at {hotel_name}. Total: ₹{total_price:.2f}. Confirmation: {confirmation_code}"
