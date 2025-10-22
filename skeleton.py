import random

class Skeleton:
    def __init__(self):
        self.name = "Bones"
        all_bones = ["head", "torso", "left arm", "right arm", "left leg", "right leg"]
        self.bones = all_bones.copy()
        self.lost_bones = []

        # lose 2-4 bones at start of game
        num_lost = random.randint(2, 4)
        for _ in range(num_lost):
            bone = random.choice(self.bones)
            self.bones.remove(bone)
            self.lost_bones.append(bone)

        self.facts_collected = 0
        self.current_room = "Entrance Hall"
        self.hinted_rooms = {}  # track room with hint
        
        # New combat system attributes
        self.spirit_energy = 0
        self.bone_shield_active = False

    def lose_bone(self, bone):
        if bone in self.bones:
            self.bones.remove(bone)
            self.lost_bones.append(bone)

    def find_bone(self):
        if self.current_room in self.hinted_rooms:
            # if first exploration in room, guarantee a bone
            if not self.hinted_rooms[self.current_room]["found"]:
                self.hinted_rooms[self.current_room]["found"] = True
                return self.lost_bones.pop(0)

        base_probability = 0.4
        
        if self.facts_collected >= 6:
            base_probability = 0.5

        if self.lost_bones and random.random() < base_probability:
            return self.lost_bones.pop(0)
        return None

    def collect_fact(self):
        self.facts_collected += 1

    def mark_room_as_hinted(self, room):
        if room not in self.hinted_rooms:
            self.hinted_rooms[room] = {"hinted": True, "found": False}  # init tracking

    def get_status(self):
        bones_status = f"Currently has: {', '.join(self.bones)}"
        lost_bones_status = f"Lost bones: {', '.join(self.lost_bones)}" if self.lost_bones else "No lost bones"
        return f"{bones_status}\n{lost_bones_status}"

    def is_alive(self):
        return len(self.bones) > 0

    def has_won(self):
        return len(self.lost_bones) == 0
    
    # Spirit Energy System Methods
    def gain_energy(self, amount):
        """Add spirit energy to the skeleton's reserves."""
        self.spirit_energy += amount
        return self.spirit_energy
    
    def spend_energy(self, amount):
        """
        Attempt to spend spirit energy.
        Returns True if successful, False if insufficient energy.
        """
        if self.spirit_energy >= amount:
            self.spirit_energy -= amount
            return True
        return False
    
    def activate_shield(self):
        """Activate bone shield protection (costs 3 energy)."""
        if self.spend_energy(3):
            self.bone_shield_active = True
            return True
        return False
    
    def check_shield(self):
        """Check if shield is active and consume it if so."""
        if self.bone_shield_active:
            self.bone_shield_active = False
            return True
        return False
    
    def spectral_search(self):
        """
        Use spirit energy to guarantee finding a bone (costs 2 energy).
        Returns the found bone or None if no lost bones remain.
        """
        if not self.spend_energy(2):
            return None
        
        if self.lost_bones:
            return self.lost_bones.pop(0)
        return None
    
    def mystic_hint(self):
        """
        Use spirit energy to get hints about bone locations (costs 1 energy).
        Returns list of rooms that might contain bones.
        """
        if not self.spend_energy(1):
            return None
        
        # Return up to 3 random room names as hints
        from rooms import rooms
        available_rooms = [room for room in rooms.keys() if room != self.current_room]
        hint_count = min(3, len(available_rooms))
        return random.sample(available_rooms, hint_count)
