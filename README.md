# 🤖 AI-Powered Resume Analyzer

An advanced ATS (Applicant Tracking System) Resume Screening and Analysis Platform built using **NLP, Machine Learning, Deep Learning, FastAPI, and Streamlit**.

The system analyzes resumes against job requirements, predicts shortlisting probability, identifies skill gaps, and provides personalized recommendations to improve resume quality.

---

# 🚀 Live Demo

Frontend: Add Your Streamlit URL Here

Backend API: Add Your Render URL Here

API Docs:

```text
https://your-render-url.onrender.com/docs
```

---

# 📌 Project Overview

The AI-Powered Resume Analyzer helps candidates evaluate their resumes against specific job roles.

The application uses:

* NLP for skill extraction
* Machine Learning for classification
* Deep Learning for prediction enhancement
* FastAPI for backend APIs
* Streamlit for interactive UI
* Render for cloud deployment

The system simulates a real-world ATS screening process used by recruiters.

---

# 🎯 Key Features

### Resume Analysis

* Analyze resume text against job roles
* ATS-style screening
* Resume-job matching

### NLP Features

* Technical skill extraction
* Experience detection
* Education detection
* Keyword density analysis
* Similarity score calculation

### Machine Learning Models

* Random Forest Classifier
* XGBoost Classifier

### Deep Learning Model

* Multi-Layer Perceptron (MLP)

### Ensemble Prediction

Weighted prediction using:

```text
Random Forest → 35%
XGBoost → 45%
MLP Neural Network → 20%
```

### Recommendations Engine

Provides:

* Missing skills
* Experience gap analysis
* Resume optimization suggestions
* ATS improvement recommendations

---

# 🧠 Technologies Used

## Programming Language

* Python

## Frontend

* Streamlit
* HTML
* CSS
* JavaScript

## Backend

* FastAPI
* Uvicorn

## Machine Learning

* Scikit-Learn
* XGBoost

## NLP

* TF-IDF Vectorizer
* Regex-based Skill Extraction

## Data Processing

* NumPy
* Pandas

## Deployment

* GitHub
* Render

---

# 📂 Project Structure

```text
AI-Powered_Resume_Analyzer/
│
├── app.py
├── streamlitAPP.py
├── model_bundle.pkl
├── job_info.json
├── requirements.txt
├── runtime.txt
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
└── README.md
```

---

# ⚙️ Workflow

```text
Resume Input
      │
      ▼
NLP Skill Extraction
      │
      ▼
Feature Engineering
      │
      ▼
TF-IDF Transformation
      │
      ▼
ML Models (RF + XGB)
      │
      ▼
Deep Learning Model (MLP)
      │
      ▼
Ensemble Prediction
      │
      ▼
Resume Analysis Report
```

---

# 📊 Output Generated

The application returns:

* Shortlisted / Rejected Prediction
* Confidence Score
* Skill Match Percentage
* Similarity Score
* Extracted Skills
* Missing Skills
* Experience Analysis
* Personalized Recommendations

---

# 🔥 Machine Learning Pipeline

### Feature Engineering

Generated Features:

* Skill Match Score
* Experience Match
* Education Match
* Similarity Score
* Experience Gap
* NLP Skill Features

### NLP Processing

* TF-IDF Vectorization
* Skill Detection
* Experience Extraction
* Education Classification

### Model Ensemble

```python
Final Prediction =
(RandomForest × 0.35)
+
(XGBoost × 0.45)
+
(MLP × 0.20)

```

🏗️ Application Architecture

This project provides two different user interfaces connected to the same AI Resume Analysis engine.

1️⃣ FastAPI + HTML/CSS/JavaScript UI

The primary application is built using FastAPI and serves a custom frontend created with:

HTML
CSS
JavaScript
Backend File
app.py
Features
Job Role Selection
Resume Text Input
Resume Analysis
ATS Prediction
Skill Gap Detection
Recommendations Generation

The frontend communicates with FastAPI APIs and displays results dynamically.

---

2️⃣ Streamlit Dashboard

An alternative interface is also developed using Streamlit.

Frontend File
streamlitAPP.py
Features
Interactive Dashboard
Model Prediction Visualization
Resume Analysis Summary
NLP Insights
Skill Match Metrics

This interface is useful for demonstrations, quick testing, and data visualization.

---

# 📈 Business Use Cases

* Resume Screening
* Recruitment Automation
* ATS Optimization
* HR Analytics
* Candidate Evaluation
* Skill Gap Identification

---

# ▶️ Installation

Clone Repository

```bash
git clone https://github.com/your-username/AI-Powered_Resume_Analyzer.git
```

Move to Project Directory

```bash
cd AI-Powered_Resume_Analyzer
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8765
```

Open:

```text
http://localhost:8765/docs
```

---

# ▶️ Run Frontend

```bash
streamlit run streamlitAPP.py
```

Open:

```text
http://localhost:8501
```

---

# 📷 Screenshots

Add screenshots of:

* Home Page
* Resume Analysis Page
* Prediction Dashboard
* API Documentation
* Deployment Dashboard

---

🔮 Future Improvements

This project is currently functional and deployed, but several enhancements are planned to make it more powerful and industry-ready.

1. Resume File Upload Support

Currently, the system accepts resume input only in text format.

Planned enhancements:

PDF Resume Upload
DOC/DOCX Resume Upload
Automatic Resume Text Extraction
Drag-and-Drop File Upload Feature

This will improve user experience and allow direct resume analysis without manual copy-pasting.
---

# 👨‍💻 Author

**Rishu Gurjar**

B.Tech Computer Science Student

Interested in:

* Python Development
* Data Science
* Machine Learning
* Deep Learning
* Artificial Intelligence

---

# ⭐ If you like this project

Give this repository a star and support the project.
