import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from streamlit.components.v1 import html
from chat_logic import detect_intent, init_memory, handle_booking, get_faq_response, handle_reschedule, handle_cancel
from rag_pipeline import extract_text_from_pdfs, create_vectorstore
from tools import rag_tool, booking_persistence_tool, email_tool
from admin_dashboard import render_admin
from db.database import init_db

init_db()

st.set_page_config(page_title="Doctor Appointment Assistant", layout="wide")

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

CUSTOM_CSS = """
<style>
.chat-card {
    background-color: #f9fbff;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e6e6e6;
    margin-bottom: 12px;
}
.confirm-card {
    background-color: #e8f5e9;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #c8e6c9;
}
.header-box {
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    padding: 24px;
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
    text-align: center;
}
.header-box h1 {
    margin: 0;
    font-size: 2.5em;
}
.header-box p {
    margin: 10px 0 0 0;
    font-size: 1.2em;
}
.plus-btn {
    width: 44px;
    height: 44px;
    background: #232323;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-top: 5px;
}
.plus-btn:hover {
    background: #444;
}
.plus-btn span {
    color: white;
    font-size: 24px;
    line-height: 0;
}
[data-testid="stFileUploader"] {
    display: none !important;
}
[data-testid="stFileUploaderDropzone"] {
    display: none !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "navbar_page" not in st.session_state:
    st.session_state.navbar_page = "home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "processed_input" not in st.session_state:
    st.session_state.processed_input = None
if "documents_uploaded" not in st.session_state:
    st.session_state.documents_uploaded = False

st.markdown("""
<div class="header-box">
    <h1>🦷 Welcome to Fixdent AI</h1>
    <p>Your Smart Dental Appointment Assistant</p>
</div>
""", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])
with nav_col1:
    if st.button("🏠 Home", key="nav_home", width="stretch"):
        st.session_state.navbar_page = "home"
        st.rerun()
with nav_col2:
    if st.button("💬 Chat", key="nav_chat", width="stretch"):
        st.session_state.navbar_page = "chat"
        st.rerun()
with nav_col3:
    if st.button("🔐 Admin", key="nav_admin", width="stretch"):
        st.session_state.navbar_page = "admin"
        st.rerun()
with nav_col4:
    if st.button("📞 Contact Us", key="nav_contact", width="stretch"):
        st.session_state.navbar_page = "contact"
        st.rerun()

st.markdown("<hr style='margin: 20px 0; border: none; border-top: 2px solid #e6e6e6;'>", unsafe_allow_html=True)

if st.session_state.navbar_page == "home":
    st.subheader("About Fixdent")
    st.write("""Welcome to Fixdent, your trusted partner in dental healthcare located in the heart of Vijayawada. We understand that scheduling dental appointments can be time-consuming and frustrating, which is why we've developed an innovative AI-powered appointment assistant that revolutionizes the way you book your dental visits.""")
    st.write("""Our state-of-the-art intelligent chatbot is available 24/7 to help you schedule appointments at your convenience. Whether you're dealing with a dental emergency, need a routine checkup, or require specialized treatment, our AI assistant guides you through the entire booking process with ease. Simply start a conversation, provide your basic details, and receive instant confirmation along with an email notification containing all your appointment information.""")
    st.write("""At Fixdent, we combine cutting-edge technology with compassionate dental care. Our clinic is equipped with modern facilities and staffed by experienced dental professionals who are committed to providing you with the highest quality treatment. We offer a comprehensive range of dental services including preventive care, cosmetic dentistry, orthodontics, oral surgery, and emergency dental services. Our flexible scheduling system allows you to choose appointment times that fit seamlessly into your busy lifestyle.""")
    st.write("""What sets Fixdent apart is our commitment to making dental care accessible and stress-free. Our AI assistant can answer your questions about clinic timings, doctor availability, services offered, and location details. You can even upload relevant medical documents or previous dental records through our secure platform, ensuring that our dental team has all the necessary information before your visit. We believe that everyone deserves quality dental care without the hassle of complicated booking procedures or long waiting times.""")
    st.write("""Getting started with Fixdent is incredibly simple. Navigate to our Chat section and begin a conversation with our AI assistant. You'll be asked to provide your name, contact information, and preferred appointment date and time. Our system will instantly check availability and confirm your booking. Within moments, you'll receive a confirmation email with your booking ID and all appointment details. If you need to reschedule or have any questions, our assistant is always ready to help. Experience the future of dental appointment booking with Fixdent today.""")
    st.stop()

if st.session_state.navbar_page == "contact":
    st.subheader("📞 Get in Touch")
    st.write("**Phone:** +91-9876543210")
    st.write("**Email:** fixdent@example.com")
    st.write("**Address:** Arundalpet, Vijayawada, Andhra Pradesh")
    st.write("**Clinic Hours:**")
    st.write("- Monday to Saturday: 9:00 AM - 7:00 PM")
    st.write("- Sunday: Closed")
    st.stop()

if st.session_state.navbar_page == "admin":
    if not st.session_state.admin_authenticated:
        st.subheader("🔐 Admin Dashboard Login")
        col_label, col_input, col_btn = st.columns([2, 4, 1])
        with col_label:
            st.markdown("**Enter Admin Password:**", unsafe_allow_html=True)
        with col_input:
            pwd = st.text_input("Admin Password", type="password", key="admin_pwd", placeholder="Password", label_visibility="collapsed")
        with col_btn:
            login_clicked = st.button("Login", key="admin_login_btn")
        if login_clicked:
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Incorrect password")
        st.stop()
    else:
        render_admin()
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.session_state.navbar_page = "home"
            st.rerun()
        st.stop()

