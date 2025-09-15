from pydantic import BaseModel
from typing import List, Optional

class RoundEvaluation(BaseModel):
    score: float
    feedback: str
    strengths: List[str]
    weaknesses: List[str]

class FullEvaluation(BaseModel):
    tech: Optional[RoundEvaluation]
    hr: Optional[RoundEvaluation]
    project: Optional[RoundEvaluation]
