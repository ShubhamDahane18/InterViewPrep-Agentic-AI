from typing import List, Dict, Optional
from typing_extensions import TypedDict

class ExtractJobInfo(TypedDict):
    job_title: str
    company: Optional[str]
    location: Optional[str]
    job_type: Optional[str]
    description: Optional[str]
    required_skills: List[str]

class TechRoundState(TypedDict):
    candidate_name : str
    company_name: str
    user_input: str 
    response: str
    core_subjects: List[str]                   # e.g., ["OS", "DS", "DBMS"]
    skills: Dict[str, List[str]]               # e.g., {"Frontend": ["HTML", "CSS"], "Backend": ["Python", "SQL"]}
    core_qa: List[Dict[str, str]]             # store Q&A for core questions
    tech_qa: List[Dict[str, str]]             # store Q&A for technical questions
    decision: Dict[str, str]                   # track decisions per round, e.g., {"core": "continue", "technical": "finish"}
    qa_counts: Dict[str, int]                  # track number of questions asked per subject/skill
    questions_per_topic: int                   # baseline per topic (e.g., 2)
    max_questions_per_topic: int               # max questions per topic (e.g., 5)
    followups_used: Dict[str, int]             # track follow-ups used per round
    job_info: Optional[ExtractJobInfo]         # Job description details
