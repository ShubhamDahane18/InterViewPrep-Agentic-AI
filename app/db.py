from supabase import create_client, Client
import os
from BACKEND.INTERVIEW.RESUME.schema import ExtractResumeData
from BACKEND.INTERVIEW.RESUME.state import ResumeAgentState

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_resume(state: ResumeAgentState) -> dict:
    """Insert or update resume in Supabase (email is primary key)."""
    allowed_fields = ExtractResumeData.model_fields.keys()
    filtered_state = {k: v for k, v in state.items() if k in allowed_fields}
    resume = ExtractResumeData(**filtered_state)
    data = {
        "email": str(resume.email),
        "name": resume.name,
        "mob_no": resume.mob_no,
        "linkedin_link": resume.linkedin,
        "github_link": resume.github,
        "leetcode_link": resume.leetcode,
        "skills": resume.skills.dict() if resume.skills else None,
        "projects": [p.dict() for p in resume.projects] if resume.projects else [],
        "experience": [e.dict() for e in resume.experience] if resume.experience else [],
        "extracurriculars": [x.dict() for x in resume.extracurriculars] if resume.extracurriculars else [],
    }
    response = supabase.table("resumes").upsert(data).execute()
    return resume

def get_resume(email: str) -> dict | None:
    """Fetch resume by email."""
    response = supabase.table("resumes").select("*").eq("email", email).execute()
    if response.data:
        return response.data[0]  # return first row
    return None