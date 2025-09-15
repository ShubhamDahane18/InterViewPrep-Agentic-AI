# io_utils.py
"""
Interaction layer abstraction for Interview AI.
Current: console input/output
Future: can be swapped for frontend API or voice STT/TTS.
"""

def get_user_response(prompt: str) -> str:
    """Fetch candidate's response."""
    return input(prompt)

def present_to_user(message: str):
    """Display interviewer message."""
    print(message)
