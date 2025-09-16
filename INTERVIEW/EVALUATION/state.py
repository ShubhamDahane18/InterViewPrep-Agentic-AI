from typing import TypedDict, List, Dict

class QAItem(TypedDict):
    question: str
    answer: str

class RoundQA(TypedDict):
    round_name: str  # "Tech", "HR", "Project"
    qa: List[QAItem]

class RoundEvaluation(TypedDict, total=False):
    score: float
    feedback: str
    reasoning: str
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    examples: List[str]

class ResourceItem(TypedDict):
    name: str  # simplified resource

class EvaluationState(TypedDict, total=False):
    candidate_name: str
    candidate_email: str
    company_name: str
    rounds: List[RoundQA]
    evaluation: Dict[str, RoundEvaluation]
    feedback: Dict[str, str]
    resources: Dict[str, List[ResourceItem]]
    summary: str
    final_report: dict
