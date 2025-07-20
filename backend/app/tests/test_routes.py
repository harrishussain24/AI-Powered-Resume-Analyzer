import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_analyze_job_empty():
    response = client.post("/analyze-job/", json={"description": ""})
    assert response.status_code == 422


def test_match_resume_job_missing_data():
    response = client.post("/match", json={"resume": {}, "job": {}})
    assert response.status_code == 422


def test_upload_resume_invalid_file():
    response = client.post("/upload-resume/", files={"file": ("empty.pdf", b"")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF file format."
