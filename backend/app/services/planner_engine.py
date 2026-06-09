import json

from app.services.llm_service import ask_llm


def generate_action_plan(goal: str):

    prompt = f"""
You are a productivity planning assistant.
Convert the user's goal into a step-by-step action plan.
Return ONLY valid JSON.
Format:
{{
    "goal": "{goal}",
    "steps": [
        {{
            "title": "Step Title",
            "description": "Step Description"
        }}
    ]
}}
Goal:
{goal}
"""

    try:

        content = ask_llm(prompt)

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        result = json.loads(content)

        return result.get("steps", [])

    except Exception as e:

        print(f"Planner Error: {e}")

        return {
            "goal": goal,
            "steps": []
        } 