from langgraph.graph import StateGraph , START , END

from INTERVIEW.TECHNICAL.state import TechRoundState
from INTERVIEW.TECHNICAL.router import router_node
from INTERVIEW.TECHNICAL.get_intent import get_user_intent_node
from INTERVIEW.TECHNICAL.ask_next import ask_user_what_next_node
from INTERVIEW.TECHNICAL.tech import tech_round_node

# -------------------------
# Graph Construction
# -------------------------
def tech_graph():
    workflow = StateGraph(TechRoundState)

    workflow.add_node("router" , router_node)
    workflow.add_node("tech_round", tech_round_node) #tech_round_node)
    workflow.add_node("ask_user_what_next", ask_user_what_next_node)
    workflow.add_node("get_user_intent_node", get_user_intent_node)

    workflow.add_edge(START , "router")
    workflow.add_edge("tech_round", END)
    workflow.add_edge("ask_user_what_next", END)
    workflow.add_edge("get_user_intent_node", END)


    return workflow.compile()