import spacy
from spacy.matcher import PhraseMatcher
import json
import re
import os

# Load the skills list once (adjust path if needed)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
skills_path = os.path.join(BASE_DIR, "skills_list.json")

with open(skills_path, "r") as f:
    skills_list = json.load(f)

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

    exp_match = re.search(r'(\d+\+?\s*years?)\s*(?:of\s*)?experience', text, re.I)
    if exp_match:
        result["experience"] = exp_match.group(1)

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
