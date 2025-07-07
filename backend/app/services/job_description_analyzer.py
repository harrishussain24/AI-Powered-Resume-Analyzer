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
    title = lines[0] if lines else None

    result = {
        "title": title,
        "skills": [],
        "experience": None,
        "education": []
    }

    experience_patterns = [
    r'\d+\+?\s*years?\s*(?:of\s*)?experience',
    r'hands[-\s]?on experience(?: with [\w\s,]+)?',
    r'proven experience(?: with [\w\s,]+)?',
    r'experience with [\w\s,]+'
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            result["experience"] = match.group(0).strip()
            break

    education_keywords = ["bachelor", "master", "phd", "mba", "degree", "diploma"]
    for keyword in education_keywords:
        if keyword in text.lower():
            result["education"].append(keyword)

    doc = nlp(text)

    skills = set()
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        skills.add(span.text.lower())

    result["skills"] = sorted(list(skills))

    return result
