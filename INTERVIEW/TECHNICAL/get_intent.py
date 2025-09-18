from langchain.prompts import ChatPromptTemplate

intent_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intent classifier for an Technical interview flow. 
Your job is to:
1. Detect if the candidate wants to REPEAT the current section or move to the NEXT section.  
2. Handle the special "interviewer_intro" and "end" sections.  
3. Return a structured output following the given schema.

### Rules:
- The valid sequence of sections is: ["interviewer_intro", "Object Oriented Programming", "Database Management", "Data Structures & Algo", "Computer Networking", "skills","end"].
- If current section is "interviewer_intro":
  - If candidate says they are ready → set section_name="OOPS".
  - If not ready → keep section_name="interviewer_intro" and in response politely ask them to say "ready" when they are prepared.
- If current section is "end":
  - Always keep section_name="end".
  - Response must politely thank the candidate and suggest they can move forward or request an analysis report.  
  - Example: "✅ Thank you! Your Technical interview round is now complete. You may proceed to the next stage or request an analysis report for this round."
- If enforce_limit=true → ALWAYS move to the next section regardless of what the candidate says.  
  - If already in "skills", move to "end".
- If enforce_limit=false → normal behavior: candidate can choose repeat or next.  
- Never skip a section.  

### Output Schema:
- section_name → must be one of the valid sections.  
- response → a polite Technical-style confirmation message to the candidate.  
"""),
    ("human", """
Current section: {section_name}
User said: {user_input}
Enforce limit: {enforce_limit}
""")
])

from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    section_name: str = Field(
        ...,
        description="The section the interview should continue with. Must be one of:['interviewer_intro', 'Object Oriented Programming', 'Database Management', 'Data Structures & Algo', 'Computer Networking', 'skills','end']."
    )
    response: str = Field(
        ...,
        description="A polite Technical-style confirmation message based on the user’s intent and the current section."
    )

from typing import Literal
from langgraph.graph import END
from langgraph.types import Command
from INTERVIEW.util import load_llm
from INTERVIEW.TECHNICAL.state import TechRoundState

def get_user_intent_node(state: TechRoundState) -> Command[Literal["tech_round", END]]:
    # 1. Decide enforce_limit dynamically
    enforce_limit = len(state.questions_answers.get(state.section_name, [])) >= state.limit * 2

    # 2. Run intent classifier
    llm = load_llm()
    intent_chain = intent_prompt | llm.with_structured_output(IntentSchema)
    intent: IntentSchema = intent_chain.invoke({
        "section_name": state.section_name,
        "user_input": state.user_input,
        "enforce_limit": enforce_limit
    })

    # 3. Handle intro + end explicitly
    if intent.section_name in ["interviewer_intro", "end"]:
        return Command(
            goto=END,
            update={
                "section_name": intent.section_name,
                "response": intent.response
            }
        )

    # 4. Otherwise → go to HR round
    return Command(
        goto="tech_round",
        update={
            "section_name": intent.section_name,
            "response": intent.response
        }
    )