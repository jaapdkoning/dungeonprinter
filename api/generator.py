from openai import OpenAI
import os
from datetime import datetime
from api.themes import themes
import json
import re

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

Keep the tone in the style of old-school fantasy. Use at most 100 words.
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


def generate_encounters_with_llm(theme="Unknown Theme", difficulty="1-3", model="gpt-3.5-turbo"):
    user_prompt = f"""
Generate 4 unique fantasy RPG encounters for the theme: {theme}.

Target difficulty level: OSE levels {difficulty}.

Each encounter must be one of:
- combat
- social
- puzzle

For each encounter, provide the following fields:
- title: one line
- type: combat | social | puzzle
- situation: the setup or scene
- challenge: what the players must overcome
- reward: what the players may gain

Respond in pure JSON, structured as an array of 4 objects with these fields.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.0,
        max_tokens=800,
    )

    content = response.choices[0].message.content.strip()

    # Step 1: Strip markdown-style code block if present
    if content.startswith("```json") or content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```\s*$", "", content)

    # Step 2: Extract JSON array if nested in text
    match = re.search(r"(\[\s*{.*?}\s*\])", content, re.DOTALL)
    if match:
        content = match.group(1)

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = [{
            "title": "Parse Error",
            "type": "unknown",
            "situation": "",
            "challenge": "",
            "reward": content
        }]

    return parsed, response.usage.total_tokens
