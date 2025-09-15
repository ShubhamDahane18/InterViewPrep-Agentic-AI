from langgraph.graph import StateGraph , START , END

from INTERVIEW.HR.state import HRState
from INTERVIEW.HR.router_node import router_node
from INTERVIEW.HR.get_intent import get_user_intent_node
from INTERVIEW.HR.ask import ask_user_what_next_node
from INTERVIEW.HR.hr import hr_round_node

# -------------------------
# Graph Construction
# -------------------------
workflow = StateGraph(HRState)

workflow.add_node("router" , router_node)
workflow.add_node("hr_round", hr_round_node)
workflow.add_node("ask_user_what_next", ask_user_what_next_node)
workflow.add_node("get_user_intent", get_user_intent_node)

workflow.add_edge(START , "router")
workflow.add_edge("hr_round", END)
workflow.add_edge("ask_user_what_next", END)
workflow.add_edge("get_user_intent", END)


app = workflow.compile()
