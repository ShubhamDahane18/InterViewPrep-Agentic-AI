import streamlit as st
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

# Pydantic model for JD
class ExtractJobInfo(BaseModel):
    job_title: str
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = []

st.title("📄 Resume Parser & JD Input")

api_url = st.text_input("API Endpoint", value="http://localhost:8000")

# --- Step 1: Upload & parse resume ---
uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
if uploaded:
    if st.button("Parse Resume"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
            resp = requests.post(f"{api_url}/parse_resume", files=files)
            if resp.ok:
                st.success("Resume saved successfully!")
                data = resp.json()
                st.session_state["email"] = data.get("email")
                st.subheader("Extracted Resume")
                st.json(data)

# --- Step 2: Get Job Description info ---
st.subheader("Enter Job Description (JD) Info")
with st.form("jd_form"):
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    location = st.text_input("Location")
    job_type = st.text_input("Job Type (Full-time, Internship, etc.)")
    description = st.text_area("Job Description")
    skills_text = st.text_input("Required Skills (comma separated)")

    submitted = st.form_submit_button("Submit JD")
    if submitted:
        required_skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        jd = ExtractJobInfo(
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            description=description,
            required_skills=required_skills,
        )

        # Save JD via FastAPI
        if "email" not in st.session_state:
            st.error("Upload a resume first to associate JD with a user")
        else:
            email = st.session_state["email"]
            resp = requests.post(f"{api_url}/save_jd/{email}", json=jd.dict())
            if resp.ok:
                st.success("JD saved successfully!")
                st.subheader("Structured JD Info")
                st.json(jd.dict())
            else:
                st.error(f"Failed to save JD: {resp.text}")