import streamlit as st
import requests
import pandas as pd

st.set_page_config(
page_title="AI Resume Analyzer",
page_icon="📄",
layout="wide"
)

# API_URL = "http://127.0.0.1:8765"
API_URL = "https://ai-powered-resumes-checker-1.onrender.com"

st.title("🤖 AI Resume Analyzer")
st.markdown("NLP + Machine Learning + Deep Learning Based ATS Resume Screening")

# Load jobs

try:
    jobs_response = requests.get(f"{API_URL}/jobs")
    jobs = jobs_response.json()["jobs"]
    job_roles = [job["job_role"] for job in jobs]

except Exception:
    st.error("FastAPI backend is not running.")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    resume_text = st.text_area(
    "Paste Resume",
    height=350
    )

with col2:
    selected_role = st.selectbox(
    "Select Job Role",
    job_roles
    )


analyze_btn = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)


if analyze_btn:
    if resume_text.strip() == "":
        st.warning("Please paste resume text")
        st.stop()

payload = {
    "resume_text": resume_text,
    "job_role": selected_role
}

response = requests.post(
    f"{API_URL}/analyze",
    data=payload
)

result = response.json()

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Confidence",
        f"{result['confidence']}%"
    )

with c2:
    st.metric(
        "Skill Match",
        f"{result['match_metrics']['skill_match_score']}%"
    )

with c3:
    st.metric(
        "Similarity Score",
        f"{result['match_metrics']['similarity_score']}%"
    )

if result["shortlisted"]:
    st.success("✅ Candidate Likely To Be Shortlisted")
else:
    st.error("❌ Candidate Not Likely To Be Shortlisted")

st.subheader("📊 Model Predictions")

models = result["model_predictions"]

model_df = pd.DataFrame({
    "Model": [
        "Random Forest",
        "XGBoost",
        "MLP Neural Network"
    ],
    "Probability": [
        models["random_forest"]["probability"],
        models["xgboost"]["probability"],
        models["neural_network_mlp"]["probability"]
    ]
})

st.dataframe(
    model_df,
    use_container_width=True
)

st.subheader("🧠 NLP Analysis")

st.write(
    "Skills Found:",
    ", ".join(result["nlp_analysis"]["extracted_skills"])
)

st.write(
    "Experience:",
    result["nlp_analysis"]["experience_years_detected"]
)

st.write(
    "Education:",
    result["nlp_analysis"]["education_detected"]
)

st.subheader("✅ Matched Skills")
st.write(result["match_metrics"]["matched_skills"])

st.subheader("❌ Missing Skills")
st.write(result["match_metrics"]["missing_skills"])

st.subheader("💡 Recommendations")

for rec in result["recommendations"]:
    st.info(rec)

