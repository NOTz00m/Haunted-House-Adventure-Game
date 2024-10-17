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

    def lose_bone(self, bone):
        if bone in self.bones:
            self.bones.remove(bone)
            self.lost_bones.append(bone)

    def find_bone(self):
        base_probability = 0.4

        if self.facts_collected >= 6:
            base_probability = 0.5

        if self.lost_bones and random.random() < base_probability:
            return self.lost_bones.pop(0)
        return None

    def collect_fact(self):
        self.facts_collected += 1

    def get_status(self):
        bones_status = f"Currently has: {', '.join(self.bones)}"
        lost_bones_status = f"Lost bones: {', '.join(self.lost_bones)}" if self.lost_bones else "No lost bones"
        return f"{bones_status}\n{lost_bones_status}"

    def is_alive(self):
        return len(self.bones) > 0

    def has_won(self):
        return len(self.lost_bones) == 0