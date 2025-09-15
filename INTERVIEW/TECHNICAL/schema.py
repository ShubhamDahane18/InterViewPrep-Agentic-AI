# schemas.py
from typing import List, Dict,Optional
from pydantic import BaseModel, Field

class QAEntry(BaseModel):
    """Represents a single question-answer pair."""
    question: str = Field(description="A single, unique interview question.")
    answer: Optional[str] = None

class EvaluationEntry(BaseModel):
    """Represents the evaluation for one section of the interview."""
    score: float = Field(description="A score from 0.0 to 10.0 for the section.")
    feedback: str = Field(description="Concise feedback on the candidate's performance for this section.")
    strengths: List[str] = Field(default_factory=list, description="Key strengths identified in this section.")
    weaknesses: List[str] = Field(default_factory=list, description="Key weaknesses identified in this section.")

class FullEvaluation(BaseModel):
    """A full evaluation of both core and technical sections."""
    core: EvaluationEntry
    technical: EvaluationEntry
   
class ResourceSuggestions(BaseModel):
    """Represents learning resources for weak subjects/skills."""
    resources: Dict[str ,List[str]] = Field(
        description="A mapping of subject/skill → list of suggested resources"
    )