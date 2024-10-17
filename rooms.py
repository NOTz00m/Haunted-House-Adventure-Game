import random
from monsters import encounter_monster
from facts import get_random_fact

rooms = {
    "Entrance Hall": {
        "left": "Creepy Library",
        "right": "Spooky Kitchen",
        "down": "Dark Cellar",
        "description": "You are in a grand hall with dusty chandeliers and old portraits."
    },
    "Creepy Library": {
        "right": "Entrance Hall",
        "description": "Books line the walls, their spines cracked. A chill runs down your spine."
    },
    "Dark Cellar": {
        "up": "Entrance Hall",
        "description": "The air is damp and musty, with shadows lurking in the corners."
    },
    "Spooky Kitchen": {
        "left": "Entrance Hall",
        "up": "Cursed Ballroom",
        "description": "The kitchen is dark and filled with cobwebs, old pots hanging above."
    },
    "Cursed Ballroom": {
        "down": "Spooky Kitchen",
        "right": "Mystic Garden",
        "description": "Once elegant, the ballroom is now in ruins, with tattered curtains swaying."
    },
    "Mystic Garden": {
        "left": "Cursed Ballroom",
        "description": "An overgrown garden where ghostly flowers bloom under the moonlight."
    },
    # add new rooms
    "Haunted Attic": {
        "down": "Creepy Library",
        "description": "Dusty trunks and old furniture fill this attic, with whispers in the air."
    },
    "Forgotten Graveyard": {
        "up": "Mystic Garden",
        "description": "Weathered tombstones are scattered about, and an eerie silence surrounds you."
    },
    "Phantom Cave": {
        "left": "Forgotten Graveyard",
        "description": "The cave is dark and damp, echoing with the sound of dripping water."
    }
} # this code is a little hacky, but it works

def move_room(skeleton, direction):
    current = skeleton.current_room
    if direction in rooms[current]:
        skeleton.current_room = rooms[current][direction]
        room_description = rooms[skeleton.current_room]["description"]
        return f"You move {direction} to the {skeleton.current_room}. {room_description}"
    else:
        return "You can't move in that direction from here."

def explore_current_room(skeleton):
    event = random.choice(["monster", "bone", "fact"])
    result = ""

    if event == "monster":
        result = encounter_monster(skeleton)
        return f"Event: {result}"
    elif event == "bone":
        found_bone = skeleton.find_bone()
        if found_bone:
            skeleton.bones.append(found_bone)
            return f"Success: You found your {found_bone}! It's reattached."
        else:
            return "Search: You can't find any bones here."
    elif event == "fact":
        fact = get_random_fact()
        skeleton.collect_fact()
        return f"Random fact found: {fact}"

def style_result(text):
    # AHHHHHHHHHHHHHHHH why does this not work
    # ^fixed haha, leaving here just in case it doesn't work out
    if "Random fact found:" in text:
        return f"\033[38;5;208m{text}\033[0m"  #orange : make into seperate label maybe???
    elif "Event:" in text or "Success:" in text:
        return f"\033[31m{text}\033[0m" #red
    elif "Search:" in text:
        return text
