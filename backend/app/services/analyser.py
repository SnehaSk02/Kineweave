import json

from app.services.llm_service import ask_llm


def analyze_capture(text: str):

    prompt = f"""
You are KineWeave, an AI-powered productivity assistant.

Analyze the user's input and return ONLY valid JSON.
The user might enter multiple distinct thoughts in one sentence (e.g., "Buy milk and call mom").
You must split these into separate items.
JSON Schema:

{{
    "intent": "",
    "priority": "",
    "entities": {{
        "person": [],
        "date": [],
        "time": [],
        "organization": [],
        "topic": []
    }},
    "tags": []
}}

Intent Definitions:

- Task:
  A specific action that needs to be completed.
  Example:
  "Finish project report"

- Reminder:
  Something that must happen at a particular date or time.
  Example:
  "Call Rahul tomorrow at 5 PM"

- Goal:
  A long-term objective.
  Example:
  "Become a Data Scientist"

- Learning Goal:
  Something the user wants to learn or study.
  Example:
  "Learn LangChain"

- Idea:
  A thought, concept, or potential opportunity.
  Example:
  "Build an AI startup"

- Project:
  A collection of related tasks with a larger outcome.
  Example:
  "Create a personal portfolio website"

- Meeting:
  Any discussion, appointment, or scheduled interaction.
  Example:
  "Meeting with manager at 3 PM"

- Note:
  Information being stored without requiring action.
  Example:
  "LangChain supports RAG pipelines"

Priority Rules:
- High:
  Contains deadlines, dates, times, urgent actions,
  interviews, exams, meetings, appointments,
  follow-ups, or important commitments.
- Medium:
  Normal tasks, goals, and learning activities.
- Low:
  General notes, ideas, and observations.

Entity Extraction:
Extract:
- person
- date
- time
- organization
- topic

Tag Generation Rules:
- Generate 3-5 meaningful tags.
- Use concise tags.
- Never return empty tags if a topic can be inferred.
- Tags should help future search and retrieval.

Examples:
Input:
Call Rahul tomorrow at 5 PM regarding internship and also buy groceries on the way home

Output:
{{
    "items": [
        {{
            "description": "Call Rahul regarding internship",
            "intent": "Reminder",
            "priority": "High",
            "entities": {{
                "person": ["Rahul"],
                "date": ["tomorrow"],
                "time": ["5 PM"],
                "organization": [],
                "topic": ["internship"]
            }},
            "tags": ["Internship", "Communication", "Follow-up"]
        }},
        {{
            "description": "Buy groceries",
            "intent": "Task",
            "priority": "Low",
            "entities": {{
                "person": [],
                "date": [],
                "time": [],
                "organization": [],
                "topic": ["groceries"]
            }},
            "tags": ["Shopping", "Errands", "Home"]
        }}
    ]
}}

Input:
Need to learn LangChain before placements
Output:
{{
    "intent": "Learning Goal",
    "priority": "Medium",
    "entities": {{
        "person": [],
        "date": [],
        "time": [],
        "organization": [],
        "topic": ["LangChain", "placements"]
    }},
    "tags": ["AI", "Learning", "Career", "LangChain"]
}}
Return ONLY valid JSON.
Text:
{text}
"""

    try:

        content = ask_llm(prompt)

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        result = json.loads(content)

        return result

    except Exception as e:

        print(f"AI Analyzer Error: {e}")

        return {
            "intent": "Task",
            "priority": "Medium",
            "entities": {
                "person": [],
                "date": [],
                "time": [],
                "organization": [],
                "topic": []
            },
            "tags": []
        }