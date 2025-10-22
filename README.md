# Haunted House Adventure Game

**Version 3.0.0** - Enhanced Edition 🎃

**P.S: This code is also available on Replit:** [Haunted House Adventure Game](https://replit.com/@notz00m/Halloween-Coding-Competition?v=1)

## Overview

Welcome to the Haunted House Adventure Game! In this enhanced interactive adventure, you play as Bones, a skeleton navigating through various spooky rooms, searching for lost bones, strategically encountering monsters, and collecting fun Halloween facts. Now featuring comprehensive statistics tracking, achievement system, sound effects, and polished UI!

## ✨ What's New in v3.0.0

### Major Enhancements
- **📊 Statistics Tracking** - Comprehensive tracking of wins, losses, combat performance, and more
- **🏆 Achievement System** - 15 unlockable achievements for various playstyles and milestones
- **🔊 Sound Effects** - Combat audio, UI feedback sounds, and atmospheric effects
- **📖 Help System** - In-game tutorial and comprehensive strategy guide
- **🎨 UI Overhaul** - Clean visual hierarchy, better navigation clarity, and consistent design
- **📍 Enhanced Navigation** - See available exits and destinations for each room
- **⚙️ Difficulty Modes** - Easy, Normal, and Hard difficulty settings (infrastructure ready)

### UI/UX Improvements
- Clear status panel with sections for bones, energy, and progress
- Visual progress bar showing bone collection
- Room exit display showing where each direction leads
- Streamlined combat dialog with clearer choices and percentages
- Color-coded feedback messages
- Consistent spacing, fonts, and button styling
- Better error handling with graceful degradation

### Quality of Life
- `.gitignore` for repository hygiene
- Robust error handling for missing assets (music/icons)
- Achievement unlock notifications
- End-game statistics summary
- Session-specific progress tracking

## Features

### Core Gameplay
- **Explore Multiple Rooms**: Traverse 9 unique haunted rooms, each with distinct themes
- **Find and Reattach Lost Bones**: Locate your missing bones and restore your skeletal form
- **Strategic Combat System**: Choose how to handle monster encounters
  - **Fight** (60% success) - Risk/reward combat for spirit energy
  - **Flee** (80% success) - Safe escape option
  - **Outwit** (10% per fact) - High-risk, high-reward strategy
- **Spirit Energy Abilities**: Earn energy through combat and use powerful abilities
  - **Spectral Search** (2 energy) - Guarantee finding a bone
  - **Bone Shield** (3 energy) - Block next bone loss
  - **Mystic Hint** (1 energy) - Reveal bone locations
- **Face 5 Monster Types**: zombies, ghosts, werewolves, vampire bats, cursed dolls
- **Collect Halloween Facts**: 19 facts that improve your outwit success rate
- **Background Music**: Eerie atmospheric music
- **Sound Effects**: Combat sounds, UI feedback, success/failure audio cues
- **Save and Load Game**: Resume your adventure anytime

### Statistics & Achievements
- **Track Your Progress**: Wins, losses, combat stats, exploration data
- **Unlock Achievements**: 15 achievements including:
  - Combat achievements (First Blood, Warrior, Pacifist)
  - Collection achievements (Bone Collector, Scholar)
  - Speedrun achievements (Speedrunner)
  - Playstyle achievements (Perfectionist, Survivor)
  - And more!
- **View Statistics**: Comprehensive stats screen with all your accomplishments

## How to Play

### Navigation
1. **Move Between Rooms**: Use directional buttons (↑ Up, ↓ Down, ← Left, → Right)
2. **Check Exits**: Look at the room description to see available exits and destinations
3. **Explore Rooms**: Click the 🔍 Explore button to search for bones, facts, or encounter events

### Combat Strategy
When you encounter a monster, you have three options:

**⚔️ FIGHT** (60% success rate)
- Win: Gain +1 spirit energy
- Lose: Lose 1 bone
- Best for: Building energy reserves

**🏃 FLEE** (80% success rate)
- Win: Escape safely
- Lose: Caught! Lose 1 bone
- Best for: Preserving bones when low

**🧠 OUTWIT** (10% per fact collected, max 90%)
- Requires: At least 1 Halloween fact
- Win: Gain +2 spirit energy
- Lose: Lose 2 bones (monster is enraged!)
- Best for: High-risk, high-reward when you have 6+ facts

**Pro Tip**: The 🛡️ Bone Shield blocks the next bone loss from any source!

### Spirit Energy Abilities
Click the **⚡ Use Spirit Energy** button to access:

1. **🔍 Spectral Search (2 energy)** - Guarantee finding a bone in the current room
2. **🛡️ Bone Shield (3 energy)** - Block the next bone loss from combat or events
3. **🔮 Mystic Hint (1 energy)** - Reveals 3 rooms that may contain bones

### Win & Lose Conditions
- **✅ WIN**: Find all your lost bones and reattach them
- **❌ LOSE**: Lose all your bones to monsters or events

### Tips for Success
- 🦴 Explore thoroughly - bones are hidden throughout the house
- 🏃 Flee from early monsters to preserve bones while building knowledge
- 📚 Collect facts to unlock and improve the Outwit strategy
- ⚡ Save spirit energy for emergencies
- 🔍 Use Spectral Search when you're close to winning
- 🛡️ Bone Shield is your "get out of jail free" card

## Requirements

- Python 3.10 or higher
- pygame 2.6.1 (for audio playback)
- tkinter (usually bundled with Python)
- numpy (for sound effect generation, optional)

## Installation

1. Clone this repository or download the files
2. Install the required packages:
   ```bash
   pip install pygame numpy
   ```
   Or use Poetry:
   ```bash
   poetry install
   ```

## Running the Game

To start the game, run the following command in the game's directory:

```bash
python main.py
```

The game window will open and you can begin your adventure!

### First Time Playing?
Click the **❓ Help** button for a comprehensive tutorial and strategy guide!

## Game Controls

| Button | Function |
|--------|----------|
| ↑ ↓ ← → | Navigate between rooms |
| 🔍 Explore | Search current room |
| ⚡ Use Spirit Energy | Access special abilities |
| ❓ Help | View tutorial and guide |
| 🏆 Stats | View statistics and achievements |
| 💾 Save / 📂 Load | Save or load your game |
| Quit | Exit the game |

## Achievement List

Unlock all 15 achievements by completing special challenges:

### Combat Achievements
- **⚔️ First Blood** - Win your first combat encounter
- **🗡️ Warrior** - Win 10 combat fights
- **🕊️ Pacifist** - Win a game without fighting any monsters
- **🏃 Escape Artist** - Successfully flee from 5 monsters in one game
- **🧠 Master of Wits** - Outwit 5 monsters in a single game

### Collection Achievements
- **🦴 Bone Collector** - Find all your bones and win the game
- **📚 Scholar** - Collect 10 Halloween facts in a single game
- **🗺️ Explorer** - Visit all 9 rooms in a single game

### Resource Achievements
- **⚡ Energy Master** - Accumulate 10 spirit energy in one game
- **🛡️ Shielded Warrior** - Use Bone Shield 3 times in one game
- **🔮 Mystic** - Use Mystic Hint 5 times total

### Challenge Achievements
- **💎 Perfectionist** - Win without losing a single bone
- **💀 Survivor** - Win a game with only 1 bone remaining
- **⏱️ Speedrunner** - Win in under 5 minutes
- **🔥 On Fire!** - Win 3 games in a row

## Statistics Tracked

The game tracks comprehensive statistics across all your sessions:

**Games**
- Games played, won, and lost
- Win rate and win streaks
- Fastest victory time

**Combat**
- Monsters encountered
- Fights won, successful flees, outwits
- Combat success rate

**Exploration**
- Rooms visited
- Bones found and lost
- Halloween facts collected

**Abilities**
- Spirit energy earned
- Spectral Searches, Bone Shields, and Mystic Hints used
- Highest energy achieved

View your full statistics anytime by clicking the **🏆 Stats** button!

## Technical Details

### File Structure
```
Haunted-House-Adventure-Game/
├── main.py                 # Main game file with UI
├── skeleton.py             # Player character class
├── rooms.py                # Room navigation and events
├── monsters.py             # Combat system
├── facts.py                # Halloween facts database
├── game_stats.py           # Statistics and achievements
├── sound_system.py         # Sound effects manager
├── ui_constants.py         # UI styling constants
├── test_combat_system.py   # Unit tests
├── integration_test.py     # Integration tests
├── icons/                  # Room icon images
├── haloweenmusic.mp3      # Background music
├── README.md              # This file
├── CHANGELOG.md           # Version history
└── .gitignore             # Git ignore patterns
```

### Save Files
- `savegame.pkl` - Your game progress
- `game_stats.json` - Persistent statistics
- `achievements.json` - Unlocked achievements

All save files are stored in the game directory and persist across sessions.

## Version History

### v3.0.0 (Current) - Enhanced Edition
- Added statistics tracking system
- Added 15-achievement system
- Added sound effects for combat and UI
- Complete UI/UX overhaul
- Added help system and tutorial
- Enhanced navigation with exit display
- Improved error handling
- Added .gitignore for repository hygiene

### v2.0.0 - Combat System Update
- Strategic combat with Fight/Flee/Outwit options
- Spirit energy system with abilities
- Bone Shield and Spectral Search mechanics
- Enhanced monster encounters

### v1.0.0 - Original Release
- Basic room exploration
- Simple monster encounters
- Bone finding mechanics
- Save/load functionality

## Known Issues & Future Improvements

### Future Features (Planned)
- Difficulty mode selection UI
- Custom sound effect files (currently uses generated tones)
- More room types and monsters
- Multiplayer support
- Mobile version

### Known Limitations
- Sound effects require numpy for generation (gracefully degrades if unavailable)
- Background music requires haloweenmusic.mp3 file
- Room icons are optional (game works without them)

## Troubleshooting

**Game won't start:**
- Ensure Python 3.10+ is installed
- Install pygame: `pip install pygame`
- Check that you're running from the correct directory

**No music:**
- Verify `haloweenmusic.mp3` exists in the game folder
- Check pygame installation
- Game continues without music if file is missing

**No sound effects:**
- Install numpy: `pip install numpy`
- Sound effects are optional, game works without them

**Icons not showing:**
- Verify `icons/` folder exists with PNG files
- Game continues without icons if files are missing

**Save file won't load:**
- Old save files (v1.0.0 and v2.0.0) are fully compatible
- Ensure file hasn't been corrupted
- Try starting a new game

## Contributing

This project welcomes improvements! Areas for contribution:
- Additional Halloween facts
- New monster types
- Room expansions
- Custom sound effects
- Translations
- Bug fixes

## Credits

**v3.0.0 Enhancements:** AI Code Improvement Agent
**v2.0.0 Combat System:** AI Code Improvement Agent  
**v1.0.0 Original Game:** Original developer (via Replit)

## License

[Add your license here]

---

**Enjoy the game! Can you find all your bones and unlock all achievements?** 🦴👻🎃
