import tkinter as tk
import pickle
from tkinter import PhotoImage, messagebox, Toplevel, scrolledtext
import pygame
from skeleton import Skeleton
from rooms import move_room, explore_current_room, rooms
from monsters import combat_encounter, get_combat_options, monsters
from game_stats import GameStatistics, AchievementSystem
from sound_system import sound_effects
from ui_constants import COLORS, FONTS, SPACING, ICONS, WINDOW, BUTTON, DIFFICULTY, DEFAULT_DIFFICULTY
import random
from datetime import datetime

# Global game state
game_stats = GameStatistics()
achievements = AchievementSystem()
current_difficulty = DEFAULT_DIFFICULTY
session_data = {}  # Track session-specific data for achievements

# save/load game with backward compatibility
def save_game():
    game_state = {
        "current_room": skeleton.current_room,
        "bones": skeleton.bones,
        "lost_bones": skeleton.lost_bones,
        "facts_collected": skeleton.facts_collected,
        "hinted_rooms": skeleton.hinted_rooms,
        "spirit_energy": skeleton.spirit_energy,
        "bone_shield_active": skeleton.bone_shield_active,
        "difficulty": current_difficulty,
        "session_data": session_data
    }
    with open("savegame.pkl", "wb") as file:
        pickle.dump(game_state, file)
    sound_effects.play_button_click()
    update_result_display("💾 Game saved successfully.", "success")

def load_game():
    global current_difficulty, session_data
    try:
        with open("savegame.pkl", "rb") as file:
            game_state = pickle.load(file)

            skeleton.current_room = game_state["current_room"]
            skeleton.bones = game_state["bones"]
            skeleton.lost_bones = game_state["lost_bones"]
            skeleton.facts_collected = game_state["facts_collected"]
            skeleton.hinted_rooms = game_state["hinted_rooms"]
            
            # Backward compatibility - add defaults for new attributes
            skeleton.spirit_energy = game_state.get("spirit_energy", 0)
            skeleton.bone_shield_active = game_state.get("bone_shield_active", False)
            current_difficulty = game_state.get("difficulty", DEFAULT_DIFFICULTY)
            session_data = game_state.get("session_data", {})

        update_status()
        sound_effects.play_button_click()
        update_result_display("📂 Game loaded successfully.", "success")
    except FileNotFoundError:
        update_result_display("❌ No save file found. Save a game first.", "error")
    except Exception as e:
        update_result_display(f"❌ Error loading game: {str(e)}", "error")

# init music with error handling
try:
    pygame.mixer.init()
    pygame.mixer.music.load('haloweenmusic.mp3') 
    pygame.mixer.music.play(-1)  # inf loop
    pygame.mixer.music.set_volume(0.2)
except (pygame.error, FileNotFoundError) as e:
    print(f"Warning: Could not load background music: {e}")
    # Game continues without music

# HELP AND TUTORIAL SYSTEM

