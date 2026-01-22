import re
from datetime import datetime
from booking_flow import get_next_field, is_valid_date, is_valid_time, validate_and_store, is_complete, summarize, QUESTIONS
from db.database import delete_booking_by_email, update_booking_time
from app.tools import email_tool

def detect_intent(message):
    msg = message.lower().strip()
    if any(greet in msg for greet in ["hi", "hello", "hey"]): return "greeting"
    if "how are you" in msg: return "wellbeing"
    if any(word in msg for word in ["timing", "available", "open", "hours"]): return "timings"
    if any(word in msg for word in ["location", "where", "address"]): return "location"
    if "doctor" in msg and any(word in msg for word in ["available", "timing"]): return "doctor_timings"
    if any(word in msg for word in ["reschedule", "change my appointment", "move"]): return "reschedule"
    if any(word in msg for word in ["cancel", "delete my appointment", "remove"]): return "cancel"
    if any(word in msg for word in ["book", "appointment", "schedule"]): return "booking"
    return "rag"

def get_faq_response(intent):
    faqs = {
        "greeting": "Hello! How can I assist you today?",
        "wellbeing": "I'm just a bot, but I'm here to help you with your dental needs!",
        "timings": "Our clinic is open from 9:00 AM to 7:00 PM, Monday to Saturday.",
        "location": "We are located at Arundalpet, Vijayawada.",
        "doctor_timings": "Our doctors are available from 10:00 AM to 6:00 PM. Would you like to book an appointment?"
    }
    return faqs.get(intent)

def init_memory(session_state):
    if "history" not in session_state: session_state.history = []
    if "booking_state" not in session_state:
        session_state.booking_state = {"name": None, "email": None, "phone": None, "booking_type": "Dental Consultation", "date": None, "time": None, "confirmed": False}
    if "in_booking" not in session_state: session_state.in_booking = False
    if "in_reschedule" not in session_state: session_state.in_reschedule = False
    if "in_cancel" not in session_state: session_state.in_cancel = False
    if "current_field" not in session_state: session_state.current_field = None
    if "awaiting_confirmation" not in session_state: session_state.awaiting_confirmation = False

def handle_reschedule(session_state, user_input):
    for key in ["reschedule_email", "reschedule_date", "reschedule_time"]:
        if key not in session_state: session_state[key] = None

    if not session_state.reschedule_email:
        clean_input = user_input.strip()
        if re.match(r"[^@]+@[^@]+\.[^@]+", clean_input):
            session_state.reschedule_email = clean_input
            return "Please provide the new date for your appointment (YYYY-MM-DD):"
        return "To reschedule, please enter the email address used for the booking:"

    if not session_state.reschedule_date:
        valid, error_msg = is_valid_date(user_input.strip())
        if valid:
            session_state.reschedule_date = user_input.strip()
            return "Please provide the new time for your appointment (HH:MM):"
        return error_msg

    if not session_state.reschedule_time:
        valid, error_msg = is_valid_time(user_input.strip(), session_state.reschedule_date)
        if valid:
            session_state.reschedule_time = user_input.strip()
            success = update_booking_time(session_state.reschedule_email, session_state.reschedule_date, session_state.reschedule_time)
            
            if success:
                email_body = f"Hello, your dental appointment at Fixdent has been rescheduled to {session_state.reschedule_date} at {session_state.reschedule_time}."
                email_tool(session_state.reschedule_email, "Fixdent – Appointment Rescheduled", email_body)
            
            email_ref = session_state.reschedule_email
            session_state.reschedule_email = session_state.reschedule_date = session_state.reschedule_time = None
            session_state.in_reschedule = False
            return "Appointment rescheduled successfully!" if success else f"No booking found for {email_ref}."
        return error_msg

def handle_cancel(session_state, user_input):
    if "cancel_email" not in session_state: session_state.cancel_email = None
    if not session_state.cancel_email:
        if re.match(r"[^@]+@[^@]+\.[^@]+", user_input.strip()):
            session_state.cancel_email = user_input.strip()
            success = delete_booking_by_email(session_state.cancel_email)
            if success:
                email_tool(session_state.cancel_email, "Fixdent – Appointment Cancelled", "Your dental appointment at Fixdent has been successfully cancelled.")
            session_state.cancel_email = None
            session_state.in_cancel = False
            return "Your appointment has been cancelled successfully!" if success else "No booking found with that email."
        return "To cancel, please enter your email address associated with your booking:"

def handle_booking(message, state, session_state):
    msg = message.strip().lower()
    if not session_state.in_booking:
        session_state.in_booking = True
        session_state.current_field = get_next_field(state)
        return QUESTIONS[session_state.current_field]
    if session_state.awaiting_confirmation:
        if msg == "yes":
            state["confirmed"] = True
            session_state.in_booking = False
            session_state.awaiting_confirmation = False
            return "CONFIRM"
        if msg == "no":
            session_state.in_booking = False
            session_state.awaiting_confirmation = False
            return "Booking cancelled. How else can I help?"
        return "Please reply YES to confirm or NO to cancel."
    field = session_state.current_field
    result = validate_and_store(field, message, state)
    if result is not True: return result
    if is_complete(state):
        session_state.awaiting_confirmation = True
        return summarize(state)
    session_state.current_field = get_next_field(state)
    return QUESTIONS[session_state.current_field]