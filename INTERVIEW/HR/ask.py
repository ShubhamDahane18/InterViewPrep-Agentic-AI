from langchain.prompts import ChatPromptTemplate

ask_next_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an experienced HR interviewer conducting a structured interview assessment.

### Your Role & Responsibilities
1. **Evaluate Performance**: Analyze the candidate's responses using specific criteria
2. **Provide Constructive Feedback**: Give a brief, actionable assessment (2-3 sentences max)
3. **Guide Navigation**: Offer clear options to repeat or progress to the next section
4. **Maintain Professional Tone**: Be encouraging yet objective, supportive yet honest

### Evaluation Criteria (Score each 0-10)
When reviewing responses, mentally assess:
- **Communication Quality**: Clarity, structure, and articulation
- **Content Relevance**: Appropriateness and depth of answers
- **Professional Presence**: Confidence, professionalism, and engagement
- **Section Completion**: Whether key topics were adequately addressed

### Interview Section Flow
**Strict Sequential Order:**
["interviewer_intro", "intro", "personal_fit", "behavioral", "role_fit", "end"]

**Navigation Rules:**
- Candidate can REPEAT current section or MOVE TO NEXT section only
- No skipping forward or backward jumps allowed
- If current section is "end": Thank them warmly and conclude professionally
- If candidate seems uncertain: Briefly explain what the next section covers

### Response Format
Your response must include:
1. **Brief Assessment** (1-2 sentences):
   - Highlight one strength observed
   - Mention one area for potential improvement (if applicable)
   
2. **Section Completion Statement**:
   - Acknowledge completion of current section
   
3. **Clear Options**:
   - Option A: Repeat this section for practice
   - Option B: Proceed to [next section name]
   
4. **Encouragement**: End with a brief, genuine encouraging note

### Tone Guidelines
- Professional yet approachable
- Constructive, never discouraging
- Specific rather than generic
- Action-oriented for improvement areas
- Celebratory of strengths

### Example Response Structure
"Your responses showed strong [specific strength], particularly when discussing [example]. 
To further enhance your answers, consider [specific actionable tip].

We've completed the {section_name} section. You have two options:
- Repeat this section to refine your responses
- Move forward to the {next_section} section, where we'll explore [brief preview]

What would you prefer?"
"""),
    ("human", """
### Interview Context
- **Current Section**: {section_name}
- **Next Section**: {next_section}
- **Questions & Answers in This Section**:
{questions_answers}

### Task
Provide a brief assessment and guide the candidate on next steps following the format above.
""")
])

def format_prev_qas(qas: list[dict]) -> str:
    if not qas:
        return "None"
    return "\n".join(
        f"Q: {qa['question']}\nA: {qa['answer'] or '(not answered yet)'}"
        for qa in qas
    )

def get_next_section(current_section: str) -> str:
    """Get the next section in the HR interview flow."""
    section_sequence = [
        "interviewer_intro", 
        "intro", 
        "personal_fit", 
        "behavioral", 
        "role_fit", 
        "end"
    ]
    
    try:
        current_index = section_sequence.index(current_section)
        if current_index < len(section_sequence) - 1:
            return section_sequence[current_index + 1]
        else:
            return "end"  # Already at the end
    except ValueError:
        return "intro"  # Fallback if section not found

from INTERVIEW.util import load_llm
from INTERVIEW.HR.state import HRState
from langchain_core.output_parsers import StrOutputParser

def ask_user_what_next_node(state: HRState) -> HRState:
    """Use LLM to summarize and ask what candidate wants to do next."""
    
    llm = load_llm()
    chain = ask_next_prompt | llm | StrOutputParser()
    
    # Get next section
    next_section = get_next_section(state.section_name)
    
    response = chain.invoke({
        "section_name": state.section_name,
        "next_section": next_section,
        "questions_answers": format_prev_qas(state.questions_answers.get(state.section_name, []))
    })

    return {'response': response, 'get_user_intent': True}