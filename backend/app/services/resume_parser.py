from pdfminer.high_level import extract_text
from fastapi import UploadFile
import spacy
import re
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
    # Regular expression for matching email addresses
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    if emails:
        return emails[0]  # Return the first email found
    return "No email found in the text."

def extract_phone(text: str) -> str:
    # Regular expression for matching phone numbers
    phone_pattern = r"(\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,5}[\s\-]?\d{3,5})"
    phones = re.findall(phone_pattern, text)
    if phones:
        return phones[0]  # Return the first phone number found
    return "No phone number found in the text."


def extract_skills(text: str) -> list:
    # Normalize special dashes
    text = re.sub(r"[–—−‐]", "-", text)
    # Match SKILLS section to next known section or end of file
    match = re.search(
        r"(?is)^skills\s*\n(.*?)(?=\n(?:certifications|education|experience|projects|summary|contact|languages|profile|additional information|additional)\b|\Z)",
        text,
        re.M,
    )
    if not match:
        return []
    
    # Join broken lines in the skills section
    skills_section = match.group(1)
    skills_section = re.sub(r"\n+", " ", skills_section)  # all newlines become spaces

    # Now split cleanly by known delimiters
    raw_skills = re.split(r"\s*\|\s*|\s{2,}|,\s*", skills_section)

    # Strip whitespace, remove empties
    skills = [s.strip() for s in raw_skills if s.strip()]
    return skills

def extract_experience(text: str) -> str:
    # Normalize special dashes
    text = re.sub(r"[–—−‐]", "-", text)
    # Match SKILLS section to next known section or end of file
    match = re.search(
    r"(?is)(?:^|\n)(work experience|experience|professional experience)\s*\n(.*?)(?=\n(?:certifications|education|skills|projects|summary|contact|languages|profile|additional information|additional)\b|\Z)",
    text,
    re.M,
)
    if not match:
        return []
    # Join broken lines in the skills section
    experience_section = match.group(1)
    experience_section = re.sub(r"\n+", " ", experience_section)  # all newlines become spaces
    print("---------- EXPERIENCE SECTION RAW TEXT ----------")
    print(experience_section)
    print("---------- END OF EXPERIENCE SECTION RAW TEXT ----------")

    # Now split cleanly by known delimiters
    raw_experience = re.split(r"\s*\|\s*|\s{2,}|,\s*", experience_section)

    # Strip whitespace, remove empties
    skills = [s.strip() for s in raw_experience if s.strip()]
    return skills

def extract_education(text: str) -> list:
    import re

    # Normalize dashes
    text = re.sub(r"[–—−‐]", "-", text)

    # Extract education block (case-insensitive)
    match = re.search(
        r"(?is)^education\s*\n(.*?)(?=\n[A-Z][A-Z\s]+\n|certifications|skills|experience|projects|\Z)",
        text,
        re.M,
    )
    education_section = match.group(1).strip() if match else ""
    

    # Split by blank lines (one or more)
    blocks = re.split(r"\n\s*\n", education_section)

    degree_keywords = [
        "bachelor", "master", "ph.d", "msc", "bsc", "bs", "ms",
        "m.sc", "b.sc", "doctor", "mba", "m.tech", "b.tech"
    ]

    educations = []

    for block in blocks:
        lines = [line.strip("•- ").strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue

        current_education = {
            "degree": "",
            "start_date": "",
            "end_date": "",
            "university": "",
            "location": ""
        }

        # Extract degree and university/location first
        for i, line in enumerate(lines):
            line_lower = line.lower()

            if not current_education["degree"] and any(k in line_lower for k in degree_keywords):
                # Clean degree line by removing trailing date info
                degree_line = line.strip()
                degree_line_clean = re.sub(
                    r"(expected\s*\d{4}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*\d{4}(-\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*\d{4})?)",
                    "",
                    degree_line,
                    flags=re.IGNORECASE,
                ).strip()
                current_education["degree"] = degree_line_clean
                continue

            if ("|" in line or "," in line) and not current_education["university"]:
                parts = [p.strip() for p in re.split(r"\||,", line)]
                if len(parts) >= 2:
                    current_education["university"] = parts[0]
                    current_education["location"] = ", ".join(parts[1:])
                else:
                    current_education["university"] = parts[0]
                continue

        # Scan all lines for dates (expected year, date ranges, single dates)
        for line in lines:
            line_lower = line.lower()

            # Expected year (priority for end_date)
            expected_match = re.search(r"expected\s*(\d{4})", line_lower)
            if expected_match and not current_education["end_date"]:
                current_education["end_date"] = expected_match.group(1)

            # Date range like "Jan 2019 - Jan 2023"
            date_matches = re.findall(
                r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*\d{4}",
                line,
                re.IGNORECASE,
            )
            if len(date_matches) == 2:
                current_education["start_date"] = date_matches[0]
                current_education["end_date"] = date_matches[1]
                break  # date range found, no need to scan further

            # Single date if no end_date yet
            elif len(date_matches) == 1 and not current_education["end_date"]:
                current_education["end_date"] = date_matches[0]

        if current_education["degree"]:
            educations.append(current_education)

    return educations

