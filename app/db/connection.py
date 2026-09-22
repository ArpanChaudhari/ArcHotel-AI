import sqlite3
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database file location
DB_PATH = BASE_DIR / "arc_hotels.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign key validation
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
