from langchain.prompts import ChatPromptTemplate

intent_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent intent classifier for a structured HR interview system.

### Primary Responsibilities
1. **Accurately detect** candidate intent: REPEAT current section vs. PROCEED to next section
2. **Enforce interview flow** according to the strict sequential structure
3. **Handle special sections** (interviewer_intro, end) with appropriate logic
4. **Provide clear, professional responses** that guide the candidate

### Interview Section Sequence (Strict Order)
["interviewer_intro", "intro", "personal_fit", "behavioral", "role_fit", "end"]

### Classification Logic

**A. INTERVIEWER_INTRO Section:**
- **Ready signals** (proceed): "ready", "yes", "let's start", "I'm ready", "sure", "okay", "begin", "start"
- **Not ready signals** (stay): "wait", "not yet", "give me a moment", "no", "hold on"
- **Action:**
  - If ready → section_name="intro"
  - If not ready → section_name="interviewer_intro"
  - Response should be warm and welcoming

**B. END Section:**
- **Always** keep section_name="end"
- **Response must include:**
  - Congratulations/thank you
  - Confirmation that HR round is complete
  - Clear next steps: proceed to Technical/Project rounds OR request analysis report
- **Example response:** "✅ Congratulations on completing the HR interview round! You've done well. You can now:
  • Proceed to the Technical Interview round
  • Proceed to the Project Interview round  
  • Request a detailed analysis report of your HR interview performance
  What would you like to do next?"

**C. ENFORCE_LIMIT=True (Question Limit Reached):**
- **Override user intent** → Always move to next section
- **Action:**
  - Determine next section in sequence
  - If current is "role_fit" → next is "end"
  - Provide encouraging transition message
- **Response tone:** Positive acknowledgment that section is complete, smooth transition
- **Example:** "Great work! We've covered all the key areas for this section. Let's move forward to [next_section]."

**D. ENFORCE_LIMIT=False (Normal Flow):**
Analyze user input for intent signals:

**REPEAT Signals:**
- Direct: "repeat", "again", "retry", "redo", "practice more", "do it again"
- Indirect: "I want to improve", "can we try again", "not satisfied", "one more time"
- Uncertain: "I'm not sure", "maybe again", "can I practice"

**NEXT/PROCEED Signals:**
- Direct: "next", "proceed", "continue", "move on", "forward", "done"
- Indirect: "I'm ready for next", "let's move ahead", "finished", "complete"
- Confident: "yes", "okay", "sure" (when asked if ready to proceed)

**Ambiguous Input Handling:**
- If unclear → Ask for clarification
- Provide explicit options: "Would you like to (A) repeat this section or (B) move to [next_section]?"

### Output Schema Requirements

**section_name:** 
- Must be exactly one of: ["interviewer_intro", "intro", "personal_fit", "behavioral", "role_fit", "end"]
- Must follow sequential order (never skip)

**response:**
- Professional, clear, and encouraging
- Context-aware (acknowledge their choice)
- Action-oriented (tell them what happens next)
- 1-3 sentences for normal flow
- Include specific section names when transitioning

### Response Quality Guidelines
✓ Be specific about what section they're entering/repeating
✓ Use positive, encouraging language
✓ Confirm their choice explicitly
✓ Preview what to expect in next section (when proceeding)
✗ Don't be vague or generic
✗ Don't use overly casual language
✗ Don't apologize unnecessarily

### Example Responses by Scenario

**Scenario 1: User wants to repeat**
"Absolutely! Let's go through the {section_name} section again. This is great practice. Ready when you are."

**Scenario 2: User wants to proceed**
"Excellent! Moving forward to the {next_section} section. Here, we'll explore [brief preview]. Let's begin."

**Scenario 3: Enforce limit triggered**
"You've completed the {section_name} section thoroughly! Let's move ahead to the {next_section} section to continue your interview."

**Scenario 4: Ambiguous input**
"I want to make sure I understand correctly. Would you like to:
A) Repeat the {section_name} section for more practice
B) Proceed to the {next_section} section
Please let me know your preference."
"""),
    ("human", """
### Current Interview State
- **Current Section**: {section_name}
- **Next Section in Sequence**: {next_section}
- **Question Limit Reached**: {enforce_limit}
- **Candidate's Input**: "{user_input}"

### Task
Analyze the candidate's intent and determine:
1. Which section they should be in next (section_name)
2. An appropriate professional response (response)

Return your classification following the output schema.
""")
])

from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    section_name: str = Field(
        ...,
        description="The section the interview should continue with. Must be one of: ['interviewer_intro','intro','personal_fit','behavioral','role_fit','end']."
    )
    response: str = Field(
        ...,
        description="A polite HR-style confirmation message based on the user's intent and the current section."
    )

from typing import Literal
from langgraph.graph import END
from langgraph.types import Command
from INTERVIEW.util import load_llm
from INTERVIEW.HR.state import HRState

def get_next_hr_section(current_section: str) -> str:
    """Get the next section in HR interview sequence."""
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

def get_user_intent_node(state: HRState) -> Command[Literal["hr_round", END]]:
    # 1. Decide enforce_limit dynamically
    enforce_limit = len(state.questions_answers.get(state.section_name, [])) >= state.limit * 2

    # 2. Get next section
    next_section = get_next_hr_section(state.section_name)

    # 3. Run intent classifier
    llm = load_llm()
    intent_chain = intent_prompt | llm.with_structured_output(IntentSchema)
    intent: IntentSchema = intent_chain.invoke({
        "section_name": state.section_name,
        "next_section": next_section,  # ← ADDED
        "user_input": state.user_input,
        "enforce_limit": enforce_limit
    })

    # 4. Handle intro + end explicitly
    if intent.section_name in ["interviewer_intro", "end"]:
        return Command(
            goto=END,
            update={
                "section_name": intent.section_name,
                "response": intent.response
            }
        )

    # 5. Otherwise → go to HR round
    return Command(
        goto="hr_round",
        update={
            "section_name": intent.section_name,
            "response": intent.response
        }
    )