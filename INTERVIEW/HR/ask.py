from langchain.prompts import ChatPromptTemplate

ask_next_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an HR interviewer wrapping up a section of an interview.

### Your Role
1. Provide a **one-line review** of the candidate’s responses (not a long summary).
2. Tell them politely that this section is now complete.
3. Ask if they’d like to **repeat this round** or **move to the next one**.
4. Always keep the tone professional, warm, and encouraging.

### Interview Section Flow
The valid sequence of sections is strictly:
["interviewer_intro", "intro", "personal_fit", "behavioral", "role_fit", "end"]

- After finishing one section, the candidate can either repeat it or proceed to the next one in this sequence.
- Never skip ahead or jump backwards outside this sequence.
- If the current section is "end", you should only thank them and politely close the interview.
"""),
    ("human", """
### Context
- Current Section: {section_name}
- Candidate’s Q&A in this section:
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
from langchain_core.output_parsers import StrOutputParser
def ask_user_what_next_node(state: HRState) -> HRState:
    """Use LLM to summarize and ask what candidate wants to do next."""

    llm = load_llm()
    chain = ask_next_prompt | llm | StrOutputParser()
    response = chain.invoke({
        "section_name": state.section_name,
        "questions_answers": format_prev_qas(state.questions_answers.get(state.section_name, []))
    })

    return {'response':response ,'get_user_intent': True}