from langgraph.graph import StateGraph , START , END

from INTERVIEW.Project.state import ProjectState
from INTERVIEW.Project.get_intent import get_project_intent_node
from INTERVIEW.Project.ask_next import ask_user_next_project_node
from INTERVIEW.Project.project import project_round_node
from INTERVIEW.Project.router_node import router_node

# -------------------------
# Graph Construction
# -------------------------

def Project_graph():
    workflow = StateGraph(ProjectState)

    workflow.add_node("router" , router_node)
    workflow.add_node("hr_round", project_round_node)
    workflow.add_node("ask_user_what_next", ask_user_next_project_node)
    workflow.add_node("get_user_intent", get_project_intent_node)

    workflow.add_edge(START , "router")
    workflow.add_edge("hr_round", END)
    workflow.add_edge("ask_user_what_next", END)
    workflow.add_edge("get_user_intent", END)


    return workflow.compile()
