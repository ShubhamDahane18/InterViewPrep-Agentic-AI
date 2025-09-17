# -------------------------
# Router Node
# -------------------------
from typing import Literal
from langgraph.types import Command
from INTERVIEW.Project.state import ProjectState


def router_node(state: ProjectState) -> Command[Literal["get_user_intent", "ask_user_what_next", "project_round"]]:
    """Route control flow to the right node based on interview state."""

    updated_qa = state.questions_answers.copy()

    if state.is_project_qa:
        qa_pair = {
            "question": state.response,   # system's last asked question
            "answer": state.user_input    # candidate's answer
        }
        updated_qa.setdefault(state.current_project_index, []).append(qa_pair)


    if state.get_user_intent:
        return Command(
            goto="get_user_intent" , 
            update={
            "is_project_qa": False , 
            "questions_answers": updated_qa
            }
        )
    
    elif len(updated_qa.get(state.current_project_index, [])) > 0 and len(updated_qa.get(state.current_project_index, [])) % state.limit == 0:
        return Command(
            goto="ask_user_what_next" , 
            update={
            "is_project_qa": False , 
            "questions_answers": updated_qa
            }
        )
    
    else:
        return Command(
            goto="project_round" , 
            update={
                "is_project_qa": False , 
                "questions_answers": updated_qa
            }
        )