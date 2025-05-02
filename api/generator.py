from openai import OpenAI
import os
from datetime import datetime
from api.themes import themes
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = "You are a creative and evocative old-school RPG dungeon master."

def generate_room_with_llm(theme="Undead Crypt", model="gpt-3.5-turbo"):
    theme_data = themes.get(theme, {})
    theme_description = theme_data.get("description", "")

    user_prompt = f"""
Generate a single unique dungeon room based on the theme: {theme}

Theme description:
{theme_description}

Invent a room name, one thematic encounter, and one piece of loot. Do not reuse anything from earlier outputs.

Output format in markdown:
## Room Name

<Short description of the room>

**Encounter:** <Creature, trap, or hazard>

**Loot:** <Interesting treasure or item>

Keep the tone in the style of old-school fantasy. Use at most 150 words.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.0,
        max_tokens=300,
    )

    content = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    return content, tokens_used

def generate_encounters_with_llm(theme="Unknown Theme", model="gpt-3.5-turbo"):
    user_prompt = f"""
Generate 4 unique fantasy RPG encounters for the theme: {theme}.

Each encounter must be classified as one of:
- combat
- social
- puzzle

For each encounter, output:
- title (one line)
- type (combat / social / puzzle)
- description (2–4 sentences)

Respond in JSON as an array of objects with: title, type, description.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.0,
        max_tokens=500,
    )

    content = response.choices[0].message.content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = [{"title": "Parse Error", "type": "unknown", "description": content}]
    return parsed, response.usage.total_tokens