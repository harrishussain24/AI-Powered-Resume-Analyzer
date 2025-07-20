import spacy
from spacy.matcher import PhraseMatcher
import re
from app.services.skills_list import skills_list

nlp = spacy.load("en_core_web_sm")

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in skills_list if skill.strip()]
matcher.add("SKILLS", patterns)


def analyze_job_description(text: str) -> dict:
    lines = [line.rstrip() for line in text.split("\n")]

    # Extract title
    role_keywords = re.compile(
        r"(developer|engineer|intern|analyst|scientist|designer|manager)", re.I
    )
    title = None
    passed_intro = False

    for line in lines:
        if not passed_intro and "about the job" in line.lower():
            passed_intro = True
            continue
        if passed_intro and role_keywords.search(line):
            title = line.strip()
            break

    if not title:
        title = lines[0].strip() if lines else "Unknown Title"

    result = {
        "title": title,
        "skills": [],
        "experience": None,
        "education": [],
        "responsibilities": [],
        "description": text.lower(),
    }

    # Experience patterns (improved)
    experience_patterns = [
        r"\d+\+?\s*years?\s*(?:of\s*)?experience",
        r"hands[-\s]?on experience(?: with [\w\s,]+)?",
        r"proven experience(?: with [\w\s,]+)?",
        r"preferred experience(?: with [\w\s,]+)?",
        r"experience with [\w\s,]+",
        r"previous (academic|personal|work|project) (experience|projects).*",
        r"background (in|with) [\w\s]+",
        r"internship.*?(\d+[-–]\d+\s*(?:month|week)s?)",
        r"duration.*?(\d+[-–]\d+\s*(?:month|week)s?)",
        r"(\d+[-–]\d+\s*(?:month|week)s?)\s*(?:internship|program)",
        r"basic knowledge of [\w\s,]+",
        r"familiarity with [\w\s,]+",
        r"exposure to [\w\s,]+",
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            result["experience"] = match.group(0).strip()
            break

    # If no experience found, look for internship-specific patterns
    if not result["experience"]:
        internship_patterns = [
            r"internship.*?(\d+[-–]\d+\s*(?:month|week)s?)",
            r"(\d+[-–]\d+\s*(?:month|week)s?)\s*internship",
            r"duration.*?(\d+[-–]\d+\s*(?:month|week)s?)",
        ]
        for pattern in internship_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                result["experience"] = f"Internship: {match.group(1)}"
                break

    # Education
    education_keywords = ["bachelor", "master", "phd", "mba", "degree", "diploma"]
    found_education = set()
    for keyword in education_keywords:
        if keyword in text.lower():
            found_education.add(keyword)
    result["education"] = sorted(found_education)

    # Responsibilities extraction (improved)
    responsibilities = []
    collecting = False
    for line in lines:
        line_strip = line.strip()
        if re.search(r"key responsibilities", line_strip, re.I):
            collecting = True
            continue

        if collecting:
            # Stop collecting when a new section starts
            if re.match(
                r"(?i)(preferred|required|qualification|experience|education|about|additional|internship|skills|summary)",
                line_strip,
            ):
                break
            # Collect bullet points or non-empty lines (ignore blank lines)
            if re.match(r"[-•]", line_strip):
                responsibilities.append(line_strip.lstrip("-• ").strip())
            elif line_strip:
                responsibilities.append(line_strip)

    result["responsibilities"] = responsibilities

    # Skills extraction with improved matching
    doc = nlp(text.lower())
    skills = set()

    # Use PhraseMatcher for exact matches
    matches = matcher(doc)
    for _, start, end in matches:
        span = doc[start:end]
        skills.add(span.text.lower())

    # Additional pattern matching for skills that might be missed
    skill_patterns = [
        r"\b(excel|sql|python|pandas|matplotlib|power\s*bi|tableau|google\s*sheets)\b",
        r"\b(java|javascript|react|node\.js|html|css|docker|kubernetes)\b",
        r"\b(aws|azure|google\s*cloud|firebase|mongodb|postgresql|mysql)\b",
        r"\b(data\s*analytics|data\s*science|machine\s*learning|ai|ml)\b",
    ]

    for pattern in skill_patterns:
        matches = re.finditer(pattern, text.lower())
        for match in matches:
            skills.add(match.group(1))

    result["skills"] = sorted(list(skills))

    return result
