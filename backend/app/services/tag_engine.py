import json

from app.services.llm_service import ask_llm


def generate_tags(text: str):

    prompt = f"""
Generate 3-5 relevant tags.

Return ONLY JSON.

Format:

{{
    "tags": []
}}

Text:
{text}
"""

    try:

        content = ask_llm(prompt)

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        result = json.loads(content)

        return result.get("tags", [])

    except Exception as e:

        print(f"Tag Generation Error: {e}")

        return []