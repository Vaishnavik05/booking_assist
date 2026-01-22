import sqlite3
from datetime import datetime
from app.config import DB_PATH
from db.models import CUSTOMERS_TABLE, BOOKINGS_TABLE

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CUSTOMERS_TABLE)
    cursor.execute(BOOKINGS_TABLE)
    conn.commit()
    conn.close()

def insert_customer(name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )
    conn.commit()
    customer_id = cursor.lastrowid
    conn.close()
    return customer_id

def insert_booking(customer_id, booking_type, date, time, status="confirmed"):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO bookings (customer_id, booking_type, date, time, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (customer_id, booking_type, date, time, status, created_at)
    )
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    return booking_id

def update_booking_time(email, new_date, new_time):
    conn = get_connection()
    cur = conn.cursor()
    # Find the most recent booking for this email to reschedule
    cur.execute("""
        SELECT b.id
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        WHERE c.email = ?
        ORDER BY b.created_at DESC
        LIMIT 1
    """, (email,))
    
    row = cur.fetchone()
    if row:
        booking_id = row[0]
        cur.execute("""
            UPDATE bookings
            SET date = ?, time = ?, status = 'confirmed'
            WHERE id = ?
        """, (new_date, new_time, booking_id))
        conn.commit()
        updated = cur.rowcount
    else:
        updated = 0
    conn.close()
    return updated > 0

def delete_booking_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM bookings
        WHERE customer_id = (SELECT customer_id FROM customers WHERE email = ?)
    """, (email,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0

def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            b.id,
            c.name,
            c.email,
            c.phone,
            b.booking_type,
            b.date,
            b.time,
            b.status,
            b.created_at
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        ORDER BY b.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows