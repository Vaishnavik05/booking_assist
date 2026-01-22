def init_memory(session_state):
    if "history" not in session_state:
        session_state.history = []
    if "booking_state" not in session_state:
        session_state.booking_state = {
            "name": None, "email": None, "phone": None,
            "booking_type": "Dental Consultation",
            "date": None, "time": None, "confirmed": False
        }
    if "in_booking" not in session_state:
        session_state.in_booking = False
    if "current_field" not in session_state:
        session_state.current_field = None
    if "awaiting_confirmation" not in session_state:
        session_state.awaiting_confirmation = False
    if "in_reschedule" not in session_state:
        session_state.in_reschedule = False
    if "in_cancel" not in session_state:
        session_state.in_cancel = False
