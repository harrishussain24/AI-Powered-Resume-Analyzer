from pdfminer.high_level import extract_text
from fastapi import UploadFile
import spacy
from spacy.matcher import PhraseMatcher
from services.skills import skills_list  


def extract_text_from_pdf(file: UploadFile) -> str:
    
    # Extract text from a pdf.
    text = extract_text(file.file)
    # Close the file after reading
    file.file.close()
    # Return the extracted text
    if not text:
        return "No text found in the PDF file."
    text = text.strip()
    if not text:
        return "The PDF file is empty or contains no readable text."
    # Return the extracted text
    return text

def analyze_resume_text(text: str) -> dict:
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience,
    }

def extract_name(text: str) -> str:
    nlp = spacy.load("en_core_web_sm")
    lines = text.splitlines()
    header = "\n".join(lines[:5])
    doc = nlp(header)

    # Extract named entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            parts = ent.text.split("\n")
            for part in parts:
                if "+" not in part and not any(char.isdigit() for char in part):
                    return part.strip()

    return "No name found in the text."

def extract_email(text: str) -> str:
    import re

    # Regular expression for matching email addresses
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    if emails:
        return emails[0]  # Return the first email found
    return "No email found in the text."

def extract_phone(text: str) -> str:
    import re

    # Regular expression for matching phone numbers
    phone_pattern = r"(\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,5}[\s\-]?\d{3,5})"
    phones = re.findall(phone_pattern, text)
    if phones:
        return phones[0]  # Return the first phone number found
    return "No phone number found in the text."


def extract_skills(text: str) -> list:
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    patterns = [nlp.make_doc(skill) for skill in skills_list]
    matcher.add("SKILLS", patterns)

    doc = nlp(text)  # Process the input text, NOT a hardcoded string

    matches = matcher(doc)
    extracted_skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        extracted_skills.add(span.text)

    return list(extracted_skills) 

def extract_education(text: str) -> list:
    import re
    education = []

    pattern = r"""(?ix)   # ignore case, verbose
    \b
    (
      (B\.?Sc\.?|Bachelor(?:'s)?(?: of)?(?: Science| Arts| Engineering| Technology)?) |
      (M\.?Sc\.?|Master(?:'s)?(?: of)?(?: Science| Arts| Engineering| Technology)?) |
      (Ph\.?D\.?|Doctorate|Doctor of Philosophy)
    )
    \b
    (?:\s(?:in|of)\s[\w\s&]+)?  # Optional degree field
    """

    matches = re.findall(pattern, text)

    # Each match is a tuple with groups, flatten them
    for match in matches:
        # match is a tuple of alternatives, filter non-empty
        degree = next((m for m in match if m), None)
        if degree:
            education.append(degree.strip())

    return list(set(education)) 

def extract_experience(text: str) -> str:
    # This is a placeholder function. In a real-world scenario, you would implement logic
    # to extract work experience from the text, possibly using regex or NLP techniques.
    
    # For simplicity, we will return a generic message.
    return "Experience extraction not implemented yet. Please provide more details."
