# graph.py
from functools import partial
from langgraph.graph import StateGraph, START, END
from INTERVIEW.TECHNICAL.state import TechRoundState
from INTERVIEW.TECHNICAL.nodes import (
    generate_qa_node,
    core_decision_node,
    tech_decision_node,
)

def core_progress(state: TechRoundState) -> str:
    """Continue asking core questions until baseline is done, else decision."""
    per = state.get("questions_per_topic", 2)
    for subject in state["core_subjects"]:
        if state.get("qa_counts", {}).get(subject, 0) < per:
            return "core_qa"
    return "core_decision"

def tech_progress(state: TechRoundState) -> str:
    """Continue asking tech questions until baseline is done, else decision."""
    per = state.get("questions_per_topic", 2)
    all_skills = [skill for cat in state["skills"].values() for skill in cat]
    for skill in all_skills:
        if state.get("qa_counts", {}).get(skill, 0) < per:
            return "tech_qa"
    return "tech_decision"

def build_graph():
    workflow = StateGraph(TechRoundState)

    workflow.add_node("core_qa", partial(generate_qa_node, round_type="core"))
    workflow.add_node("tech_qa", partial(generate_qa_node, round_type="tech"))
    workflow.add_node("core_decision", core_decision_node)
    workflow.add_node("tech_decision", tech_decision_node)


    workflow.add_edge(START, "core_qa")

    workflow.add_conditional_edges("core_qa", core_progress)
    workflow.add_conditional_edges(
        "core_decision",
        lambda s: s.get("decision", {}).get("core", "next"),
        {"continue": "core_qa", "next": "tech_qa"}
    )

    workflow.add_conditional_edges("tech_qa", tech_progress)
    workflow.add_conditional_edges(
        "tech_decision",
        lambda s: s.get("decision", {}).get("technical", "next"),
        {"continue": "tech_qa", "next": END}
    )
    return workflow.compile()
