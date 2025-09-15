# app.py
from fastapi import FastAPI, UploadFile, File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys , os
from INTERVIEW.util import extract_text_and_links_from_pdf
from INTERVIEW.RESUME.graph import build_graph

from typing import Dict
from app.db import save_resume
from INTERVIEW.RESUME.schema import ExtractResumeData


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse_resume", response_model=ExtractResumeData)
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Step 1: Extract text & links
    text, links = extract_text_and_links_from_pdf(file.file)

    # Step 2: Run graph → produces state dict
    graph = build_graph()
    input_state = {"full_text": text, "links": links}
    final_state: Dict = graph.invoke(input_state)

    # Step 3: Save to SupaB0ase and validate schema
    try:
        saved_resume = save_resume(final_state)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 4: Return structured resume to frontend for preview
    return saved_resume  # Pydantic ExtractResumeData object

from pydantic import BaseModel
from typing import List, Optional
from app.db import supabase  # your existing supabase client

class ExtractJobInfo(BaseModel):
    job_title: str
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = []


@app.post("/save_jd/{email}")
def save_jd(email: str, jd: ExtractJobInfo):
    """
    Save JD info for a specific user email
    """
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Upsert JD linked to the user email
    response = supabase.table("job_descriptions").upsert({
        "user_email": email,
        "job_title": jd.job_title,
        "company": jd.company,
        "location": jd.location,
        "job_type": jd.job_type,
        "description": jd.description,
        "required_skills": jd.required_skills
    }).execute()

    return {"message": "JD saved successfully", "email": email}