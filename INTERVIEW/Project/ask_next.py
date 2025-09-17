from langchain.prompts import ChatPromptTemplate


ask_next_project_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an interviewer wrapping up the discussion of one project in a technical/project round.
Your role is to:
1. Briefly summarize the candidate's responses for this project in a polite, encouraging way.
2. Tell them that the current project discussion is complete.
3. Ask them if they’d like to repeat this project once more, or move to the next project.
Keep the tone professional but warm.
"""),
    ("human", """
### Context
- Project Name: {project_name}
- Questions and Answers from this project:
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

def ask_user_next_project_node(state: ProjectState) -> ProjectState:
    """Use LLM to summarize current project Q&A and ask what candidate wants to do next."""
    
    llm = load_llm()
    chain = ask_next_project_prompt | llm

    # Get QAs for the current project
    current_project = state.resume_project_info[state.current_project_index]
    project_name = current_project["name"]



    # Generate interviewer response
    response = chain.invoke({
        "project_name": project_name,
        "questions_answers": format_prev_qas(state.questions_answers[state.current_project_index])
    })

    # Mark that next step is → classify intent
    state.get_user_intent = True
    return {'get_user_intent': True , 'response':response}