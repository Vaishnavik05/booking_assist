import streamlit as st
import pandas as pd
from db.database import get_all_bookings

def render_admin():
    st.title("Fixdent Admin Dashboard")

    bookings = get_all_bookings()

    if not bookings:
        st.info("No dental appointments found.")
        return

    df = pd.DataFrame(bookings, columns=[
        "Booking ID",
        "Customer Name",
        "Email",
        "Phone",
        "Type",
        "Date",
        "Time",
        "Status",
        "Created At"
    ])

    st.subheader("All Dental Appointments")

    search = st.text_input("Search by name or email")

    if search:
        df = df[
            df["Customer Name"].str.contains(search, case=False) |
            df["Email"].str.contains(search, case=False)
        ]

    st.dataframe(df, width="stretch")
