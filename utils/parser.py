import pdfplumber
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF using PyMuPDF first, fallback to pdfplumber."""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if text.strip():
            return text
    except:
        pass

    # Fallback
    pdf_file.seek(0)
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])

def extract_text_from_url(url: str) -> str:
    """Extract main visible text from a webpage."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator="\n")
    except:
        return ""

def get_clean_text(text: str) -> str:
    """Clean raw text (remove excessive newlines etc)."""
    lines = text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)