def show_help_dialog():
    """Display comprehensive help and tutorial information."""
    help_window = Toplevel(window)
    help_window.title("How to Play")
    help_window.geometry("650x600")
    help_window.transient(window)
    help_window.grab_set()
    
    # Create scrolled text widget
    text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, 
                                            font=FONTS["body"], padx=15, pady=15)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    help_text = f"""
{ICONS['skull']} HAUNTED HOUSE ADVENTURE - PLAYER GUIDE {ICONS['skull']}

{'═' * 60}
OBJECTIVE
{'═' * 60}
You are Bones, a skeleton who has lost 2-4 of your body parts in this haunted
house! Navigate through 9 spooky rooms, avoid or defeat monsters, and find all
your missing bones to escape and win.

{'═' * 60}
NAVIGATION
{'═' * 60}
{ICONS['info']} Use the directional buttons (Up/Down/Left/Right) to move between rooms
{ICONS['info']} The room description shows which exits are available
{ICONS['info']} Look for the "Exits:" line to see where each direction leads
{ICONS['info']} Click "Explore" to search the current room

{'═' * 60}
ROOM EXPLORATION
{'═' * 60}
When you explore a room, you might find:
  {ICONS['bone']} Lost Bones - Reattach them to restore yourself! (40-50% chance)
  {ICONS['monster']} Monsters - Trigger combat encounters (see combat guide below)
  📖 Halloween Facts - Increase your knowledge (helps with Outwit)
  {ICONS['warning']} Random Events - Ghosts may give you hints about bone locations

{'═' * 60}
COMBAT SYSTEM {ICONS['fight']}
{'═' * 60}
When you encounter a monster, choose your strategy:

1. FIGHT {ICONS['fight']} (60% success)
   • High risk, moderate reward
   • Win: Gain +1 Spirit Energy
   • Lose: Lose 1 bone

2. FLEE {ICONS['flee']} (80% success)
   • Low risk, no reward
   • Win: Escape safely
   • Lose: Caught! Lose 1 bone

3. OUTWIT {ICONS['outwit']} (10% per fact collected, max 90%)
   • Requires at least 1 Halloween fact
   • High risk, high reward
   • Win: Gain +2 Spirit Energy
   • Lose: Monster is enraged! Lose 2 bones

{ICONS['shield']} TIP: Bone Shield blocks the next bone loss from any source!

{'═' * 60}
SPIRIT ENERGY SYSTEM {ICONS['energy']}
{'═' * 60}
Earn Spirit Energy by winning combat encounters, then spend it on abilities:

{ICONS['spectral']} SPECTRAL SEARCH (2 energy)
   • Guarantee finding a bone in the current room
   • Use when you desperately need a bone!

{ICONS['shield']} BONE SHIELD (3 energy)
   • Block the next bone loss from combat or any event
   • One-time use, consumed when hit

{ICONS['mystic']} MYSTIC HINT (1 energy)
   • Reveals 3 rooms that may contain bones
   • Helps guide your exploration

{'═' * 60}
HALLOWEEN FACTS {ICONS['outwit']}
{'═' * 60}
Collecting Halloween facts has TWO benefits:
  1. Unlocks the "Outwit" combat option
  2. Increases Outwit success rate (+10% per fact, max 90%)
  
STRATEGY: Collect 6+ facts before relying on Outwit!

{'═' * 60}
WIN & LOSE CONDITIONS
{'═' * 60}
{ICONS['success']} WIN: Find all your lost bones and reattach them
{ICONS['failure']} LOSE: Lose all your bones to monsters or events

{'═' * 60}
TIPS FOR SUCCESS
{'═' * 60}
{ICONS['star']} Explore thoroughly - bones are hidden in rooms
{ICONS['star']} Flee from early monsters to preserve bones
{ICONS['star']} Collect facts to enable powerful Outwit strategy
{ICONS['star']} Save Spirit Energy for emergencies
{ICONS['star']} Use Spectral Search when you're close to winning
{ICONS['star']} Bone Shield is your "get out of jail free" card

{'═' * 60}
DIFFICULTY MODES
{'═' * 60}
EASY: Higher success rates, more forgiving
NORMAL: Balanced, recommended for first playthrough
HARD: Lower success rates, challenging exploration

{'═' * 60}
ACHIEVEMENTS {ICONS['trophy']}
{'═' * 60}
Unlock 15 achievements by completing special challenges:
  • Combat achievements (win fights, flee, outwit)
  • Collection achievements (find bones, collect facts)
  • Speedrun achievements (win quickly)
  • Playstyle achievements (pacifist, perfectionist)

Check your progress in the Statistics menu!

{'═' * 60}

Good luck, Bones! May you find all your parts and escape this haunted house!

{'═' * 60}
"""
    
    text_widget.insert(1.0, help_text)
    text_widget.config(state=tk.DISABLED)  # Make read-only
    
    close_btn = tk.Button(help_window, text="Close", command=help_window.destroy,
                          font=FONTS["body_bold"], width=15)
    close_btn.pack(pady=SPACING["md"])

