from pypdf import PdfReader
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

documents = []

def get_working_model():
    models = genai.list_models()
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            return m.name
    return None

MODEL_NAME = get_working_model()

def extract_text_from_pdfs(files):
    text = ""
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    return text

def create_vectorstore(text):
    global documents
    documents = [text[i:i+500] for i in range(0, len(text), 500)]

def rag_query(query):
    if not documents:
        return "No documents uploaded yet."

    if not MODEL_NAME:
        return "No supported Gemini model found."

    context = "\n".join(documents[:5])
    prompt = f"Use the following context to answer:\n{context}\n\nQuestion: {query}"

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text
