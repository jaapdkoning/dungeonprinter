from openai import OpenAI
import os
from datetime import datetime
from api.themes import themes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = "You are a creative and evocative old-school RPG dungeon master."

def generate_room_with_llm(theme="Undead Crypt", model="gpt-3.5-turbo"):
    theme_data = themes.get(theme, {})
    theme_description = theme_data.get("description", "")
    encounters = ", ".join(theme_data.get("encounter_table", []))
    loot = ", ".join(theme_data.get("loot_table", []))

    user_prompt = f"""
Generate a single dungeon room in the theme: **{theme}**
Theme description: {theme_description}
Here are some example encounters: {encounters}
Here is possible loot: {loot}
Format as markdown.
Limit to 100 words.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,
        max_tokens=250,
    )

    content = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    return content, tokens_used