# state.py
from typing import List, Dict, Optional, Any
from typing_extensions import TypedDict

class TechRoundState(TypedDict):
    company_name: str
    core_subjects: List[str]
    skills: Dict[str, List[str]]
    core_qa: List[Dict[str, str]]
    tech_qa: List[Dict[str, str]]
    evaluation: Dict[str, Any]
    decision: Dict[str, str]
    summary: Optional[str]
    qa_counts: Dict[str, int]       # track questions asked per subject/skill
    questions_per_topic: int        # baseline per topic (e.g., 2)
    max_questions_per_topic: int  
    followups_used: Dict[str, int]  # absolute cap (e.g., 5)