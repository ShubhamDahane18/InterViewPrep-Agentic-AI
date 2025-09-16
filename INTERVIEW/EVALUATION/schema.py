from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class QAItem(BaseModel):
    question: str
    answer: str

class RoundQA(BaseModel):
    round_name: str
    qa: List[QAItem]

class RoundEvaluation(BaseModel):
    score: float = Field(..., ge=0, le=10)
    feedback: str
    reasoning: Optional[str] = None
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)

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
