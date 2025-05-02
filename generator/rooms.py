import random

room_types = [
    "Traps and Riddles", "Flooded Chamber", "Collapsed Tunnel",
    "Altar Room", "Crypt", "Fungal Grove", "Beast Den", "Cursed Library"
]

room_features = [
    "the smell of decay", "damp, moss-covered walls", "whispers in an unknown language",
    "an eerie glow", "bones arranged in patterns", "a low humming noise", "scorch marks on the floor"
]

encounters = [
    "a lurking ooze", "swarms of glowing insects", "a skeletal champion",
    "a cursed statue that animates", "a fungal beast", "a crazed cultist"
]

loot = [
    "a glowing gem embedded in the wall", "a rusted weapon with runes", "a scroll sealed with wax",
    "a potion that shifts color", "a ring that pulses with heat", "a broken mirror that shows strange scenes"
]

def generate_room(index):
    return {
        "title": f"Room {index + 1}: {random.choice(room_types)}",
        "description": f"You enter a room with {random.choice(room_features)}.",
        "encounter": f"You notice {random.choice(encounters)}.",
        "loot": f"You find {random.choice(loot)}."
    }

def generate_rooms(num_rooms=4):
    return [generate_room(i) for i in range(num_rooms)]