st.subheader("💬 Chat with Fixdent AI")
st.write("Book your dental appointment in seconds")
init_memory(st.session_state)


def add_to_memory_nodup(session_state, role, content):
    if session_state.history and session_state.history[-1]["role"] == role and session_state.history[-1]["content"] == content:
        return
    session_state.history.append({"role": role, "content": content})
    session_state.history = session_state.history[-25:]

def get_generic_response(user_message):
    msg_lower = user_message.lower().strip()
    if any(word in msg_lower for word in ["thank", "thanks", "ty", "appreciate"]):
        return "You're welcome! Feel free to reach out if you need anything else. 😊"
    if any(word in msg_lower for word in ["hi", "hello", "hey"]):
        return "Hello! How can I assist you today?"
    if msg_lower in ["ok", "okay", "sure", "yes"]:
        return "Great! Is there anything else I can help you with?"
    return None

st.markdown('<div style="height:70px"></div>', unsafe_allow_html=True)

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-card'>{msg['content']}</div>", unsafe_allow_html=True)
input_container = st.container()
with input_container:
    uploaded_files = st.file_uploader(
    "Upload PDF files", type=["pdf"], accept_multiple_files=True, key="hidden_uploader", label_visibility="collapsed"
)

    col_btn, col_chat = st.columns([0.07, 0.93])

    with col_btn:
        st.markdown(
            """
            <div class="plus-btn" id="custom-plus-button">
                <span>+</span>
            </div>
            """, unsafe_allow_html=True
        )

    with col_chat:
        user_input = st.chat_input("Ask anything", key="chat_input_final")

    html_code = """
        <script>
            const parentDoc = window.parent.document;
            const plusBtn = parentDoc.getElementById("custom-plus-button");
            const fileInput = parentDoc.querySelector('input[type="file"]');
            
            if (plusBtn && fileInput) {
                plusBtn.onclick = function() {
                    fileInput.click();
                };
            }
        </script>
    """
    html(html_code, height=0)

if uploaded_files:
    try:
        all_text = ""
        for file in uploaded_files:
            all_text += extract_text_from_pdfs([file]) + "\n"
        create_vectorstore(all_text)
        st.session_state.documents_uploaded = True
        st.toast("Documents processed successfully!")
    except Exception as e:
        st.error(f"PDF processing failed: {str(e)}")
        
if user_input and user_input.strip() and user_input != st.session_state.processed_input:
    st.session_state.processed_input = user_input
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-card'>{user_input}</div>", unsafe_allow_html=True)
    add_to_memory_nodup(st.session_state, "user", user_input)
    
    response = None

    if st.session_state.get("in_cancel", False):
        response = handle_cancel(st.session_state, user_input)
        if response and ("successfully" in response or "No booking found" in response):
            st.session_state.in_cancel = False
    elif st.session_state.get("in_reschedule", False):
        response = handle_reschedule(st.session_state, user_input)
        if response and ("successfully" in response or "No booking found" in response):
            st.session_state.in_reschedule = False
    elif st.session_state.in_booking:
        response = handle_booking(user_input, st.session_state.booking_state, st.session_state)
    elif st.session_state.get("ask_new_booking"):
        if user_input.lower() == "yes":
            st.session_state.booking_state = {
                "name": None, "email": None, "phone": None,
                "booking_type": "Dental Consultation",
                "date": None, "time": None, "confirmed": False
            }
            st.session_state.in_booking = True
            st.session_state.ask_new_booking = False
            response = handle_booking(user_input, st.session_state.booking_state, st.session_state)
        else:
            response = "Okay, let me know if you need anything else."
            st.session_state.ask_new_booking = False
    else:
        intent = detect_intent(user_input)
        if intent == "booking":
            if st.session_state.booking_state.get("confirmed"):
                response = "You already have a confirmed booking. Do you want to book another appointment? (yes/no)"
                st.session_state.ask_new_booking = True
            else:
                response = handle_booking(user_input, st.session_state.booking_state, st.session_state)
        elif intent == "reschedule":
            st.session_state.in_reschedule = True
            response = handle_reschedule(st.session_state, user_input)
        elif intent == "cancel":
            response = "To cancel your appointment, please provide your email address associated with your booking:"
            st.session_state.in_cancel = True
        else:
            if st.session_state.documents_uploaded:
                try:
                    response = rag_tool(user_input)
                except Exception as e:
                    response = "Service temporarily unavailable. Please try again later."
            else:
                response = get_generic_response(user_input) or "I'm here to help you book, reschedule, or cancel dental appointments. How can I assist you today?"

    # --- THIS PART MUST BE INSIDE THE USER_INPUT BLOCK ---
    if response == "CONFIRM":
        booking_id = booking_persistence_tool(st.session_state.booking_state)
        user_email = st.session_state.booking_state['email']
        email_body = f"""
        Hello {st.session_state.booking_state['name']}, 
        Your appointment at Fixdent is confirmed!
        
        Booking ID: {booking_id}
        Date: {st.session_state.booking_state['date']}
        Time: {st.session_state.booking_state['time']}
        
        Clinic: Fixdent
        Location: Arundalpet, Vijayawada
        """
        # Call email tool
        email_tool(user_email, "Fixdent Confirmation", email_body)
        
        response = f"""<div class="confirm-card"><h4>🦷 Appointment Confirmed</h4><b>Booking ID:</b> {booking_id}</div>"""
        st.session_state.booking_state["confirmed"] = True
        st.toast("Confirmation sent to Mailtrap!")

    # Display assistant response
    if response:
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        add_to_memory_nodup(st.session_state, "assistant", response)
        st.rerun()