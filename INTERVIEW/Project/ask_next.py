from langchain.prompts import ChatPromptTemplate

ask_next_project_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an interviewer wrapping up the discussion of one project in a technical/project round.

### Your Role
1. Provide a **one-line review** of the candidate’s responses about this project.  
2. Politely state that this project discussion is now complete.  
3. Ask them if they’d like to **repeat this project** or **move to the next one**.  
4. Always keep the tone professional, warm, and encouraging.  

### Project Flow
- The valid sequence of projects comes from the candidate’s project list in order.  
- After finishing one project, the candidate can either:
  - Repeat this project, OR  
  - Proceed to the **next project in sequence**.  
- Never skip ahead or jump backwards outside this sequence.  
- If the current project is the **last one**, thank them and politely close the project discussion round.  
"""),
    ("human", """
### Context
- Candidate Name: {user_name}  
- Current Project: {project_name}  
- Candidate’s Q&A for this project:  
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
from INTERVIEW.Project.state import ProjectState  # <-- your project state model
from langchain_core.output_parsers import StrOutputParser

def ask_user_next_project_node(state: ProjectState) -> ProjectState:
    """Use LLM to summarize current project Q&A and ask what candidate wants to do next."""
    
    llm = load_llm()
    chain = ask_next_project_prompt | llm | StrOutputParser()

    # Get QAs for the current project
    current_project = state.projects[int(state.current_project_index)]
    project_name = current_project["name"]



    # Generate interviewer response
    response = chain.invoke({
        "user_name": state.user_name,
        "project_name": project_name,
        "questions_answers": format_prev_qas(state.questions_answers[int(state.current_project_index)])
    })

    # Mark that next step is → classify intent
    state.get_user_intent = True
    return {'get_user_intent': True , 'response':response}