# -------------------------
# Router Node
# -------------------------
from typing import Literal
from langgraph.types import Command
from INTERVIEW.TECHNICAL.state import TechRoundState


def router_node(state: TechRoundState) -> Command[Literal["get_user_intent_node", "ask_user_what_next", "tech_round"]]:
    """Route control flow to the right node based on interview state."""

    updated_qa = state.questions_answers.copy()

    if state.is_qa:
        qa_pair = {
            "question": state.response,   # system's last asked question
            "answer": state.user_input    # candidate's answer
        }
        updated_qa.setdefault(state.section_name, []).append(qa_pair)

    if state.get_user_intent:
        return Command(
            goto="get_user_intent_node",
            update={
                "is_qa": False,
                "questions_answers": updated_qa
            }
        )

    elif len(updated_qa.get(state.section_name, [])) > 0 and len(updated_qa.get(state.section_name, [])) % state.limit == 0:
        return Command(
            goto="ask_user_what_next",
            update={
                "is_qa": False,
                "questions_answers": updated_qa
            }
        )

    else:
        return Command(
            goto="tech_round",
            update={
                "is_qa": False,
                "questions_answers": updated_qa
            }
        )