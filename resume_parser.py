import re
import spacy
import pdfplumber
import os

nlp = spacy.load("en_core_web_sm")

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+")
PHONE_RE = re.compile(r"(\+?\d[\d \-()]{7,}\d)")

SKILLS_DB = [
    "python", "java", "javascript", "react", "node", "sql", "aws", "docker",
    "linux", "machine learning", "nlp", "tensorflow", "pytorch", "excel",
    "data analysis", "project management", "ui", "ux", "figma"
]


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text content from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def parse_resume(file_path: str) -> dict:
    """Parse PDF or TXT resume and extract structured info."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type. Use .pdf or .txt")

    doc = nlp(text)

    # Extract name (first PERSON entity)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    email = EMAIL_RE.findall(text)
    phone = PHONE_RE.findall(text)

    skills = [s for s in SKILLS_DB if s.lower() in text.lower()]

    education = []
    for line in text.splitlines():
        if re.search(r"\b(Bachelor|Master|PhD|B\.Tech|M\.Tech|BSc|MSc)\b", line, re.I):
            education.append(line.strip())

    experience = []
    for line in text.splitlines():
        if "experience" in line.lower() or re.search(r"\byears?\b", line, re.I):
            experience.append(line.strip())

    return {
        "name": name,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "skills": list(set(skills)),
        "education": education,
        "experience": experience,
        "raw_text": text
    }
