from supabase import create_client, Client
import os
from INTERVIEW.RESUME.schema import ExtractResumeData
from INTERVIEW.RESUME.state import ResumeAgentState
from typing import List, Optional , Dict

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

# -----------------------------
# Resume Helper
# -----------------------------
def get_hr_resume(email: str) -> Optional[Dict]:
    """Fetch candidate resume details and return as dict for HRState.resume_info."""
    resume_resp = (
        supabase.table("resumes")
        .select("name, experience, extracurriculars")
        .eq("email", email)
        .execute()
    )

    if not resume_resp.data:
        return None

    return resume_resp.data[0]  # { "name": ..., "experience": [...], "extracurriculars": [...] }


def get_jd(email: str) -> Optional[Dict]:
    """Fetch job description details and return as dict for HRState.jd_info."""
    jd_resp = (
        supabase.table("job_description")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not jd_resp.data:
        return None

    return jd_resp.data[0]


from INTERVIEW.HR.state import HRState
from typing import List, Optional , Dict

# -----------------------------
# Helpers
# -----------------------------
def get_hr_state(email: str) -> Optional[HRState]:
    result = supabase.table("hr_states").select("state").eq("email", email).execute()
    if result.data:
        return HRState(**result.data[0]["state"])
    return None


def save_hr_state(email: str, state: HRState):
    supabase.table("hr_states").upsert({
        "email": email,
        "state": state.dict()
    }).execute()