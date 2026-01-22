CUSTOMERS_TABLE = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
);
"""

BOOKINGS_TABLE = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    booking_type TEXT,
    date TEXT,
    time TEXT,
    status TEXT,
    created_at TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
"""
