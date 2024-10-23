class AchievementManager:
    def __init__(self):
        # initialize all achievements as locked/false
        self.achievements = {
            "first_bone": {"description": "Find your first bone", "unlocked": False},
            "three_facts": {"description": "Collect 3 facts", "unlocked": False},
        }

    def unlock_achievement(self, key):
        if key in self.achievements and not self.achievements[key]["unlocked"]:
            self.achievements[key]["unlocked"] = True
            return f"Achievement Unlocked: {self.achievements[key]['description']}"
        return None

    def check_achievements(self, skeleton):
        messages = []
        if not self.achievements["first_bone"]["unlocked"] and len(skeleton.bones) > 0:
            message = self.unlock_achievement("first_bone")
            if message:
                messages.append(message)

        if not self.achievements["three_facts"]["unlocked"] and skeleton.facts_collected >= 3:
            message = self.unlock_achievement("three_facts")
            if message:
                messages.append(message)

        return messages

    def get_unlocked_achievements(self):
        return [ach["description"] for ach in self.achievements.values() if ach["unlocked"]]
