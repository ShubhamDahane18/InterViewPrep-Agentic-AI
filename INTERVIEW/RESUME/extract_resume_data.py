from INTERVIEW.RESUME.schema import ExtractResumeData
from INTERVIEW.RESUME.state import ResumeAgentState
from INTERVIEW.util import load_llm


def extract_resume_data(state: ResumeAgentState) -> ResumeAgentState:
    try:
        # Load the structured-output LLM with the expected schema
        llm = load_llm().with_structured_output(ExtractResumeData)
        
        # Extract inputs from state
        full_text = state.get('full_text' , '')
        links = state.get('links' , [])

        # Combine text and links into a single input string
        resume_input = full_text + "\n\nLinks:\n" + "\n".join(
        f"Page: {link['page']}, Text: {link['text']}, URL: {link['url']}" for link in links)

        # Invoke the LLM to extract structured data
        extracted_data = llm.invoke(resume_input)

        # Return the updated state
        return extracted_data.model_dump()

    except Exception as e:
        raise RuntimeError(f"Failed to extract resume data: {e}")