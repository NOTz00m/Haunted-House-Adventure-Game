"""
Game Statistics and Achievement Tracking System
Tracks player performance, unlocks achievements, and persists data.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class GameStatistics:
    """Tracks comprehensive game statistics across sessions."""
    
    def __init__(self, stats_file: str = "game_stats.json"):
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """Load statistics from file or create new stats."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_stats()
        return self._get_default_stats()
    
    def _get_default_stats(self) -> Dict:
        """Return default statistics structure."""
        return {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "total_playtime_seconds": 0,
            
            # Combat stats
            "monsters_encountered": 0,
            "combats_won": 0,
            "combats_fled": 0,
            "combats_outwitted": 0,
            "total_bones_lost": 0,
            "total_bones_found": 0,
            
            # Exploration stats
            "total_rooms_visited": 0,
            "total_facts_collected": 0,
            "total_spirit_energy_earned": 0,
            
            # Abilities used
            "spectral_searches_used": 0,
            "bone_shields_used": 0,
            "mystic_hints_used": 0,
            
            # Records
            "fastest_win_seconds": None,
            "highest_energy_achieved": 0,
            "longest_win_streak": 0,
            "current_win_streak": 0,
            
            # Difficulty stats (added for future difficulty modes)
            "easy_wins": 0,
            "normal_wins": 0,
            "hard_wins": 0,
            
            # Session data
            "last_played": None,
            "first_played": None
        }
    
    def save_stats(self):
        """Persist statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save statistics: {e}")
    
    # Session management
    def start_game(self):
        """Record game start."""
        self.stats["games_played"] += 1
        if not self.stats["first_played"]:
            self.stats["first_played"] = datetime.now().isoformat()
        self.stats["last_played"] = datetime.now().isoformat()
        self.session_start_time = datetime.now()
    
    def end_game(self, won: bool, playtime_seconds: Optional[int] = None):
        """Record game end with result."""
        if playtime_seconds is None and hasattr(self, 'session_start_time'):
            playtime_seconds = int((datetime.now() - self.session_start_time).total_seconds())
        
        if playtime_seconds:
            self.stats["total_playtime_seconds"] += playtime_seconds
        
        if won:
            self.stats["games_won"] += 1
            self.stats["current_win_streak"] += 1
            
            # Update longest streak
            if self.stats["current_win_streak"] > self.stats["longest_win_streak"]:
                self.stats["longest_win_streak"] = self.stats["current_win_streak"]
            
            # Update fastest win
            if playtime_seconds:
                if (self.stats["fastest_win_seconds"] is None or 
                    playtime_seconds < self.stats["fastest_win_seconds"]):
                    self.stats["fastest_win_seconds"] = playtime_seconds
        else:
            self.stats["games_lost"] += 1
            self.stats["current_win_streak"] = 0
        
        self.save_stats()
    
    # Combat tracking
    def record_combat(self, action: str, won: bool):
        """Record combat encounter outcome."""
        self.stats["monsters_encountered"] += 1
        
        if action == "fight" and won:
            self.stats["combats_won"] += 1
        elif action == "flee" and won:
            self.stats["combats_fled"] += 1
        elif action == "outwit" and won:
            self.stats["combats_outwitted"] += 1
    
    def record_bone_lost(self):
        """Record bone loss."""
        self.stats["total_bones_lost"] += 1
    
    def record_bone_found(self):
        """Record bone found."""
        self.stats["total_bones_found"] += 1
    
    def record_fact_collected(self):
        """Record Halloween fact collection."""
        self.stats["total_facts_collected"] += 1
    
    def record_room_visit(self):
        """Record room visitation."""
        self.stats["total_rooms_visited"] += 1
    
    def record_energy_gained(self, amount: int):
        """Record spirit energy gained."""
        self.stats["total_spirit_energy_earned"] += amount
    
    def record_energy_at(self, current_energy: int):
        """Update highest energy achieved if new record."""
        if current_energy > self.stats["highest_energy_achieved"]:
            self.stats["highest_energy_achieved"] = current_energy
    
    # Ability tracking
    def record_spectral_search(self):
        """Record spectral search usage."""
        self.stats["spectral_searches_used"] += 1
    
    def record_bone_shield(self):
        """Record bone shield usage."""
        self.stats["bone_shields_used"] += 1
    
    def record_mystic_hint(self):
        """Record mystic hint usage."""
        self.stats["mystic_hints_used"] += 1
    
    # Getters
    def get_win_rate(self) -> float:
        """Calculate win rate percentage."""
        total_games = self.stats["games_won"] + self.stats["games_lost"]
        if total_games == 0:
            return 0.0
        return (self.stats["games_won"] / total_games) * 100
    
    def get_combat_success_rate(self) -> float:
        """Calculate combat success rate."""
        if self.stats["monsters_encountered"] == 0:
            return 0.0
        successes = (self.stats["combats_won"] + 
                    self.stats["combats_fled"] + 
                    self.stats["combats_outwitted"])
        return (successes / self.stats["monsters_encountered"]) * 100
    
    def get_summary(self) -> str:
        """Get formatted statistics summary."""
        lines = [
            "═══════════════════════════════════════",
            "           GAME STATISTICS",
            "═══════════════════════════════════════",
            "",
            f"📊 Games Played: {self.stats['games_played']}",
            f"✅ Wins: {self.stats['games_won']}",
            f"❌ Losses: {self.stats['games_lost']}",
            f"📈 Win Rate: {self.get_win_rate():.1f}%",
            f"🔥 Current Streak: {self.stats['current_win_streak']}",
            f"🏆 Best Streak: {self.stats['longest_win_streak']}",
            "",
            "⚔️ COMBAT STATS",
            f"   Monsters Faced: {self.stats['monsters_encountered']}",
            f"   Fights Won: {self.stats['combats_won']}",
            f"   Successful Flees: {self.stats['combats_fled']}",
            f"   Outwitted: {self.stats['combats_outwitted']}",
            f"   Success Rate: {self.get_combat_success_rate():.1f}%",
            "",
            "🦴 BONES & FACTS",
            f"   Bones Found: {self.stats['total_bones_found']}",
            f"   Bones Lost: {self.stats['total_bones_lost']}",
            f"   Facts Collected: {self.stats['total_facts_collected']}",
            "",
            "⚡ ABILITIES USED",
            f"   Spectral Searches: {self.stats['spectral_searches_used']}",
            f"   Bone Shields: {self.stats['bone_shields_used']}",
            f"   Mystic Hints: {self.stats['mystic_hints_used']}",
            "",
            "🌟 RECORDS",
            f"   Highest Energy: {self.stats['highest_energy_achieved']}",
        ]
        
        if self.stats["fastest_win_seconds"]:
            minutes = self.stats["fastest_win_seconds"] // 60
            seconds = self.stats["fastest_win_seconds"] % 60
            lines.append(f"   Fastest Win: {minutes}m {seconds}s")
        
        lines.append("═══════════════════════════════════════")
        
        return "\n".join(lines)


class AchievementSystem:
    """Manages achievement unlocking and tracking."""
    
    # Achievement definitions
    ACHIEVEMENTS = {
        "first_blood": {
            "name": "First Blood",
            "description": "Win your first combat encounter",
            "icon": "⚔️"
        },
        "pacifist": {
            "name": "Pacifist",
            "description": "Win a game without fighting any monsters",
            "icon": "🕊️"
        },
        "warrior": {
            "name": "Warrior",
            "description": "Win 10 combat fights",
            "icon": "🗡️"
        },
        "scholar": {
            "name": "Scholar",
            "description": "Collect 10 Halloween facts in a single game",
            "icon": "📚"
        },
        "bone_collector": {
            "name": "Bone Collector",
            "description": "Find all your bones and win the game",
            "icon": "🦴"
        },
        "escape_artist": {
            "name": "Escape Artist",
            "description": "Successfully flee from 5 monsters in one game",
            "icon": "🏃"
        },
        "master_of_wits": {
            "name": "Master of Wits",
            "description": "Outwit 5 monsters in a single game",
            "icon": "🧠"
        },
        "energy_master": {
            "name": "Energy Master",
            "description": "Accumulate 10 spirit energy in one game",
            "icon": "⚡"
        },
        "shielded_warrior": {
            "name": "Shielded Warrior",
            "description": "Use Bone Shield 3 times in one game",
            "icon": "🛡️"
        },
        "mystic": {
            "name": "Mystic",
            "description": "Use Mystic Hint 5 times",
            "icon": "🔮"
        },
        "perfectionist": {
            "name": "Perfectionist",
            "description": "Win without losing a single bone",
            "icon": "💎"
        },
        "survivor": {
            "name": "Survivor",
            "description": "Win a game with only 1 bone remaining",
            "icon": "💀"
        },
        "speedrunner": {
            "name": "Speedrunner",
            "description": "Win in under 5 minutes",
            "icon": "⏱️"
        },
        "explorer": {
            "name": "Explorer",
            "description": "Visit all 9 rooms in a single game",
            "icon": "🗺️"
        },
        "win_streak": {
            "name": "On Fire!",
            "description": "Win 3 games in a row",
            "icon": "🔥"
        }
    }
    
    def __init__(self, achievements_file: str = "achievements.json"):
        self.achievements_file = achievements_file
        self.unlocked = self._load_achievements()
        self.session_progress = {}  # Track session-specific progress
    
    def _load_achievements(self) -> Dict[str, dict]:
        """Load unlocked achievements from file."""
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_achievements(self):
        """Persist achievements to file."""
        try:
            with open(self.achievements_file, 'w') as f:
                json.dump(self.unlocked, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save achievements: {e}")
    
    def unlock(self, achievement_id: str) -> bool:
        """
        Unlock an achievement if not already unlocked.
        Returns True if newly unlocked, False if already had it.
        """
        if achievement_id not in self.ACHIEVEMENTS:
            return False
        
        if achievement_id in self.unlocked:
            return False
        
        self.unlocked[achievement_id] = {
            "unlocked_at": datetime.now().isoformat(),
            **self.ACHIEVEMENTS[achievement_id]
        }
        self.save_achievements()
        return True
    
    def is_unlocked(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked."""
        return achievement_id in self.unlocked
    
    def get_progress(self) -> tuple:
        """Get achievement progress (unlocked, total)."""
        return len(self.unlocked), len(self.ACHIEVEMENTS)
    
    def get_unlocked_list(self) -> List[dict]:
        """Get list of unlocked achievements."""
        return [
            {
                "id": aid,
                "name": data["name"],
                "description": data["description"],
                "icon": data["icon"],
                "unlocked_at": data["unlocked_at"]
            }
            for aid, data in self.unlocked.items()
        ]
    
    def get_locked_list(self) -> List[dict]:
        """Get list of locked achievements."""
        return [
            {
                "id": aid,
                "name": data["name"],
                "description": data["description"],
                "icon": data["icon"]
            }
            for aid, data in self.ACHIEVEMENTS.items()
            if aid not in self.unlocked
        ]
    
    def check_achievements(self, stats: GameStatistics, session_data: dict) -> List[str]:
        """
        Check for newly unlocked achievements based on stats and session data.
        Returns list of newly unlocked achievement IDs.
        """
        newly_unlocked = []
        
        # First Blood - Win first combat
        if stats.stats["combats_won"] >= 1 and not self.is_unlocked("first_blood"):
            if self.unlock("first_blood"):
                newly_unlocked.append("first_blood")
        
        # Warrior - Win 10 fights
        if stats.stats["combats_won"] >= 10 and not self.is_unlocked("warrior"):
            if self.unlock("warrior"):
                newly_unlocked.append("warrior")
        
        # Bone Collector - Win the game (checked when game won)
        if session_data.get("game_won") and not self.is_unlocked("bone_collector"):
            if self.unlock("bone_collector"):
                newly_unlocked.append("bone_collector")
        
        # Scholar - Collect 10 facts in one game
        if session_data.get("facts_this_game", 0) >= 10 and not self.is_unlocked("scholar"):
            if self.unlock("scholar"):
                newly_unlocked.append("scholar")
        
        # Escape Artist - Flee 5 times in one game
        if session_data.get("flees_this_game", 0) >= 5 and not self.is_unlocked("escape_artist"):
            if self.unlock("escape_artist"):
                newly_unlocked.append("escape_artist")
        
        # Master of Wits - Outwit 5 in one game
        if session_data.get("outwits_this_game", 0) >= 5 and not self.is_unlocked("master_of_wits"):
            if self.unlock("master_of_wits"):
                newly_unlocked.append("master_of_wits")
        
        # Energy Master - Reach 10 energy
        if session_data.get("max_energy_this_game", 0) >= 10 and not self.is_unlocked("energy_master"):
            if self.unlock("energy_master"):
                newly_unlocked.append("energy_master")
        
        # Shielded Warrior - Use shield 3 times in one game
        if session_data.get("shields_this_game", 0) >= 3 and not self.is_unlocked("shielded_warrior"):
            if self.unlock("shielded_warrior"):
                newly_unlocked.append("shielded_warrior")
        
        # Mystic - Use hint 5 times total
        if stats.stats["mystic_hints_used"] >= 5 and not self.is_unlocked("mystic"):
            if self.unlock("mystic"):
                newly_unlocked.append("mystic")
        
        # Perfectionist - Win without losing bones
        if (session_data.get("game_won") and 
            session_data.get("bones_lost_this_game", 0) == 0 and
            not self.is_unlocked("perfectionist")):
            if self.unlock("perfectionist"):
                newly_unlocked.append("perfectionist")
        
        # Survivor - Win with 1 bone
        if (session_data.get("game_won") and 
            session_data.get("final_bones_count", 0) == 1 and
            not self.is_unlocked("survivor")):
            if self.unlock("survivor"):
                newly_unlocked.append("survivor")
        
        # Speedrunner - Win in under 5 minutes
        if (session_data.get("game_won") and 
            session_data.get("playtime_seconds", 999999) < 300 and
            not self.is_unlocked("speedrunner")):
            if self.unlock("speedrunner"):
                newly_unlocked.append("speedrunner")
        
        # Explorer - Visit all 9 rooms
        if len(session_data.get("rooms_visited", set())) >= 9 and not self.is_unlocked("explorer"):
            if self.unlock("explorer"):
                newly_unlocked.append("explorer")
        
        # Win Streak - 3 in a row
        if stats.stats["current_win_streak"] >= 3 and not self.is_unlocked("win_streak"):
            if self.unlock("win_streak"):
                newly_unlocked.append("win_streak")
        
        # Pacifist - Win without fighting
        if (session_data.get("game_won") and 
            session_data.get("fights_this_game", 0) == 0 and
            not self.is_unlocked("pacifist")):
            if self.unlock("pacifist"):
                newly_unlocked.append("pacifist")
        
        return newly_unlocked
