import random

monsters = ["zombie", "ghost", "werewolf", "vampire bat", "cursed doll"]

def encounter_monster(skeleton):
    """
    Legacy monster encounter for backward compatibility.
    Automatically attempts to flee from the monster.
    """
    monster = random.choice(monsters)
    result = combat_encounter(skeleton, "flee", monster)
    return result["message"]

def combat_encounter(skeleton, action, monster_type=None):
    """
    New combat system with strategic choices.
    
    Args:
        skeleton: The player's Skeleton instance
        action: Combat action - "fight", "flee", or "outwit"
        monster_type: Optional specific monster, otherwise random
    
    Returns:
        dict with keys:
            - success: bool
            - message: str (description of what happened)
            - energy_change: int (spirit energy gained/lost)
            - bones_lost: list of bone names lost
    """
    if monster_type is None:
        monster_type = random.choice(monsters)
    
    result = {
        "success": False,
        "message": "",
        "energy_change": 0,
        "bones_lost": []
    }
    
    # Check for bone shield protection
    shield_blocked = False
    
    if action == "fight":
        # 60% chance to win
        if random.random() < 0.6:
            result["success"] = True
            result["energy_change"] = 1
            skeleton.gain_energy(1)
            result["message"] = f"Victory! You fought the {monster_type} and gained 1 spirit energy!"
        else:
            # Fight failed - lose bone unless shielded
            if skeleton.check_shield():
                shield_blocked = True
                result["message"] = f"The {monster_type} strikes, but your bone shield absorbs the blow!"
            elif skeleton.bones:
                lost_bone = random.choice(skeleton.bones)
                skeleton.lose_bone(lost_bone)
                result["bones_lost"].append(lost_bone)
                result["message"] = f"Defeat! The {monster_type} overpowered you and you lost your {lost_bone}!"
            else:
                result["message"] = f"The {monster_type} tries to harm you, but you have no bones left to lose!"
    
    elif action == "flee":
        # 80% chance to escape
        if random.random() < 0.8:
            result["success"] = True
            result["message"] = f"You successfully fled from the {monster_type}!"
        else:
            # Caught while fleeing - lose bone unless shielded
            if skeleton.check_shield():
                shield_blocked = True
                result["message"] = f"The {monster_type} caught you, but your bone shield protected you!"
            elif skeleton.bones:
                lost_bone = random.choice(skeleton.bones)
                skeleton.lose_bone(lost_bone)
                result["bones_lost"].append(lost_bone)
                result["message"] = f"The {monster_type} caught you while fleeing! You lost your {lost_bone}!"
            else:
                result["message"] = f"The {monster_type} caught you, but you have no bones left!"
    
    elif action == "outwit":
        # Success chance based on facts collected (10% per fact, max 90%)
        outwit_chance = min(0.9, skeleton.facts_collected * 0.1)
        
        if random.random() < outwit_chance:
            result["success"] = True
            result["energy_change"] = 2
            skeleton.gain_energy(2)
            result["message"] = f"Brilliant! You used your Halloween knowledge to outwit the {monster_type}! Gained 2 spirit energy!"
        else:
            # Outwit failed - monster is angry, lose TWO bones (if possible)
            bones_to_lose = min(2, len(skeleton.bones))
            
            # Shield can only block one bone loss
            if skeleton.check_shield():
                shield_blocked = True
                bones_to_lose = max(0, bones_to_lose - 1)
            
            for _ in range(bones_to_lose):
                if skeleton.bones:
                    lost_bone = random.choice(skeleton.bones)
                    skeleton.lose_bone(lost_bone)
                    result["bones_lost"].append(lost_bone)
            
            if result["bones_lost"]:
                bones_list = ", ".join(result["bones_lost"])
                shield_text = " (shield blocked one!)" if shield_blocked else ""
                result["message"] = f"The {monster_type} saw through your trick and became enraged! Lost: {bones_list}{shield_text}"
            else:
                result["message"] = f"The {monster_type} saw through your trick, but you have no bones to lose!"
    
    return result

def get_combat_options(skeleton):
    """
    Returns available combat options based on skeleton's current state.
    
    Returns:
        dict with keys "fight", "flee", "outwit" mapped to dict containing:
            - available: bool
            - description: str
            - probability: float (success chance)
    """
    options = {
        "fight": {
            "available": True,
            "description": "Attack the monster directly (60% success)",
            "probability": 0.6,
            "reward": "+1 spirit energy on success",
            "penalty": "Lose 1 bone on failure"
        },
        "flee": {
            "available": True,
            "description": "Try to escape safely (80% success)",
            "probability": 0.8,
            "reward": "No reward, but safe",
            "penalty": "Lose 1 bone if caught"
        },
        "outwit": {
            "available": skeleton.facts_collected > 0,
            "description": f"Use Halloween knowledge ({int(min(90, skeleton.facts_collected * 10))}% success)",
            "probability": min(0.9, skeleton.facts_collected * 0.1),
            "reward": "+2 spirit energy on success",
            "penalty": "Lose 2 bones on failure!"
        }
    }
    
    return options
