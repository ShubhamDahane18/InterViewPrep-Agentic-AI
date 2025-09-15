from typing import TypedDict, List, Dict

class QAItem(TypedDict):
    question: str
    answer: str

class RoundQA(TypedDict):
    round_name: str  # "Tech", "HR", "Project"
    qa: List[QAItem]

class EvaluationState(TypedDict, total=False):
    candidate_name: str
    candidate_email: str
    company_name: str
    rounds: List[RoundQA]
    evaluation: Dict[str, dict]
    feedback: Dict[str, str]
    resources: Dict[str, List[str]]
    summary: str
    final_report: dict
