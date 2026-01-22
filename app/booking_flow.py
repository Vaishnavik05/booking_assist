import re
from datetime import datetime

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)

def is_valid_date(date_str):
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return False, "Date must be in YYYY-MM-DD format."
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        if input_date < today:
            return False, "Please check your date. We cannot book appointments for the past."
        return True, None
    except ValueError:
        return False, "Invalid date values provided."

def is_valid_time(time_str, selected_date_str=None):
    if not re.match(r"^\d{2}:\d{2}$", time_str):
        return False, "Time must be in HH:MM format (24-hour clock)."
    try:
        input_time_obj = datetime.strptime(time_str, "%H:%M").time()
        now = datetime.now()
        
        if selected_date_str:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            if selected_date == now.date():
                if input_time_obj <= now.time():
                    return False, "This time has already passed for today. Please choose a future time."

        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()
        if not (start_time <= input_time_obj <= end_time):
            return False, "Clinic hours are 09:00 to 19:00. Please choose a time within this range."
        return True, None
    except ValueError:
        return False, "Invalid time values provided."

QUESTIONS = {
    "name": "What is your full name?",
    "email": "What is your email address?",
    "phone": "What is your 10-digit phone number?",
    "date": "Preferred appointment date? (YYYY-MM-DD)",
    "time": "Preferred appointment time? (HH:MM)"
}

def get_next_field(state):
    for field in ["name", "email", "phone", "date", "time"]:
        if not state[field]:
            return field
    return None

def validate_and_store(field, message, state):
    msg = message.strip()
    if field == "name":
        state["name"] = msg
        return True
    if field == "email":
        if is_valid_email(msg):
            state["email"] = msg
            return True
        return "Invalid email format."
    if field == "phone":
        if is_valid_phone(msg):
            state["phone"] = msg
            return True
        return "Phone number must be 10 digits."
    if field == "date":
        valid, error_msg = is_valid_date(msg)
        if valid:
            state["date"] = msg
            return True
        return error_msg
    if field == "time":
        valid, error_msg = is_valid_time(msg, state.get("date"))
        if valid:
            state["time"] = msg
            return True
        return error_msg

def is_complete(state):
    return all([state["name"], state["email"], state["phone"], state["date"], state["time"]])

def summarize(state):
    missing = [k for k in ["name", "email", "phone", "date", "time"] if not state.get(k)]
    if missing:
        return f"Please provide your {', '.join(missing)}."
    return f"""
Please confirm your dental appointment:

Clinic: Fixdent  
Location: Arundalpet, Vijayawada  

Name: {state['name']}
Email: {state['email']}
Phone: {state['phone']}
Type: Dental Consultation
Date: {state['date']}
Time: {state['time']}

Reply YES to confirm or NO to cancel.
""".strip()