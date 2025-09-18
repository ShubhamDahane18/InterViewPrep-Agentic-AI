from typing import Dict, List, Optional

def qa_to_str(questions_answers: Dict[str, List[Dict[str, Optional[str]]]]) -> str:
    """
    Convert a dict of section -> list of {question, answer} 
    into a human-readable plain string.
    """
    lines = []
    for section, qa_list in questions_answers.items():
        lines.append(f"Section: {section}")
        for idx, qa in enumerate(qa_list, start=1):
            question = qa.get("question") or ""
            answer = qa.get("answer") or ""
            lines.append(f"  Q{idx}: {question}")
            lines.append(f"  A{idx}: {answer}")
    return "\n".join(lines)