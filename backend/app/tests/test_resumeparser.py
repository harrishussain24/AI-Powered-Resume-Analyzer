import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from app.services.resume_parser import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
    extract_experience,
)


sample_resume_text = """
John Doe
john.doe@example.com
+1 234-567-8900

Skills
Python, FastAPI, SQL, Docker

Work Experience
Software Engineer | CompanyX | Berlin
Jan 2020 - Present
- Developed REST APIs
- Led migration to cloud

Education
Bachelor of Science in Computer Science | University of Example | 2015 - 2019
"""


def test_extract_name():
    name = extract_name(sample_resume_text)
    assert name == "John Doe"


def test_extract_email():
    email = extract_email(sample_resume_text)
    assert email == "john.doe@example.com"


def test_extract_phone():
    phone = extract_phone(sample_resume_text)
    assert phone == "+1 234-567-8900"


def test_extract_skills():
    skills = extract_skills(sample_resume_text)
    assert "Python" in skills
    assert "FastAPI" in skills


def test_extract_experience():
    experience = extract_experience(sample_resume_text)
    assert len(experience) > 0
    assert experience[0]["title"].lower() == "software engineer"
    assert "Developed REST APIs" in experience[0]["bullets"]
