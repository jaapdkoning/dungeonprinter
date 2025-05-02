def print_to_markdown(rooms, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🏰 Dungeon Zine\n\n")
        f.write("Generated with *Dungeonprinter*.\n\n---\n\n")
        for room in rooms:
            f.write(f"## {room['title']}\n\n")
            f.write(f"{room['description']}\n\n")
            f.write(f"**Encounter:** {room['encounter']}\n\n")
            f.write(f"**Loot:** {room['loot']}\n\n")
            f.write("---\n\n")
