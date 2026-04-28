# Haunted House Adventure Game

**Version 3.0.0** - Enhanced Edition 🎃

**P.S: This code is also available on Replit:** [Haunted House Adventure Game](https://replit.com/@notz00m/Halloween-Coding-Competition?v=1)

## Overview

Welcome to the Haunted House Adventure Game! In this enhanced interactive adventure, you play as Bones, a skeleton navigating through various spooky rooms, searching for lost bones, strategically encountering monsters, and collecting fun Halloween facts. Now featuring comprehensive statistics tracking, achievement system, sound effects, and polished UI!

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

---

**Enjoy the game! Can you find all your bones and unlock all achievements?**
