# 🚀 AI-Powered Resume Analyzer

[![Netlify Status](https://api.netlify.com/api/v1/badges/65796857-8373-48d0-a827-a1a03db9f42d/deploy-status)](https://app.netlify.com/projects/ai-powered-resume-analyzer/deploys)
[![Frontend CI](https://github.com/harrishussain24/AI-Powered-Resume-Analyzer/actions/workflows/frontend.yml/badge.svg)](https://github.com/harrishussain24/AI-Powered-Resume-Analyzer/actions/workflows/frontend.yml)
[![Backend CI](https://github.com/harrishussain24/AI-Powered-Resume-Analyzer/actions/workflows/backend.yml/badge.svg)](https://github.com/harrishussain24/AI-Powered-Resume-Analyzer/actions/workflows/backend.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Website](https://img.shields.io/website-up-down-green-red/https/ai-powered-resume-analyzer.netlify.app)](https://ai-powered-resume-analyzer.netlify.app)

Smartly match your resume to job descriptions using AI and NLP! Upload your resume, let the backend parse and analyze it, and get instant feedback on your job fit.

---

## 🛠️ Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-8B0000?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Netlify](https://img.shields.io/badge/Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)
![Transformers](https://img.shields.io/badge/HuggingFace_Transformers-F8BF3C?style=for-the-badge&logo=huggingface&logoColor=black)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Neon](https://img.shields.io/badge/Neon-000000?style=for-the-badge&logo=data:image/svg+xml;base64,...&logoColor=white) <!-- Replace with custom badge or skip -->
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Flake8](https://img.shields.io/badge/Flake8-3F6E9A?style=for-the-badge)
![ESLint](https://img.shields.io/badge/ESLint-4B32C3?style=for-the-badge&logo=eslint&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)


---

## 📦 Project Structure

- **backend/**: FastAPI app, resume parsing, job matching, PostgreSQL models, authentication, Dockerfile  
- **frontend/**: Vue 3 app, resume upload UI, job match dashboard, TailwindCSS styling

---
[![Netlify Live](https://img.shields.io/badge/Live-Demo-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://ai-powered-resume-analyzer.netlify.app)

## ⚡ Quickstart

### 1. Backend Setup

```bash
cd backend/app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set up your .env file with DB and Supabase credentials
uvicorn main:app --reload

The backend runs on http://localhost:8000

Test endpoints with Postman or the built-in Swagger UI at /docs
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
The frontend runs on http://localhost:5173
```

### 3. 🧠 How It Works
```bash
Upload Resume: User uploads a PDF resume via the web UI.

Parse & Analyze: Backend extracts text, parses skills, experience, and contact info using spaCy and custom logic.

Job Description Upload: User uploads or pastes a job description.

Matching: Backend compares resume and job description, highlights skill matches and gaps.

Results: Frontend displays parsed resume data, match percentage, and job fit insights.
```

### 4. 📋 API Endpoints (Backend)
```bash
POST /upload-resume/ — Upload and parse a resume PDF

POST /analyze-job/ — Analyze a job description

POST /match — Match a parsed resume to a job description

POST /auth/register — Register a new user

POST /auth/login — Login and get JWT token
```

### 5. 🌐 Deployment
```bash
Backend: Deployable to Render with Docker

Frontend: Deployable to Netlify

Database: Cloud PostgreSQL (Neon)

Storage: Supabase for uploaded resumes
```

## 🤝 Contribution

**Pull requests are welcome!** For major changes, please open an issue first to discuss what you would like to change.


## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) © 2025 Harris Hussain
