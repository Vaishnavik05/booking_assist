Here is your **properly formatted README.md** — you can **directly copy-paste this into GitHub**:

---

# 🦷 Fixdent AI – Dental Appointment Assistant

Fixdent AI is a smart dental appointment assistant built using **Streamlit**, **Google Gemini**, and **Mailtrap**. It enables users to **book, reschedule, and cancel appointments** through a conversational chatbot and provides instant answers to dental FAQs using **RAG (Retrieval-Augmented Generation)** from uploaded PDFs.

---

## 🚀 Features

* **Conversational Chatbot** – Book, reschedule, or cancel appointments via chat
* **PDF-based RAG** – Upload multiple PDFs; bot answers questions from their content
* **Admin Dashboard** – View, search, and manage all bookings
* **Email Notifications** – Confirmation, cancellation, and reschedule emails via Mailtrap
* **Input Validation** – Validates email, phone number, date, and time
* **Secure Admin Login** – Password-protected admin panel
* **Persistent Storage** – All data stored in SQLite

---

## 🛠️ Tech Stack

| Component          | Technology                          |
| ------------------ | ----------------------------------- |
| Frontend/UI        | Streamlit                           |
| AI / RAG           | Google Gemini (google-generativeai) |
| PDF Processing     | pypdf                               |
| Database           | SQLite                              |
| Email              | Mailtrap SMTP                       |
| Secrets Management | Streamlit secrets                   |
| Data Display       | pandas                              |

---

## 📁 Project Structure

```
chatbot_neostats/
│
├── app/
│   ├── main.py              # Main Streamlit app
│   ├── chat_logic.py        # Chatbot intent and flow logic
│   ├── booking_flow.py      # Booking validation and flow
│   ├── rag_pipeline.py      # PDF extraction and Gemini RAG
│   ├── tools.py             # Email, Gemini, persistence tools
│   ├── admin_dashboard.py   # Admin dashboard UI
│   ├── config.py            # Loads environment variables
│   └── __init__.py          # Session state initialization
│
├── db/
│   ├── database.py          # SQLite operations
│   └── models.py            # Table schemas
│
├── .streamlit/
│   └── secrets.toml         # API keys and credentials
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Setup Instructions

### 1️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure Secrets

Create a file:

```
.streamlit/secrets.toml
```

Add the following:

```toml
GEMINI_API_KEY="your-gemini-api-key"

EMAIL_HOST="sandbox.smtp.mailtrap.io"
EMAIL_PORT=2525
EMAIL_USER="your-mailtrap-username"
EMAIL_PASSWORD="your-mailtrap-password"

ADMIN_PASSWORD="your-admin-password"
```

---

### 4️⃣ Run the App

```bash
streamlit run app/main.py
```

---

## Usage

### 🏠 Home

Learn about Fixdent AI and its features.

### 💬 Chat

* Book an appointment
* Reschedule an appointment
* Cancel an appointment
* Upload PDFs for document-based answers

### 🔐 Admin

* Login using admin password
* View all bookings
* Search by name/email
* Manage records

### 📞 Contact Us

Displays clinic contact information.

---

## 🗓️ Booking Flow

1. Start chat and choose booking
2. Enter:

   * Name
   * Email
   * Phone
   * Date
   * Time
3. Confirm appointment
4. Receive email confirmation

---

## 🔄 Reschedule / Cancel

### Reschedule

* Enter your registered email
* Provide new date
* Provide new time
* Receive reschedule email

### Cancel

* Enter your registered email
* Booking is removed
* Receive cancellation email

---

## PDF RAG (Document-Based QA)

1. Upload one or more PDFs
2. Ask questions related to the documents
3. Bot answers using Gemini + document context

---

## Deployment

You can deploy this project on:

### 🔹 Streamlit Community Cloud

1. Push project to GitHub
2. Connect repo to Streamlit Cloud
3. Add secrets
4. Deploy

### 🔹 Render.com

1. Create a new Web Service
2. Add environment variables
3. Deploy

---

## 🔐 Environment Variables

| Variable       | Description              |
| -------------- | ------------------------ |
| GEMINI_API_KEY | Google Gemini API key    |
| EMAIL_HOST     | Mailtrap SMTP host       |
| EMAIL_PORT     | Mailtrap SMTP port       |
| EMAIL_USER     | Mailtrap username        |
| EMAIL_PASSWORD | Mailtrap password        |
| ADMIN_PASSWORD | Admin dashboard password |

---

## Troubleshooting

### PDF Upload Not Working

* Only PDF files are allowed

### Gemini API Errors

* Check your API quota
* Verify API key

### Email Not Sending

* Check Mailtrap credentials
* Ensure SMTP details are correct

### Database Issues

* Make sure SQLite DB file is writable

---

## 📌 Future Enhancements

* Appointment reminders
* Doctor selection
* Payment integration
* Multi-clinic support
* Voice-based interaction
* Real-time slot availability
