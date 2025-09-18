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
    user_input: str = ''
    response: str = ''
    limit:int = 3
    section_name: str = "interviewer_intro"
    get_user_intent: bool = False
    is_qa: bool = False
    skills: Optional[Dict[str, List[str]]] = None
    questions_answers: Dict[str, List[Dict[str, Optional[str]]]] = {}
    resume_info: Optional[Dict] = None
    job_info: Optional[ExtractJobInfo] = None
