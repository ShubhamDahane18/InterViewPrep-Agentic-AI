from typing import Dict, List, Optional
from pydantic import BaseModel

class ProjectState(BaseModel):
    section_name: str = "interviewer_intro"
    current_project_index: int = -1

    in_project_qa: bool = False

    # Resume + JD data
    resume_info: Optional[Dict] = None
    jd_info: Optional[Dict] = None

    # Latest interaction
    user_input: Optional[str] = None
    response: Optional[str] = None

    # Section-wise Q&A
    questions_answers: Dict[str, List[Dict[str, Optional[str]]]] = {}

    # All projects (list of project dictionaries)
    projects: List[Dict[str, Optional[str]]] = []