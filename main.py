import os
from datetime import datetime
from generator.llm import generate_room_with_llm
from api.themes import themes
from generator.printer import print_to_markdown

def choose_theme():
    print("📚 Available Dungeon Themes:")
    theme_list = list(themes.keys())
    for idx, name in enumerate(theme_list):
        print(f"{idx + 1}. {name}")
    
    while True:
        try:
            selection = int(input("Select a theme by number: ")) - 1
            if 0 <= selection < len(theme_list):
                return theme_list[selection]
            else:
                print("❌ Invalid number, try again.")
        except ValueError:
            print("❌ Please enter a number.")

def main():
    use_llm = True
    selected_theme = choose_theme()

    rooms = []
    total_tokens = 0

    if use_llm:
        print(f"\n⏳ Generating 4 rooms in theme: {selected_theme}...\n")
        for i in range(4):
            markdown_room, tokens_used = generate_room_with_llm(theme=selected_theme)
            rooms.append({"markdown": markdown_room})
            total_tokens += tokens_used
    else:
        print("LLM mode is disabled. Using local generation (not implemented here).")
        return

    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_theme = selected_theme.replace(" ", "_")
    output_filename = f"dungeon_{safe_theme}_{timestamp}.md"
    output_path = os.path.join("output", output_filename)

    # Write combined markdown file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🏰 Dungeon Zine\n\n")
        f.write(f"**Theme:** {selected_theme}\n")
        f.write(f"Generated at: {timestamp}\n")
        f.write(f"Model: gpt-3.5-turbo | Total tokens used: {total_tokens}\n\n---\n\n")
        for room in rooms:
            f.write(room["markdown"])
            f.write("\n\n---\n\n")

    print(f"✅ Dungeon generated: {output_path}")
    print(f"📊 Total tokens used: {total_tokens}")

if __name__ == "__main__":
    main()
