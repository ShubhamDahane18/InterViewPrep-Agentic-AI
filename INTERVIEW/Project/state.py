from typing import Dict, List, Optional
from pydantic import BaseModel

class Project(BaseModel):
    name: str = ''
    time_period: Optional[str] = None
    tech_stack: List[str] = []
    features: List[str] = []

class ProjectState(BaseModel):
    section_name: str = "interviewer_intro"
    current_project_index: int = -1
    limit:int = 5

    is_project_qa: bool = False
    get_user_intent: bool = False

    # Resume + JD data
    user_name: Optional[str] = ''
    jd_info: Optional[Dict] = None

    # Latest interaction
    user_input: Optional[str] = None
    response: Optional[str] = None

    # Section-wise Q&A
    questions_answers: Dict[str, List[Dict[str, Optional[str]]]] = {}

    # All projects (list of project dictionaries)
    projects: List[Project] = []