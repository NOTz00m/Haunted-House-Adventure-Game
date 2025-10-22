"""
Sound Effects System for Haunted House Adventure
Manages combat, UI, and ambient sound effects with fallback handling.
"""

import pygame
import os
from typing import Optional


class SoundEffects:
    """Manages all game sound effects with graceful degradation."""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.sounds = {}
        self.volume = 0.5
        
        # Initialize pygame mixer if not already done
        if self.enabled:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
            except pygame.error:
                print("Warning: Could not initialize sound system")
                self.enabled = False
        
        # Define sound mappings (will generate simple tones if files missing)
        self.sound_definitions = {
            # Combat sounds
            "fight_start": {"freq": 220, "duration": 200},      # A3 note
            "fight_win": {"freq": 523, "duration": 300},        # C5 - triumphant
            "fight_lose": {"freq": 110, "duration": 400},       # A2 - ominous
            "flee_success": {"freq": 440, "duration": 150},     # A4 - quick
            "flee_caught": {"freq": 185, "duration": 350},      # F#3 - tense
            "outwit_success": {"freq": 659, "duration": 250},   # E5 - clever
            "outwit_fail": {"freq": 147, "duration": 450},      # D3 - dread
            
            # UI sounds
            "button_click": {"freq": 330, "duration": 50},      # E4 - short
            "bone_found": {"freq": 587, "duration": 200},       # D5 - joyful
            "fact_collected": {"freq": 494, "duration": 150},   # B4 - knowledge
            "energy_gained": {"freq": 784, "duration": 180},    # G5 - power
            "shield_activate": {"freq": 392, "duration": 250},  # G4 - protection
            "hint_used": {"freq": 622, "duration": 200},        # D#5 - mystery
            
            # Game state sounds
            "game_start": {"freq": 262, "duration": 300},       # C4 - begin
            "game_won": {"freq": 880, "duration": 500},         # A5 - victory!
            "game_lost": {"freq": 98, "duration": 600},         # G2 - defeat
            "room_enter": {"freq": 294, "duration": 100},       # D4 - transition
        }
    
    def _generate_tone(self, frequency: int, duration: int) -> Optional[pygame.mixer.Sound]:
        """Generate a simple sine wave tone."""
        if not self.enabled:
            return None
        
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate / 1000)
            
            # Generate sine wave
            arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration / 1000, frames))
            
            # Apply envelope (fade in/out to avoid clicks)
            envelope = np.ones(frames)
            fade_frames = min(frames // 10, 50)
            envelope[:fade_frames] = np.linspace(0, 1, fade_frames)
            envelope[-fade_frames:] = np.linspace(1, 0, fade_frames)
            arr = arr * envelope
            
            # Convert to 16-bit PCM
            arr = np.array(arr * 32767, dtype=np.int16)
            
            # Stereo
            arr = np.repeat(arr.reshape(frames, 1), 2, axis=1)
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
            
        except (ImportError, Exception) as e:
            # Numpy not available or error generating sound
            return None
    
    def load_sounds(self):
        """Load or generate all sound effects."""
        if not self.enabled:
            return
        
        for sound_name, sound_def in self.sound_definitions.items():
            # Try to load from file first (for custom sounds)
            sound_file = f"sounds/{sound_name}.wav"
            
            if os.path.exists(sound_file):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_file)
                except pygame.error:
                    # Generate tone if file load fails
                    self.sounds[sound_name] = self._generate_tone(
                        sound_def["freq"], 
                        sound_def["duration"]
                    )
            else:
                # Generate simple tone
                self.sounds[sound_name] = self._generate_tone(
                    sound_def["freq"], 
                    sound_def["duration"]
                )
    
    def play(self, sound_name: str, volume_override: Optional[float] = None):
        """Play a sound effect by name."""
        if not self.enabled:
            return
        
        if sound_name not in self.sounds:
            return
        
        sound = self.sounds[sound_name]
        if sound is None:
            return
        
        try:
            vol = volume_override if volume_override is not None else self.volume
            sound.set_volume(vol)
            sound.play()
        except pygame.error:
            pass  # Silently fail if sound can't play
    
    def set_volume(self, volume: float):
        """Set master volume for all effects (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
    
    def toggle_enabled(self):
        """Toggle sound effects on/off."""
        self.enabled = not self.enabled
        return self.enabled
    
    # Convenience methods for specific sounds
    def play_combat_start(self):
        """Play combat encounter start sound."""
        self.play("fight_start", 0.4)
    
    def play_fight_win(self):
        """Play fight victory sound."""
        self.play("fight_win", 0.6)
    
    def play_fight_lose(self):
        """Play fight defeat sound."""
        self.play("fight_lose", 0.5)
    
    def play_flee_success(self):
        """Play successful flee sound."""
        self.play("flee_success", 0.5)
    
    def play_flee_caught(self):
        """Play caught while fleeing sound."""
        self.play("flee_caught", 0.5)
    
    def play_outwit_success(self):
        """Play outwit success sound."""
        self.play("outwit_success", 0.6)
    
    def play_outwit_fail(self):
        """Play outwit failure sound."""
        self.play("outwit_fail", 0.5)
    
    def play_button_click(self):
        """Play UI button click sound."""
        self.play("button_click", 0.3)
    
    def play_bone_found(self):
        """Play bone found sound."""
        self.play("bone_found", 0.6)
    
    def play_fact_collected(self):
        """Play fact collection sound."""
        self.play("fact_collected", 0.5)
    
    def play_energy_gained(self):
        """Play spirit energy gained sound."""
        self.play("energy_gained", 0.5)
    
    def play_shield_activate(self):
        """Play bone shield activation sound."""
        self.play("shield_activate", 0.6)
    
    def play_hint_used(self):
        """Play mystic hint sound."""
        self.play("hint_used", 0.5)
    
    def play_game_start(self):
        """Play game start sound."""
        self.play("game_start", 0.5)
    
    def play_game_won(self):
        """Play victory sound."""
        self.play("game_won", 0.7)
    
    def play_game_lost(self):
        """Play defeat sound."""
        self.play("game_lost", 0.6)
    
    def play_room_enter(self):
        """Play room transition sound."""
        self.play("room_enter", 0.3)


# Create a global sound effects instance
try:
    sound_effects = SoundEffects(enabled=True)
    sound_effects.load_sounds()
except Exception as e:
    print(f"Warning: Sound effects disabled due to error: {e}")
    sound_effects = SoundEffects(enabled=False)