def show_statistics_dialog():
    """Display game statistics and achievements."""
    stats_window = Toplevel(window)
    stats_window.title("Statistics & Achievements")
    stats_window.geometry("600x700")
    stats_window.transient(window)
    stats_window.grab_set()
    
    # Create notebook/tabs
    notebook = tk.Frame(stats_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Statistics text
    stats_text = scrolledtext.ScrolledText(notebook, wrap=tk.WORD, 
                                           font=("Courier New", 10), 
                                           padx=10, pady=10)
    stats_text.pack(fill=tk.BOTH, expand=True)
    stats_text.insert(1.0, game_stats.get_summary())
    stats_text.config(state=tk.DISABLED)
    
    # Achievements section
    ach_frame = tk.Frame(stats_window)
    ach_frame.pack(fill=tk.X, padx=10, pady=10)
    
    unlocked_count, total_count = achievements.get_progress()
    progress_label = tk.Label(ach_frame, 
                             text=f"{ICONS['trophy']} Achievements: {unlocked_count}/{total_count}",
                             font=FONTS["heading"])
    progress_label.pack()
    
    # Show unlocked achievements
    unlocked = achievements.get_unlocked_list()
    if unlocked:
        unlocked_label = tk.Label(ach_frame, text="\nUnlocked:", 
                                 font=FONTS["body_bold"])
        unlocked_label.pack()
        for ach in unlocked[:5]:  # Show first 5
            ach_text = f"{ach['icon']} {ach['name']}: {ach['description']}"
            label = tk.Label(ach_frame, text=ach_text, font=FONTS["small"])
            label.pack()
    
    close_btn = tk.Button(stats_window, text="Close", command=stats_window.destroy,
                          font=FONTS["body_bold"], width=15)
    close_btn.pack(pady=SPACING["md"])

# GAME END/WIN FUNCTIONALITY:

def set_buttons_state(state):
    """Enable or disable all game control buttons."""
    up_button.config(state=state)
    left_button.config(state=state)
    down_button.config(state=state)
    right_button.config(state=state)
    explore_button.config(state=state)
    energy_button.config(state=state)

def game_over():
    global restart_button, quit_button
    
    # Play defeat sound
    sound_effects.play_game_lost()
    
    # Record game end
    session_data['game_won'] = False
    session_data['final_bones_count'] = len(skeleton.bones)
    game_stats.end_game(won=False)
    
    # Check achievements
    newly_unlocked = achievements.check_achievements(game_stats, session_data)
    
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.insert(tk.END, f"{ICONS['skull']} Game Over! You have lost all your bones.\n\n")
    
    # Show quick stats
    result_text_widget.insert(tk.END, f"Monsters faced: {session_data.get('monsters_encountered', 0)}\n")
    result_text_widget.insert(tk.END, f"Bones found: {session_data.get('bones_found_this_game', 0)}\n")
    result_text_widget.insert(tk.END, f"Facts collected: {session_data.get('facts_this_game', 0)}\n\n")
    
    if newly_unlocked:
        result_text_widget.insert(tk.END, f"{ICONS['trophy']} New achievements unlocked!\n\n")
    
    result_text_widget.insert(tk.END, "Would you like to restart or quit?\n")
    result_text_widget.config(state=tk.DISABLED)

    set_buttons_state(tk.DISABLED)

    # handle redundancy created by restart func with buttons
    
    if 'restart_button' not in globals() or not restart_button.winfo_exists():
        restart_button = tk.Button(frame, text="Restart", command=restart_game,
                                  font=FONTS["body_bold"])
        restart_button.pack(pady=SPACING["sm"])

    if 'quit_button' not in globals() or not quit_button.winfo_exists():
        quit_button = tk.Button(frame, text="Quit", command=on_quit,
                               font=FONTS["body_bold"])
        quit_button.pack(pady=SPACING["sm"])

def restart_game():
    global skeleton, restart_button, quit_button, session_data
    
    # Reset session data
    session_data = {
        'rooms_visited': set(),
        'facts_this_game': 0,
        'bones_found_this_game': 0,
        'bones_lost_this_game': 0,
        'fights_this_game': 0,
        'flees_this_game': 0,
        'outwits_this_game': 0,
        'shields_this_game': 0,
        'max_energy_this_game': 0,
    }
    
    skeleton = Skeleton()
    game_stats.start_game()
    sound_effects.play_game_start()
    
    update_status()
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.config(state=tk.DISABLED) 

    set_buttons_state(tk.NORMAL)

    for widget in frame.winfo_children():
        if isinstance(widget, tk.Button) and widget['text'] in ["Restart", "Quit"]:
            widget.destroy()

def win_game():
    global restart_button, quit_button
    
    # Play victory sound
    sound_effects.play_game_won()
    
    # Calculate playtime
    playtime = None
    if hasattr(game_stats, 'session_start_time'):
        playtime = int((datetime.now() - game_stats.session_start_time).total_seconds())
    
    # Record game end
    session_data['game_won'] = True
    session_data['final_bones_count'] = len(skeleton.bones)
    session_data['playtime_seconds'] = playtime
    game_stats.end_game(won=True, playtime_seconds=playtime)
    
    # Check achievements
    newly_unlocked = achievements.check_achievements(game_stats, session_data)
    
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.insert(tk.END, f"{ICONS['trophy']} Congratulations! You have found all your bones!\n\n")
    
    # Show game stats
    if playtime:
        minutes = playtime // 60
        seconds = playtime % 60
        result_text_widget.insert(tk.END, f"Time: {minutes}m {seconds}s\n")
    result_text_widget.insert(tk.END, f"Monsters defeated: {session_data.get('fights_this_game', 0)}\n")
    result_text_widget.insert(tk.END, f"Facts collected: {session_data.get('facts_this_game', 0)}\n")
    result_text_widget.insert(tk.END, f"Max energy: {session_data.get('max_energy_this_game', 0)}\n\n")
    
    if newly_unlocked:
        result_text_widget.insert(tk.END, f"{ICONS['trophy']} {len(newly_unlocked)} new achievement(s) unlocked!\n\n")
    
    result_text_widget.insert(tk.END, "Would you like to restart or quit?\n")
    result_text_widget.config(state=tk.DISABLED)

    set_buttons_state(tk.DISABLED)

    if 'restart_button' not in globals() or not restart_button.winfo_exists():
        restart_button = tk.Button(frame, text="Restart", command=restart_game,
                                  font=FONTS["body_bold"])
        restart_button.pack(pady=SPACING["sm"])

    if 'quit_button' not in globals() or not quit_button.winfo_exists():
        quit_button = tk.Button(frame, text="Quit", command=on_quit,
                               font=FONTS["body_bold"])
        quit_button.pack(pady=SPACING["sm"])

################

def update_status():
    """Update the status display with current skeleton stats and enhanced formatting."""
    # Bones section
    if skeleton.bones:
        bones_list = ', '.join(skeleton.bones)
        bones_status = f"{ICONS['bone']} BONES: {bones_list}"
    else:
        bones_status = f"{ICONS['skull']} BONES: None remaining!"
    
    # Lost bones section
    if skeleton.lost_bones:
        lost_list = ', '.join(skeleton.lost_bones)
        lost_status = f"{ICONS['warning']} MISSING: {lost_list}"
    else:
        lost_status = f"{ICONS['success']} ALL BONES FOUND!"
    
    # Progress bar
    total_bones = 6
    found_bones = total_bones - len(skeleton.lost_bones)
    progress = f"Progress: {found_bones}/{total_bones} "
    progress += "█" * found_bones + "░" * len(skeleton.lost_bones)
    
    # Energy and shield
    energy_status = f"{ICONS['energy']} Energy: {skeleton.spirit_energy}"
    if skeleton.bone_shield_active:
        energy_status += f"  {ICONS['shield']} SHIELD ACTIVE"
    
    # Facts collected
    facts_status = f"📖 Facts: {skeleton.facts_collected}"
    
    # Combine all
    status_text.set(f"{bones_status}\n{lost_status}\n{progress}\n{energy_status}  {facts_status}")
    
    # Update room display with exits
    room_exits = get_room_exits(skeleton.current_room)
    room_text.set(f"📍 Location: {skeleton.current_room}\n{room_exits}")

    # Update room icon if available
    if skeleton.current_room in room_icons:
        room_icon = room_icons[skeleton.current_room]
        room_icon_label.config(image=room_icon)
        room_icon_label.image = room_icon  # keep ref to avoid garbage collection
    
    # Track session stats
    session_data['rooms_visited'] = session_data.get('rooms_visited', set())
    session_data['rooms_visited'].add(skeleton.current_room)
    game_stats.record_room_visit()
    
    # Track max energy
    session_data['max_energy_this_game'] = max(
        session_data.get('max_energy_this_game', 0),
        skeleton.spirit_energy
    )
    game_stats.record_energy_at(skeleton.spirit_energy)

def get_room_exits(room_name):
    """Get formatted string of available exits from current room."""
    if room_name not in rooms:
        return ""
    
    room_data = rooms[room_name]
    exits = []
    
    # Map directions to their destinations
    direction_map = {
        "up": "↑",
        "down": "↓", 
        "left": "←",
        "right": "→"
    }
    
    for direction in ["up", "down", "left", "right"]:
        if direction in room_data:
            destination = room_data[direction]
            symbol = direction_map[direction]
            exits.append(f"{symbol} {direction.title()}: {destination}")
    
    if exits:
        return "Exits: " + " | ".join(exits)
    else:
        return "No exits available"

def on_move(direction):
    result = move_room(skeleton, direction)
    
    # Play room transition sound
    if "You move" in result:
        sound_effects.play_room_enter()

    if not skeleton.is_alive():
        game_over()
        return

    if skeleton.has_won():
        win_game()
        return
    
    # Color-coded feedback
    if "Random fact found:" in result:
        sound_effects.play_fact_collected()
        update_result_display(result, "warning")
    elif "Event:" in result or "Success:" in result:
        update_result_display(result, "info")
    elif "can't move" in result.lower():
        update_result_display(result, "error")
    else:
        update_result_display(result, "default")
    update_status()

def show_combat_dialog():
    """Display combat options dialog when encountering a monster."""
    monster = random.choice(monsters)
    
    sound_effects.play_combat_start()
    
    combat_window = Toplevel(window)
    combat_window.title("Monster Encounter!")
    combat_window.geometry("520x450")
    combat_window.transient(window)
    combat_window.grab_set()
    
    # Monster encounter message
    header = tk.Label(combat_window, text=f"{ICONS['monster']} A {monster} blocks your path!",
                      font=FONTS["heading"], fg=COLORS["error"])
    header.pack(pady=SPACING["md"])
    
    # Get available options
    options = get_combat_options(skeleton)
    
    # Difficulty adjustment
    diff_settings = DIFFICULTY[current_difficulty]
    
    # Display options
    option_frame = tk.Frame(combat_window)
    option_frame.pack(pady=SPACING["sm"], padx=SPACING["lg"], fill=tk.BOTH, expand=True)
    
    def handle_combat_choice(action):
        """Process the combat choice and update game state."""
        combat_window.destroy()
        
        # Track combat action
        session_data[f"{action}s_this_game"] = session_data.get(f"{action}s_this_game", 0) + 1
        
        result = combat_encounter(skeleton, action, monster)
        
        # Play appropriate sound
        if action == "fight":
            if result["success"]:
                sound_effects.play_fight_win()
            else:
                sound_effects.play_fight_lose()
        elif action == "flee":
            if result["success"]:
                sound_effects.play_flee_success()
            else:
                sound_effects.play_flee_caught()
        elif action == "outwit":
            if result["success"]:
                sound_effects.play_outwit_success()
            else:
                sound_effects.play_outwit_fail()
        
        # Track combat stats
        game_stats.record_combat(action, result["success"])
        if not result["success"] and result["bones_lost"]:
            for _ in result["bones_lost"]:
                game_stats.record_bone_lost()
                session_data['bones_lost_this_game'] = session_data.get('bones_lost_this_game', 0) + 1
        
        if result["energy_change"] > 0:
            game_stats.record_energy_gained(result["energy_change"])
            sound_effects.play_energy_gained()
        
        # Display result with appropriate color
        color = "success" if result["success"] else "error"
        update_result_display(result["message"], color)
        
        # Check for game over or win
        if not skeleton.is_alive():
            game_over()
            return
        
        if skeleton.has_won():
            win_game()
            return
        
        update_status()
    
    # Fight button
    fight_success = int(diff_settings["fight_chance"] * 100)
    fight_text = f"{ICONS['fight']} FIGHT\n" \
                 f"{options['fight']['description']}\n" \
                 f"Success: {fight_success}% | Reward: +1 energy | Risk: Lose 1 bone"
    fight_btn = tk.Button(option_frame, text=fight_text, width=BUTTON["combat_width"], 
                          height=BUTTON["combat_height"],
                          command=lambda: handle_combat_choice("fight"),
                          bg=COLORS["fight_bg"], font=FONTS["body"])
    fight_btn.pack(pady=SPACING["sm"])
    
    # Flee button
    flee_success = int(diff_settings["flee_chance"] * 100)
    flee_text = f"{ICONS['flee']} FLEE\n" \
                f"{options['flee']['description']}\n" \
                f"Success: {flee_success}% | Reward: Escape safely | Risk: Lose 1 bone if caught"
    flee_btn = tk.Button(option_frame, text=flee_text, width=BUTTON["combat_width"], 
                         height=BUTTON["combat_height"],
                         command=lambda: handle_combat_choice("flee"),
                         bg=COLORS["flee_bg"], font=FONTS["body"])
    flee_btn.pack(pady=SPACING["sm"])
    
    # Outwit button (only if facts collected)
    if options['outwit']['available']:
        outwit_success = int(min(90, skeleton.facts_collected * 10))
        outwit_text = f"{ICONS['outwit']} OUTWIT\n" \
                      f"{options['outwit']['description']}\n" \
                      f"Success: {outwit_success}% | Reward: +2 energy | Risk: Lose 2 bones!"
        outwit_btn = tk.Button(option_frame, text=outwit_text, width=BUTTON["combat_width"], 
                               height=BUTTON["combat_height"],
                               command=lambda: handle_combat_choice("outwit"),
                               bg=COLORS["outwit_bg"], font=FONTS["body"])
        outwit_btn.pack(pady=SPACING["sm"])
    else:
        locked_text = f"{ICONS['outwit']} OUTWIT\n(Requires Halloween Facts)\nCollect facts to unlock!"
        locked_btn = tk.Button(option_frame, text=locked_text, width=BUTTON["combat_width"], 
                               height=BUTTON["combat_height"],
                               state=tk.DISABLED, bg=COLORS["disabled"], font=FONTS["body"])
        locked_btn.pack(pady=SPACING["sm"])
    
    # Shield indicator
    if skeleton.bone_shield_active:
        shield_label = tk.Label(combat_window, 
                                text=f"{ICONS['shield']} Bone Shield Active - Next hit blocked!",
                                fg=COLORS["shield"], font=FONTS["body_bold"])
        shield_label.pack(pady=SPACING["sm"])

def show_energy_menu():
    """Display spirit energy usage options."""
    energy_window = Toplevel(window)
    energy_window.title("Spirit Energy Abilities")
    energy_window.geometry("500x420")
    energy_window.transient(window)
    energy_window.grab_set()
    
    header = tk.Label(energy_window, 
                      text=f"{ICONS['energy']} Spirit Energy: {skeleton.spirit_energy}",
                      font=FONTS["heading"], fg=COLORS["energy"])
    header.pack(pady=SPACING["md"])
    
    abilities_frame = tk.Frame(energy_window)
    abilities_frame.pack(pady=SPACING["sm"], padx=SPACING["lg"])
    
    def use_spectral_search():
        """Use spectral search ability."""
        if skeleton.spirit_energy < 2:
            messagebox.showerror("Insufficient Energy", 
                               "You need 2 spirit energy for Spectral Search!")
            return
        
        energy_window.destroy()
        game_stats.record_spectral_search()
        session_data['spectral_this_game'] = session_data.get('spectral_this_game', 0) + 1
        
        result = explore_current_room(skeleton, use_spectral_search=True)
        if "revealed your" in result:
            sound_effects.play_bone_found()
        update_result_display(result, "energy")
        update_status()
        
        if skeleton.has_won():
            win_game()
    
    def use_bone_shield():
        """Activate bone shield."""
        if skeleton.spirit_energy < 3:
            messagebox.showerror("Insufficient Energy", 
                               "You need 3 spirit energy for Bone Shield!")
            return
        
        if skeleton.activate_shield():
            energy_window.destroy()
            sound_effects.play_shield_activate()
            game_stats.record_bone_shield()
            session_data['shields_this_game'] = session_data.get('shields_this_game', 0) + 1
            update_result_display(f"{ICONS['shield']} Bone Shield activated! Your next bone loss will be prevented.", "shield")
            update_status()
        else:
            messagebox.showerror("Error", "Failed to activate shield!")
    
    def use_mystic_hint():
        """Get mystic hints about bone locations."""
        if skeleton.spirit_energy < 1:
            messagebox.showerror("Insufficient Energy", 
                               "You need 1 spirit energy for Mystic Hint!")
            return
        
        hints = skeleton.mystic_hint()
        if hints:
            energy_window.destroy()
            sound_effects.play_hint_used()
            game_stats.record_mystic_hint()
            hint_text = f"{ICONS['mystic']} The spirits whisper of bones in these rooms:\n{', '.join(hints)}"
            update_result_display(hint_text, "energy")
            update_status()
        else:
            messagebox.showerror("Error", "Failed to get hint!")
    
    # Ability buttons with better styling
    spectral_btn = tk.Button(abilities_frame, 
                             text=f"{ICONS['spectral']} Spectral Search (2 energy)\n"
                                  f"Guarantee finding a bone in this room",
                             width=BUTTON["combat_width"], height=3, 
                             command=use_spectral_search,
                             bg=COLORS["spectral_bg"], font=FONTS["body"],
                             state=tk.NORMAL if skeleton.spirit_energy >= 2 else tk.DISABLED)
    spectral_btn.pack(pady=SPACING["sm"])
    
    shield_btn = tk.Button(abilities_frame,
                           text=f"{ICONS['shield']} Bone Shield (3 energy)\n"
                                f"Prevent next bone loss from combat",
                           width=BUTTON["combat_width"], height=3, 
                           command=use_bone_shield,
                           bg=COLORS["shield_bg"], font=FONTS["body"],
                           state=tk.NORMAL if skeleton.spirit_energy >= 3 else tk.DISABLED)
    shield_btn.pack(pady=SPACING["sm"])
    
    hint_btn = tk.Button(abilities_frame,
                         text=f"{ICONS['mystic']} Mystic Hint (1 energy)\n"
                              f"Reveal rooms that may contain bones",
                         width=BUTTON["combat_width"], height=3, 
                         command=use_mystic_hint,
                         bg=COLORS["hint_bg"], font=FONTS["body"],
                         state=tk.NORMAL if skeleton.spirit_energy >= 1 else tk.DISABLED)
    hint_btn.pack(pady=SPACING["sm"])
    
    close_btn = tk.Button(energy_window, text="Close", command=energy_window.destroy,
                          font=FONTS["body_bold"], width=15)
    close_btn.pack(pady=SPACING["md"])

def on_explore():
    """Handle room exploration - may trigger combat or other events."""
    result = explore_current_room(skeleton)
    
    # Check if combat was triggered
    if result == "COMBAT_TRIGGER":
        show_combat_dialog()
        return

    if not skeleton.is_alive():
        game_over()
        return

    if skeleton.has_won():
        win_game()
        return
    
    # Handle different result types with sounds and colors
    if "Random fact found:" in result:
        sound_effects.play_fact_collected()
        game_stats.record_fact_collected()
        session_data['facts_this_game'] = session_data.get('facts_this_game', 0) + 1
        update_result_display(result, "warning")
    elif "found your" in result.lower():
        sound_effects.play_bone_found()
        game_stats.record_bone_found()
        update_result_display(result, "success")
    elif "Event:" in result:
        update_result_display(result, "info")
    else:
        update_result_display(result, "default")
    
    update_status()
    
    # Check achievements
    newly_unlocked = achievements.check_achievements(game_stats, session_data)
    if newly_unlocked:
        show_achievement_notification(newly_unlocked)

def show_achievement_notification(achievement_ids):
    """Show notification for newly unlocked achievements."""
    for ach_id in achievement_ids:
        ach_data = achievements.ACHIEVEMENTS[ach_id]
        messagebox.showinfo(
            "Achievement Unlocked!",
            f"{ICONS['trophy']} {ach_data['icon']} {ach_data['name']}\n\n{ach_data['description']}"
        )

def on_quit():
    pygame.mixer.music.stop()
    window.destroy()

def update_result_display(message, color_key="default"):
    """Update result display with color-coded messages."""
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)  # clear prev

    result_text_widget.insert(tk.END, message)
    start_index = '1.0'
    end_index = 'end'

    # Map color keys to actual colors
    color_map = {
        "default": COLORS["text_primary"],
        "success": COLORS["success"],
        "error": COLORS["error"],
        "warning": COLORS["warning"],
        "info": COLORS["info"],
        "energy": COLORS["energy"],
        "shield": COLORS["shield"],
    }
    
    actual_color = color_map.get(color_key, COLORS["text_primary"])
    result_text_widget.tag_configure(color_key, foreground=actual_color)
    result_text_widget.tag_add(color_key, start_index, end_index)

    result_text_widget.config(state=tk.DISABLED)  # make read-only


