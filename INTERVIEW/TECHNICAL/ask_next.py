from langchain.prompts import ChatPromptTemplate

ask_next_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a **Technical Interviewer** wrapping up a round of the technical interview.  

### Your Role
1. Begin your response by **greeting the candidate by name ({candidate_name})**.  
   Example: "Thank you, Pranav, for completing this round."  
2. Briefly summarize the candidate's responses in a polite, encouraging way.  
3. Tell them the current round is complete.  
4. Ask them if they’d like to repeat this round once more, or move to the next one.  

Keep the tone professional but warm.  
"""),
    ("human", """
### Context
- Candidate Name: {candidate_name}
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
from INTERVIEW.TECHNICAL.state import TechRoundState
from langchain_core.output_parsers import StrOutputParser
def ask_user_what_next_node(state: TechRoundState) -> TechRoundState:
    """Use LLM to summarize and ask what candidate wants to do next."""

    llm = load_llm()
    chain = ask_next_prompt | llm | StrOutputParser()
    response = chain.invoke({
        "section_name": state.section_name,
        "questions_answers": format_prev_qas(state.questions_answers.get(state.section_name, []))
    })

    return {'response':response ,'get_user_intent': True}

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in qas
    )


from INTERVIEW.util import load_llm
from INTERVIEW.TECHNICAL.state import TechRoundState
from langchain_core.output_parsers import StrOutputParser
def ask_user_what_next_node(state: TechRoundState) -> TechRoundState:
    """Use LLM to summarize and ask what candidate wants to do next."""

    llm = load_llm()
    chain = ask_next_prompt | llm | StrOutputParser()
    response = chain.invoke({
        "candidate_name":state.candidate_name,
        "section_name": state.section_name,
        "questions_answers": format_prev_qas(state.questions_answers.get(state.section_name, []))
    })

    return {'response':response ,'get_user_intent': True}