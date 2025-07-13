import re
from rapidfuzz import fuzz, process
from difflib import SequenceMatcher

def text_similarity(text1, text2):
    """Simple text similarity without ML models"""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def fuzzy_skill_match(resume_skills, job_skills, threshold=80):
    """
    Perform fuzzy matching between resume skills and job skills using rapidfuzz.
    Returns a set of matched skills from job_skills.
    """
    matched_skills = set()
    for r_skill in resume_skills:
        best_match = process.extractOne(r_skill, job_skills, scorer=fuzz.token_sort_ratio)
        if best_match and best_match[1] >= threshold:
            matched_skills.add(best_match[0])
    return matched_skills

def match_resume_to_job(resume: dict, job: dict) -> dict:
    # Lowercase sets of skills from resume and job description
    resume_skills = set([skill.lower() for skill in resume.get("skills", [])])
    job_skills = set([skill.lower() for skill in job.get("skills", [])])

    # Extract all bullets from experience entries
    experience_entries = resume.get("experience", [])
    all_bullets = []
    for entry in experience_entries:
        bullets = entry.get("bullets", [])
        all_bullets.extend(bullets)

    # Join all bullets to a single string
    resume_experience_text = " ".join(all_bullets).lower()

    # Lowercase job description text
    job_description = job.get("description", "").lower()

    # Fuzzy skill matching
    matched_skills = fuzzy_skill_match(resume_skills, job_skills, threshold=80)
    skill_match_score = round(len(matched_skills) / len(job_skills), 2) if job_skills else 0.0

    # Calculate missing skills
    missing_skills = list(job_skills - matched_skills)

    # Experience similarity using lightweight text comparison
    if resume_experience_text.strip() and job_description.strip():
        experience_match_score = round(text_similarity(resume_experience_text, job_description), 2)
    else:
        experience_match_score = 0.0

    # Overall average score of skill and experience match
    overall_score = round((skill_match_score + experience_match_score) / 2, 2)

    result = {
        "matched_skills": list(matched_skills),
        "missing_skills": missing_skills,
        "skill_match_score": skill_match_score,
        "experience_match_score": experience_match_score,
        "overall_score": overall_score,
    }
    
    return result