# init game, tkinter window here as well
skeleton = Skeleton()
game_stats.start_game()
session_data = {
    'rooms_visited': set(),
    'facts_this_game': 0,
    'bones_found_this_game': 0,
    'bones_lost_this_game': 0,
    'fights_this_game': 0,
    'flees_this_game': 0,
    'outwits_this_game': 0,
    'shields_this_game': 0,
    'max_energy_this_game': 0,
}

window = tk.Tk()
window.title(WINDOW["title"])
window.minsize(WINDOW["min_width"], WINDOW["min_height"])

# disp elements

frame = tk.Frame(window, padx=SPACING["md"], pady=SPACING["md"])
frame.pack(fill=tk.BOTH, expand=True)

# Room icon at top
room_icon_label = tk.Label(frame)
room_icon_label.pack(pady=SPACING["sm"])

# Room location and exits
room_text = tk.StringVar()
room_label = tk.Label(frame, textvariable=room_text, justify="left", 
                     font=FONTS["body_bold"])
room_label.pack(pady=SPACING["xs"])

# Status panel with better formatting
status_text = tk.StringVar()
status_label = tk.Label(frame, textvariable=status_text, justify="left",
                       font=FONTS["body"])
status_label.pack(pady=SPACING["sm"])

# Result text widget
result_text_widget = tk.Text(frame, height=6, width=60, font=FONTS["body"],
                            wrap=tk.WORD)
