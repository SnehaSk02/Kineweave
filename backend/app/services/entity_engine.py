import json

from app.services.llm_service import ask_llm


def extract_entities(text: str):

    prompt = f"""
You are an entity extraction system.

Extract entities from the text.

Return ONLY valid JSON.

Schema:

{{
    "person": [],
    "date": [],
    "time": [],
    "organization": [],
    "topic": []
}}

Text:
{text}
"""
    try:

        content = ask_llm(prompt)

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        entities = json.loads(content)

        return entities

    except Exception as e:

        print(f"Entity Extraction Error: {e}")

        return {
            "person": [],
            "date": [],
            "time": [],
            "organization": [],
            "topic": []
        }