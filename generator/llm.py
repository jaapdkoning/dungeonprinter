from openai import OpenAI
import os
from datetime import datetime
from generator.themes import themes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = "You are a creative and evocative old-school RPG dungeon master."

def generate_room_with_llm(theme="Undead Crypt", model="gpt-3.5-turbo", log_dir="logs"):
    # Load theme data
    theme_data = themes.get(theme, {})
    theme_description = theme_data.get("description", "")
    encounter_options = ", ".join(theme_data.get("encounter_table", []))
    loot_options = ", ".join(theme_data.get("loot_table", []))

    # Compose user prompt
    user_prompt = f"""
Generate a single dungeon room in the theme: **{theme}**

Theme description: {theme_description}

Here are some examples of possible encounters: {encounter_options}
And possible loot items: {loot_options}

Format your response in Markdown:
- Use a room title with '## Room Name'
- Write a short, evocative description of the room
- Include one encounter or threat
- Include one loot item

Keep the total under 100 words. Be immersive, but brief.
"""

    # Run completion
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Log output and usage
    log_filename = f"{log_dir}/room_{theme.replace(' ', '_')}_{timestamp}.md"
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(f"# Theme: {theme}\n")
        f.write(f"Generated at: {timestamp}\n")
        f.write(f"Model: {model}, Tokens used: {tokens_used}\n\n")
        f.write(content)

    print(f"📄 Logged room to: {log_filename} (tokens used: {tokens_used})")

    return content, tokens_used
