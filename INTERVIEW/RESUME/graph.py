from INTERVIEW.RESUME.state import ResumeAgentState
from INTERVIEW.RESUME.extract_resume_data import extract_resume_data
from INTERVIEW.RESUME.check_links import check_links_and_alert
from langgraph.graph import StateGraph , START , END

def build_graph():

    builder = StateGraph(ResumeAgentState)

    builder.add_node("extract_resume_data" , extract_resume_data)
    builder.add_node("check_links_and_alert" , check_links_and_alert)

    builder.add_edge(START , "extract_resume_data")
    builder.add_edge("extract_resume_data" , "check_links_and_alert")
    builder.add_edge("check_links_and_alert" , END)

    graph = builder.compile()
    return graph

