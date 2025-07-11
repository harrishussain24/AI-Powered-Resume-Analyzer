import spacy
from spacy.matcher import PhraseMatcher
import json
import re
import os
from services.skills_list import skills_list


nlp = spacy.load("en_core_web_sm")

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in skills_list if skill.strip()]
matcher.add("SKILLS", patterns)

def analyze_job_description(text: str) -> dict:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Improved title extraction: Find first line with role keywords after "About the job"
    role_keywords = re.compile(r"(developer|engineer|intern|analyst|scientist|designer|manager)", re.I)
    title = None
    passed_intro = False

    for line in lines:
        if not passed_intro and "about the job" in line.lower():
            passed_intro = True
            continue
        if passed_intro and role_keywords.search(line):
            title = line
            break

    if not title:
        title = lines[0] if lines else None  # fallback to first line

    result = {
        "title": title,
        "skills": [],
        "experience": None,
        "education": []
    }

    # Extended experience patterns
    experience_patterns = [
        r'\d+\+?\s*years?\s*(?:of\s*)?experience',
        r'hands[-\s]?on experience(?: with [\w\s,]+)?',
        r'proven experience(?: with [\w\s,]+)?',
        r'experience with [\w\s,]+',
        r'previous (academic|personal|work|project) (experience|projects).*',
        r'background (in|with) [\w\s]+'
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            result["experience"] = match.group(0).strip()
            break

    # Simple education detection
    education_keywords = ["bachelor", "master", "phd", "mba", "degree", "diploma"]
    found_education = set()
    for keyword in education_keywords:
        if keyword in text.lower():
            found_education.add(keyword)
    result["education"] = sorted(found_education)

    # Skill matching using PhraseMatcher
    doc = nlp(text)
    skills = set()
    matches = matcher(doc)
    for _, start, end in matches:
        span = doc[start:end]
        skills.add(span.text.lower())

    result["skills"] = sorted(list(skills))

    return result
