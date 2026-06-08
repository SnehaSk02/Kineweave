from app.services.llm_service import ask_llm

VALID_INTENTS = [
    "Task",
    "Goal",
    "Idea",
    "Reminder",
    "Note",
    "Project",
    "Meeting",
    "Learning Goal"
]

def detect_intent(text):

    prompt = f"""
You are an intent classification engine.

Classify the user input into exactly one of these categories:

Task
Goal
Idea
Reminder
Note
Project
Meeting
Learning Goal

Return ONLY the category name.

User Input:
{text}
"""

    try:

        intent = ask_llm(prompt).strip()

        if intent not in VALID_INTENTS:
            return "Task"

        return intent

    except Exception as e:

        print(f"Intent Detection Error: {e}")

        return "Task"