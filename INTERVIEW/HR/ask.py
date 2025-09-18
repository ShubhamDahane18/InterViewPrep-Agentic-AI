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
- Current Round: {section_name}
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


from INTERVIEW.util import load_llm
from INTERVIEW.HR.state import HRState
from langchain.output_parsers import StrOutputParser
def ask_user_what_next_node(state: HRState) -> HRState:
    """Use LLM to summarize and ask what candidate wants to do next."""

    llm = load_llm()
    chain = ask_next_prompt | llm | StrOutputParser()
    response = chain.invoke({
        "section_name": state.section_name,
        "questions_answers": format_prev_qas(state.questions_answers.get(state.section_name, []))
    })

    return {'response':response ,'get_user_intent': True}