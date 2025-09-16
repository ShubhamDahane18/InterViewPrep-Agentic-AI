from langchain.prompts import ChatPromptTemplate

project_intent_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intent classifier for a Project Interview flow. 
Your job is to:
1. Detect if the candidate wants to REPEAT the current project, move to the NEXT project, or conclude the round.  
2. Handle the special "interviewer_intro" and "end" sections.  
3. Return a structured output following the given schema.

### Rules:
- The valid sequence of sections is: ["interviewer_intro", "project_loop", "end"].
- If current section is "interviewer_intro":
  - If candidate says they are ready → section_name="project_loop" and delta=1.
  - Otherwise → stay in "interviewer_intro" and delta=0.
- If current section is "project_loop":
  - If candidate says "next" → move to the next project and delta=1.
  - If candidate says "repeat" → stay in "project_loop" and delta=0.
  - If last project is done → move to "end" and delta=1.
- If current section is "end":
  - Always stay in "end" and delta=0.
- If enforce_limit=true → ALWAYS set delta=1 regardless of user input.
- Never skip a project or section.  

### Output Schema:
- section_name → must be one of: ['interviewer_intro','project_loop','end'].
- response → polite confirmation message for the candidate.
- delta → 1 if moving forward (next project / start project_loop / enforce_limit), 0 otherwise.
"""),
    ("human", """
Current section: {section_name}
Current project index: {project_index}
Total projects: {total_projects}
User said: {user_input}
Enforce limit: {enforce_limit}
""")
])


from pydantic import BaseModel, Field

class ProjectIntentSchema(BaseModel):
    section_name: str = Field(
        ...,
        description="The next section of the project interview. Must be one of: ['interviewer_intro','project_loop','end']."
    )
    response: str = Field(
        ...,
        description="Polite confirmation message for the candidate."
    )
    delta: int = Field(
        ...,
        description="1 = move forward (next project / start project_loop / enforce_limit), 0 = stay in current section."
    )

from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from INTERVIEW.util import load_llm
from INTERVIEW.PROJECT.state import ProjectState  # <-- your project state model

def get_project_intent_node(state: ProjectState) -> Command[Literal["project_round", END]]:
    # 1. Enforce limit if too many QAs in this project
    enforce_limit = len(state.questions_answers) >= 10

    # 2. Run intent classifier
    llm = load_llm()
    intent_chain = project_intent_prompt | llm.with_structured_output(ProjectIntentSchema)
    intent: ProjectIntentSchema = intent_chain.invoke({
        "section_name": state.section_name,
        "project_index": state.current_project_index,
        "total_projects": len(state.resume_project_info or []),
        "user_input": state.user_input,
        "enforce_limit": enforce_limit
    })

    # 3. Handle end explicitly
    if intent.section_name == "end":
        return Command(
            goto=END,
            update={
                "section_name": intent.section_name,
                "response": intent.response
            }
        )

    # 4. Otherwise → go back to project_round loop
    return Command(
        goto="project_round",
        update={
            "section_name": intent.section_name,
            "response": intent.response
        }
    )