result_text_widget.pack(pady=SPACING["md"])
result_text_widget.config(state=tk.DISABLED)  # make it read-only

# Load room icons with error handling
room_icons = {}
icon_files = {
    "Entrance Hall": "icons/entrance_hall.png",
    "Creepy Library": "icons/creepy_library.png",
    "Dark Cellar": "icons/dark_cellar.png",
    "Spooky Kitchen": "icons/spooky_kitchen.png",
    "Cursed Ballroom": "icons/cursed_ballroom.png",
    "Mystic Garden": "icons/mystic_garden.png",
    "Haunted Attic": "icons/haunted_attic.png",
    "Forgotten Graveyard": "icons/forgotten_graveyard.png",
    "Phantom Cave": "icons/phantom_cave.png"
}

for room_name, icon_path in icon_files.items():
    try:
        room_icons[room_name] = PhotoImage(file=icon_path)
    except tk.TclError:
        print(f"Warning: Could not load icon for {room_name}")
        # Create a placeholder if icon fails to load
        # Game continues without icons

# diamond layout
button_frame = tk.Frame(frame)
button_frame.pack(pady=SPACING["md"])

# diamond shape with consistent styling
up_button = tk.Button(button_frame, text="↑ Up", command=lambda: on_move("up"),
                     width=BUTTON["standard_width"], font=FONTS["body"])
