from typing import TypedDict, List, Dict,Optional
from pydantic import BaseModel

class RoundEvaluation(TypedDict, total=False):
    score: float
    reasoning: str
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    examples: List[str]
    
class ExtractJobInfo(BaseModel):
    job_title: str
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = []
    
class EvaluationState(TypedDict, total=False):
    resume_info: Optional[Dict] = None
    jd_info :Optional[ExtractJobInfo] = None
    round_name: str = ''
    evaluation: RoundEvaluation
    feedback: str=''
    resources: str=''
    summary: str = ''
    final_report: str = ''
