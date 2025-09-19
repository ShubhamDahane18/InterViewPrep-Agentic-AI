from langgraph.graph import StateGraph, START, END
from INTERVIEW.EVALUATION.state import EvaluationState
from INTERVIEW.EVALUATION.nodes import evaluation_node, summary_node, final_report_node

def build_evaluation_graph():
    workflow = StateGraph(EvaluationState)
    workflow.add_node("evaluation_node", evaluation_node)
    workflow.add_node("summary_node", summary_node)
    workflow.add_node("final_report_node", final_report_node)

    workflow.add_edge(START, "evaluation_node")
    workflow.add_edge("evaluation_node", "summary_node")
    workflow.add_edge("summary_node", "final_report_node")
    workflow.add_edge("final_report_node", END)

    return workflow.compile()
