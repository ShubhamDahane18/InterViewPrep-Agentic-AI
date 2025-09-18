from typing import Dict, List, Optional
from pydantic import BaseModel

class HRState(BaseModel):
    user_input: str = ''
    response: str = ''
    limit: int = 3
    section_name: str = "interviewer_intro"
    get_user_intent: bool = False
    is_qa: bool = False
    
    # Chat log style storage
    questions_answers: Dict[str, List[Dict[str, Optional[str]]]] = {}

    # Context
    resume_info: Optional[Dict] = None
    jd_info: Optional[Dict] = None