up_button.grid(row=0, column=1, padx=SPACING["xs"], pady=SPACING["xs"])

left_button = tk.Button(button_frame, text="← Left", command=lambda: on_move("left"),
                       width=BUTTON["standard_width"], font=FONTS["body"])
left_button.grid(row=1, column=0, padx=SPACING["xs"], pady=SPACING["xs"])

explore_button = tk.Button(button_frame, text=f"{ICONS['spectral']} Explore", 
                          command=on_explore,
                          width=BUTTON["standard_width"], font=FONTS["body_bold"],
                          bg=COLORS["button_bg"])
explore_button.grid(row=1, column=1, padx=SPACING["xs"], pady=SPACING["xs"])

down_button = tk.Button(button_frame, text="↓ Down", command=lambda: on_move("down"),
                       width=BUTTON["standard_width"], font=FONTS["body"])
down_button.grid(row=2, column=1, padx=SPACING["xs"], pady=SPACING["xs"])

right_button = tk.Button(button_frame, text="→ Right", command=lambda: on_move("right"),
                        width=BUTTON["standard_width"], font=FONTS["body"])
right_button.grid(row=1, column=2, padx=SPACING["xs"], pady=SPACING["xs"])

# Spirit Energy button
energy_button = tk.Button(frame, text=f"{ICONS['energy']} Use Spirit Energy", 
                         command=show_energy_menu,
                          bg=COLORS["spectral_bg"], font=FONTS["body_bold"],
                          width=BUTTON["wide_width"])
energy_button.pack(pady=SPACING["sm"])

# Utility buttons row
utility_frame = tk.Frame(frame)
utility_frame.pack(pady=SPACING["sm"])

help_button = tk.Button(utility_frame, text="❓ Help", command=show_help_dialog,
                       font=FONTS["body"], width=10)
help_button.pack(side=tk.LEFT, padx=SPACING["xs"])

stats_button = tk.Button(utility_frame, text=f"{ICONS['trophy']} Stats", 
                        command=show_statistics_dialog,
                        font=FONTS["body"], width=10)
stats_button.pack(side=tk.LEFT, padx=SPACING["xs"])

save_button = tk.Button(utility_frame, text="💾 Save", command=save_game,
                       font=FONTS["body"], width=10)
save_button.pack(side=tk.LEFT, padx=SPACING["xs"])

load_button = tk.Button(utility_frame, text="📂 Load", command=load_game,
                       font=FONTS["body"], width=10)
load_button.pack(side=tk.LEFT, padx=SPACING["xs"])

quit_button = tk.Button(utility_frame, text="Quit", command=on_quit,
                       font=FONTS["body"], width=10)
quit_button.pack(side=tk.LEFT, padx=SPACING["xs"])

update_status()
window.mainloop()
