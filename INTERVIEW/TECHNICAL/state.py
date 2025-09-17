from pydantic import BaseModel
from typing import List, Dict, Optional

class ExtractJobInfo(BaseModel):
    job_title: str
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = []

class TechRoundState(BaseModel):
    candidate_name: str = ''
    company_name: str = ''
    user_input: str = ''
    response: str = ''
    core_subjects: Optional[List[str]] = None
    skills: Optional[Dict[str, List[str]]] = None
    core_qa: Optional[List[Dict[str, str]]] = None
    tech_qa: Optional[List[Dict[str, str]]] = None
    decision: Optional[Dict[str, str]] = None
    qa_counts: Optional[Dict[str, int]] = None
    questions_per_topic: Optional[int] = None
    max_questions_per_topic: Optional[int] = None
    followups_used: Optional[Dict[str, int]] = None
    job_info: Optional[ExtractJobInfo] = None