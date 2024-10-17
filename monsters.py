import random

monsters = ["zombie", "ghost", "werewolf", "vampire bat", "cursed doll"]

def encounter_monster(skeleton):
    monster = random.choice(monsters)
    if skeleton.bones:
        lost_bone = random.choice(skeleton.bones)
        skeleton.lose_bone(lost_bone)
        message = f"Oh no! You encounter a {monster} and lose your {lost_bone}!"

        if not skeleton.is_alive():
            message += " You have lost all your bones! Game Over!"
        return message
    
    else:
        return f"The {monster} tries to scare you, but you've already lost all your bones!"
