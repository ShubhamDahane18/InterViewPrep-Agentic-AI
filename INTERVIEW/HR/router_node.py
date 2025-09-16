# -------------------------
# Router Node
# -------------------------
from typing import Literal
from langgraph.types import Command
from INTERVIEW.HR.state import HRState


def router_node(state: HRState) -> Command[Literal["get_user_intent", "ask_user_what_next", "hr_round"]]:
    """Route control flow to the right node based on interview state."""

    if state.is_qa:
        qa_pair = {
            "question": state.response,   # system's last asked question
            "answer": state.user_input    # candidate's answer
        }
        state.questions_answers.setdefault(state.section_name, []).append(qa_pair) 
    
    if state.get_user_intent:
        return Command(
            goto="get_user_intent" , 
            update={
            "is_qa": False
            }
        )
    
    elif len(state.questions_answers.get(state.section_name, [])) > 0 and len(state.questions_answers.get(state.section_name, [])) % state.limit == 0:
        return Command(
            goto="ask_user_what_next" , 
            update={
            "is_qa": False
            }
        )
    
    else:
        return Command(
            goto="hr_round" , 
            update={
                "is_qa": False
            }
        )