import json

from app.services.llm_service import ask_llm


def analyze_capture(text: str):

    prompt = f"""
You are KineWeave AI.

The user may provide:
- One task
- Multiple tasks
- Multiple goals
- Multiple reminders
- Multiple ideas

The tasks may be separated by:
- and
- also
- then
- commas
- punctuation
- natural speech

Your job is to:

1. Split independent thoughts into separate captures.
2. Classify each capture.
3. Extract entities.
4. Assign priority.
5. Generate tags.
6. Identify deadline.

Return ONLY valid JSON.

IMPORTANT RULES FOR SPLITTING:
- DO NOT split sentences connected by "so", "because", "therefore", "but" or "also" unless they clearly introduce a completely new, unrelated topic.
- If a sentence starts with a lowercase letter (like "so"), it is likely a continuation of the previous sentence. Merge it with the previous capture.
- Treat "and" as a separator ONLY if it connects two distinct subjects (e.g., "Buy milk and call mom"), not if it connects details (e.g., "Submit project and prepare for it").

Schema:

{{
    "captures": [
        {{
            "text": "",
            "intent": "",
            "priority": "",
            "deadline": "",
            "entities": {{
                "person": [],
                "date": [],
                "time": [],
                "organization": [],
                "topic": []
            }},
            "tags": []
        }}
    ]
}}

Intent Types:

- Task
- Reminder
- Goal
- Learning Goal
- Idea
- Project
- Meeting
- Note

Priority Rules:

High:
- deadlines
- interviews
- meetings
- appointments
- reminders with dates
- reminders with time

Medium:
- tasks
- goals
- learning goals
- projects

Low:
- notes
- ideas

Example:

Input:
Learn LangChain and buy groceries tomorrow, call Rahul at 5 PM

Output:
{{
    "captures": [
        {{
            "text": "Learn LangChain",
            "intent": "Learning Goal",
            "priority": "Medium",
            "entities": {{
                "person": [],
                "date": [],
                "time": [],
                "organization": [],
                "topic": ["LangChain"]
            }},
            "tags": ["AI","Learning","LangChain"]
        }},
        {{
            "text": "Buy groceries tomorrow",
            "intent": "Reminder",
            "priority": "High",
            "entities": {{
                "person": [],
                "date": ["tomorrow"],
                "deadline": "tomorrow",
                "time": [],
                "organization": [],
                "topic": ["groceries"]
            }},
            "tags": ["Shopping","Home","Reminder"]
        }},
        {{
            "text": "Call Rahul at 5 PM",
            "intent": "Reminder",
            "priority": "High",
            "entities": {{
                "person": ["Rahul"],
                "date": [],
                "time": ["5 PM"],
                "organization": [],
                "topic": []
            }},
            "tags": ["Call","Reminder","Follow-up"]
        }}
    ]
}}

Analyze:

{text}
"""

    try:

        content = ask_llm(prompt)

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        result = json.loads(content)

        if "captures" not in result:

            return {
                "captures": [
                    {
                        "text": text,
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
                ]
            }

        return result

    except Exception as e:

        print("Analyzer Error:", e)

        return {
            "captures": [
                {
                    "text": text,
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
            ]
        }