import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
from rag_pipeline import rag_query
from db.database import insert_customer, insert_booking
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, GEMINI_API_KEY
import streamlit as st
genai.configure(api_key=GEMINI_API_KEY)

def gemini_chat(prompt):
    models = genai.list_models()
    model_name = None
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            model_name = m.name
            break

    if not model_name:
        return "No supported Gemini model found."

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text


def rag_tool(query):
    return rag_query(query)

def booking_persistence_tool(data):
    customer_id = insert_customer(data["name"], data["email"], data["phone"])
    booking_id = insert_booking(customer_id, data["booking_type"], data["date"], data["time"])
    return booking_id

def email_tool(receiver_email, subject, body):
    # Pull credentials from the secrets file
    smtp_server = st.secrets["EMAIL_HOST"]
    smtp_port = st.secrets["EMAIL_PORT"]
    smtp_user = st.secrets["EMAIL_USER"]
    smtp_pass = st.secrets["EMAIL_PASSWORD"]

    # Create the email content
    msg = MIMEText(body)
    msg["Subject"] = subject
    # You can name this whatever you want
    msg["From"] = f"Fixdent AI <noreply@fixdent.com>" 
    msg["To"] = receiver_email

    try:
        # Connect to Mailtrap Sandbox
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Secure the connection
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Mailtrap Error: {e}")
        return False