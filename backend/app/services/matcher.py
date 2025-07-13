import re
import torch
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz, process

# Lazy load model to save memory
_model = None

def get_model():
    global _model
    if _model is None:
        # Use smaller model for memory efficiency
        _model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return _model

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

    # Join all bullets to a single string (fallback)
    resume_experience_text = " ".join(all_bullets).lower()

    # Lowercase job description text
    job_description = job.get("description", "").lower()

    # Fuzzy skill matching
    matched_skills = fuzzy_skill_match(resume_skills, job_skills, threshold=80)
    skill_match_score = round(len(matched_skills) / len(job_skills), 2) if job_skills else 0.0

    # Calculate missing skills
    missing_skills = list(job_skills - matched_skills)

    # Experience semantic similarity
    if all_bullets and job_description.strip():
        model = get_model()
        embeddings_resume = model.encode(all_bullets, convert_to_tensor=True, device='cpu')
        avg_embedding_resume = torch.mean(embeddings_resume, dim=0)
        embeddings_job = model.encode(job_description, convert_to_tensor=True, device='cpu')
        cosine_score = util.pytorch_cos_sim(avg_embedding_resume, embeddings_job)
        experience_match_score = round(float(cosine_score.item()), 2)
    elif resume_experience_text.strip() and job_description.strip():
        model = get_model()
        embeddings_resume = model.encode(resume_experience_text, convert_to_tensor=True, device='cpu')
        embeddings_job = model.encode(job_description, convert_to_tensor=True, device='cpu')
        cosine_score = util.pytorch_cos_sim(embeddings_resume, embeddings_job)
        experience_match_score = round(float(cosine_score.item()), 2)
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