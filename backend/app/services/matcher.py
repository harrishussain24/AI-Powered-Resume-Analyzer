

def match_resume_to_job(resume: dict, job: dict) -> dict:
    resume_skills = set([skill.lower() for skill in resume.get("skills", [])])

    # Safely extract text from all bullets in all experiences
    experience_entries = resume.get("experience", [])
    all_bullets = []
    for entry in experience_entries:
        bullets = entry.get("bullets", [])
        all_bullets.extend(bullets)

    resume_experience = " ".join(all_bullets).lower()

    job_skills = set([skill.lower() for skill in job.get("skills", [])])
    job_description = job.get("description", "").lower()

    matched_skills = resume_skills.intersection(job_skills)
    skill_match_score = round(len(matched_skills) / len(job_skills), 2) if job_skills else 0.0

    experience_keywords = ["develop", "design", "lead", "build", "test", "deploy", "manage"]
    experience_score = sum(1 for word in experience_keywords if word in resume_experience and word in job_description)
    experience_match_score = round(experience_score / len(experience_keywords), 2)

    return {
        "matched_skills": list(matched_skills),
        "skill_match_score": skill_match_score,
        "experience_match_score": experience_match_score,
        "overall_score": round((skill_match_score + experience_match_score) / 2, 2)
    }
