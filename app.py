"""
Advanced AI Resume Analyzer - FastAPI Backend
Uses NLP (TF-IDF) + ML (RandomForest + XGBoost) + DL (MLP Neural Network)
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pickle
import json
import numpy as np
import re
import io
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

app = FastAPI(title="AI Resume Analyzer", version="2.0")
templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
with open('model_bundle.pkl', 'rb') as f:
    BUNDLE = pickle.load(f)

with open('job_info.json', 'r', encoding='utf-8') as f:
    JOB_INFO = json.load(f)

JOB_ROLES = [j['job_role'] for j in JOB_INFO]

TECH_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
    "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Redis",
    "React", "Vue", "Angular", "Node.js", "Flask", "Django", "FastAPI", "Spring",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "XGBoost",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Cloud Computing",
    "Git", "CI/CD", "DevOps", "Linux",
    "Data Analysis", "Power BI", "Tableau", "Excel",
    "Spark", "Hadoop", "Kafka",
    "REST API", "GraphQL", "Microservices",
    "Excel", "Power BI", "Tableau"
]

EDU_MAP = {'Bachelors': 0, 'Masters': 1, 'PhD': 2}
EDU_REVERSE = {v: k for k, v in EDU_MAP.items()}

def extract_skills_nlp(text: str) -> list:
    """NLP-based skill extraction using pattern matching"""
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(set(found))

def extract_experience_years(text: str) -> int:
    """Extract years of experience using regex NLP"""
    patterns = [
        r'(\d+)\+?\s*years?\s+of\s+experience',
        r'(\d+)\+?\s*years?\s+experience',
        r'experience.*?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s+exp',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    # Count job sections as proxy
    sections = len(re.findall(r'\b(20\d{2}|19\d{2})\b', text))
    return min(sections // 2, 15) if sections else 2

def detect_education(text: str) -> str:
    """Detect highest education level"""
    text_lower = text.lower()
    if any(w in text_lower for w in ['phd', 'ph.d', 'doctorate', 'doctor of']):
        return 'PhD'
    elif any(w in text_lower for w in ['master', 'msc', 'm.sc', 'mba', 'm.tech', 'ms ']):
        return 'Masters'
    else:
        return 'Bachelors'

def compute_features(resume_text: str, job_role: str, required_skills_str: str, 
                     job_exp_required: int, resume_skills_override: str = None):
    """Compute all features for prediction"""
    
    # NLP Skill Extraction
    if resume_skills_override:
        extracted_skills = [s.strip() for s in resume_skills_override.split(',')]
    else:
        extracted_skills = extract_skills_nlp(resume_text)
    
    exp_years = extract_experience_years(resume_text)
    education = detect_education(resume_text)
    edu_encoded = EDU_MAP.get(education, 0)
    
    # Skill match computation
    resume_skills_set = set([s.lower() for s in extracted_skills])
    required_skills_list = [s.strip().lower() for s in required_skills_str.split(',')]
    required_skills_set = set(required_skills_list)
    
    matched_skills = resume_skills_set & required_skills_set
    missing_skills = required_skills_set - resume_skills_set
    skill_match_score = len(matched_skills) / len(required_skills_set) if required_skills_set else 0
    
    # Feature computation
    experience_match = 1 if exp_years >= job_exp_required else 0
    education_match = 1 if edu_encoded >= 0 else 0  # basic
    
    # Similarity score (cosine via TF-IDF)
    tfidf = BUNDLE['tfidf']
    resume_vec = tfidf.transform([resume_text]).toarray()[0]
    job_vec = tfidf.transform([required_skills_str + " " + job_role]).toarray()[0]
    
    norm_r = np.linalg.norm(resume_vec)
    norm_j = np.linalg.norm(job_vec)
    similarity = np.dot(resume_vec, job_vec) / (norm_r * norm_j + 1e-8)
    
    final_score = (skill_match_score * 0.5 + experience_match * 0.3 + 
                   education_match * 0.1 + similarity * 0.1)
    
    exp_gap = exp_years - job_exp_required
    
    structured = np.array([[
        skill_match_score, experience_match, education_match,
        final_score, similarity, edu_encoded,
        skill_match_score,  # computed_skill_overlap
        np.clip(exp_gap, -5, 10),
        exp_years, job_exp_required
    ]])
    
    tfidf_feats = tfidf.transform([resume_text]).toarray()
    X = np.hstack([structured, tfidf_feats])
    X_scaled = BUNDLE['scaler'].transform(X)
    
    return {
        'X_scaled': X_scaled,
        'extracted_skills': extracted_skills,
        'exp_years': exp_years,
        'education': education,
        'skill_match_score': skill_match_score,
        'experience_match': experience_match,
        'education_match': education_match,
        'final_score': final_score,
        'similarity': float(similarity),
        'matched_skills': list(matched_skills),
        'missing_skills': list(missing_skills),
        'exp_gap': exp_gap
    }

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
@app.get("/jobs")
def get_jobs():
    """Return available job roles"""
    return {"jobs": JOB_INFO}

@app.post("/analyze")
async def analyze_resume(
    resume_text: str = Form(...),
    job_role: str = Form(...),
):
    """Main endpoint: analyze resume against job role"""
    
    # Find job info
    job = next((j for j in JOB_INFO if j['job_role'] == job_role), None)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job role '{job_role}' not found")
    
    required_skills = job['required_skills']
    job_exp = int(job['job_experience_required'])
    
    # Compute features
    feats = compute_features(resume_text, job_role, required_skills, job_exp)
    X = feats['X_scaled']
    
    # Individual model predictions
    rf_prob = BUNDLE['rf'].predict_proba(X)[0][1]
    xgb_prob = BUNDLE['xgb'].predict_proba(X)[0][1]
    mlp_prob = BUNDLE['mlp'].predict_proba(X)[0][1]
    
    # Weighted ensemble
    ensemble_prob = rf_prob * 0.35 + xgb_prob * 0.45 + mlp_prob * 0.20
    shortlisted = bool(ensemble_prob >= 0.5)
    
    # Confidence
    confidence = ensemble_prob if shortlisted else (1 - ensemble_prob)
    
    # NLP Analysis: keyword density
    words = resume_text.lower().split()
    tech_density = sum(1 for w in words if any(s.lower() in w for s in feats['extracted_skills'])) / max(len(words), 1)
    
    return {
        "shortlisted": shortlisted,
        "ensemble_probability": round(float(ensemble_prob), 4),
        "confidence": round(float(confidence) * 100, 1),
        "model_predictions": {
            "random_forest": {"probability": round(float(rf_prob), 4), "type": "ML"},
            "xgboost": {"probability": round(float(xgb_prob), 4), "type": "ML"},
            "neural_network_mlp": {"probability": round(float(mlp_prob), 4), "type": "DL"}
        },
        "nlp_analysis": {
            "extracted_skills": feats['extracted_skills'],
            "total_skills_found": len(feats['extracted_skills']),
            "experience_years_detected": feats['exp_years'],
            "education_detected": feats['education'],
            "tech_keyword_density": round(tech_density * 100, 2)
        },
        "match_metrics": {
            "skill_match_score": round(feats['skill_match_score'] * 100, 1),
            "matched_skills": feats['matched_skills'],
            "missing_skills": feats['missing_skills'],
            "experience_match": bool(feats['experience_match']),
            "experience_gap": feats['exp_gap'],
            "similarity_score": round(feats['similarity'] * 100, 1),
            "final_score": round(feats['final_score'] * 100, 1)
        },
        "job_details": {
            "role": job_role,
            "required_skills": required_skills,
            "required_experience": job_exp
        },
        "recommendations": generate_recommendations(feats, shortlisted)
    }

def generate_recommendations(feats, shortlisted):
    recs = []
    if feats['missing_skills']:
        top_missing = feats['missing_skills'][:5]
        recs.append(f"Add these missing skills: {', '.join(top_missing)}")
    if feats['exp_gap'] < 0:
        recs.append(f"You need {abs(feats['exp_gap'])} more years of experience. Add freelance/project work.")
    if feats['skill_match_score'] < 0.5:
        recs.append("Tailor your resume to include more job-specific keywords.")
    if feats['similarity'] < 0.3:
        recs.append("Use similar language as the job description in your resume.")
    if len(feats['extracted_skills']) < 5:
        recs.append("Add a dedicated Skills section with all your technical skills.")
    if not recs:
        recs.append("Great resume! Ensure your achievements are quantified with numbers.")
    return recs

@app.get("/health")
def health():
    return {"status": "ok", "models": ["RandomForest", "XGBoost", "MLP-DNN"]}