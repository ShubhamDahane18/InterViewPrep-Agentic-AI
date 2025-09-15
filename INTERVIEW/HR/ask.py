from langchain.prompts import ChatPromptTemplate

ask_next_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an HR interviewer wrapping up a round of an interview.
Your role is to:
1. Briefly summarize the candidate's responses in a polite, encouraging way.
2. Tell them the current round is complete.
3. Ask them if they’d like to repeat this round once more, or move to the next one.
Keep the tone professional but warm.
"""),
    ("human", """
### Context
- Current Round: {round_name}
- Questions and Answers from this round:
{questions_answers}
""")
])

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in qas
    )


from BACKEND.INTERVIEW.util import load_llm
from BACKEND.INTERVIEW.HR.state import HRState

def ask_user_what_next_node(state: HRState) -> HRState:
    """Use LLM to summarize and ask what candidate wants to do next."""

    llm = load_llm()
    chain = ask_next_prompt | llm
    state.response = chain.invoke({
        "round_name": state.round_name,
        "questions_answers": format_prev_qas(state.questions_answers.get(state.round_name, []))
    })

    # Next step → classify user intent from their reply
    state.get_user_intent = True
    return state