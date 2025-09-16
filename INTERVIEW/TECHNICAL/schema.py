from typing import Optional
from pydantic import BaseModel, Field

class QAEntry(BaseModel):
    """Represents a single question-answer pair."""
    question: str = Field(description="A single, unique interview question.")
    answer: Optional[str] = None
