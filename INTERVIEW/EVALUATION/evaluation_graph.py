from langgraph.graph import StateGraph, START, END
from state import EvaluationState
from nodes import evaluation_node, feedback_node, resource_node, summary_node, final_report_node

def build_evaluation_graph():
    workflow = StateGraph(EvaluationState)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("feedback", feedback_node)
    workflow.add_node("resources", resource_node)
    workflow.add_node("summary", summary_node)
    workflow.add_node("final_report", final_report_node)

    workflow.add_edge(START, "evaluation")
    workflow.add_edge("evaluation", "feedback")
    workflow.add_edge("feedback", "resources")
    workflow.add_edge("resources", "summary")
    workflow.add_edge("summary", "final_report")
    workflow.add_edge("final_report", END)

    return workflow.compile()
