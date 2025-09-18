from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class QAItem(BaseModel):
    question: str
    answer: str

class RoundQA(BaseModel):
    round_name: str
    qa: List[QAItem]

class RoundEvaluation(BaseModel):
    """
    Structured evaluation of a candidate's interview round.
    """
    score: float = Field(
        ...,
        ge=0,
        le=10,
        description="Numerical evaluation of the candidate's performance (0.0–10.0 scale)."
    )
    feedback: str = Field(
        ...,
        description="General feedback summary about the candidate's performance in this round."
    )
    reasoning: Optional[str] = Field(
        None,
        description="Concise explanation of why the candidate received this score."
    )
    strengths: List[str] = Field(
        default_factory=list,
        description="Key areas where the candidate performed well."
    )
    weaknesses: List[str] = Field(
        default_factory=list,
        description="Areas where the candidate struggled or showed gaps."
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Actionable advice for improvement."
    )
    examples: List[str] = Field(
        default_factory=list,
        description="Specific excerpts or instances from candidate answers supporting this evaluation."
    )

class ResourceItem(BaseModel):
    name: str

class FullEvaluation(BaseModel):
    evaluations: Dict[str, RoundEvaluation]

class Summary(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    overall_impression: str

class FinalReport(BaseModel):
    candidate: Dict[str, str]
    evaluation: Dict[str, RoundEvaluation]
    feedback: Dict[str, str]
    resources: Dict[str, List[ResourceItem]] = Field(default_factory=dict)
    summary: Summary
