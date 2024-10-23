import tkinter as tk
from tkinter import PhotoImage
import pygame
from skeleton import Skeleton
from rooms import move_room, explore_current_room
from achievements import AchievementManager
import monsters # needed here before, left here just in case

# init music
pygame.mixer.init()
pygame.mixer.music.load('haloweenmusic.mp3') 
pygame.mixer.music.play(-1)  # inf loop
pygame.mixer.music.set_volume(0.2)

# init achievement manager
achievement_manager = AchievementManager()

# GAME END/WIN FUNCTIONALITY:

def set_buttons_state(state):
    up_button.config(state=state)
    left_button.config(state=state)
    down_button.config(state=state)
    right_button.config(state=state)
    explore_button.config(state=state)

def game_over():
    global restart_button, quit_button
    
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.insert(tk.END, "Game Over! You have lost all your bones.\n")
    result_text_widget.insert(tk.END, "Would you like to restart or quit?\n")
    result_text_widget.config(state=tk.DISABLED)

    set_buttons_state(tk.DISABLED)

    # handle redundancy created by restart func with buttons
    
    if 'restart_button' not in globals() or not restart_button.winfo_exists():
        restart_button = tk.Button(frame, text="Restart", command=restart_game)
        restart_button.pack(pady=5)

    if 'quit_button' not in globals() or not quit_button.winfo_exists():
        quit_button = tk.Button(frame, text="Quit", command=on_quit)
        quit_button.pack(pady=5)

def restart_game():
    global skeleton, restart_button, quit_button
    skeleton = Skeleton()
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
    
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.insert(tk.END, "Congratulations! You have found all your bones!\n")
    result_text_widget.insert(tk.END, "Would you like to restart or quit?\n")
    result_text_widget.config(state=tk.DISABLED)

    set_buttons_state(tk.DISABLED)

    if 'restart_button' not in globals() or not restart_button.winfo_exists():
        restart_button = tk.Button(frame, text="Restart", command=restart_game)
        restart_button.pack(pady=5)

    if 'quit_button' not in globals() or not quit_button.winfo_exists():
        quit_button = tk.Button(frame, text="Quit", command=on_quit)
        quit_button.pack(pady=5)

################

def update_status():
    status_text.set(skeleton.get_status())
    room_text.set(f"Current location: {skeleton.current_room}")

    room_icon = room_icons[skeleton.current_room]
    room_icon_label.config(image=room_icon)
    room_icon_label.image = room_icon  # keep ref to avoid garbage collection

def on_move(direction):
    result = move_room(skeleton, direction)

    if not skeleton.is_alive():
        game_over()
        return

    if skeleton.has_won():
        win_game()
        return

    # could probably improve this
    if "Random fact found:" in result:
        update_result_display(result, "orange")
    elif "Event:" in result or "Success:" in result:
        update_result_display(result, "red")
    else:
        update_result_display(result, "black")
    update_status()

    # check for new achievements
    achievement_messages = achievement_manager.check_achievements(skeleton)
    for message in achievement_messages:
        update_result_display(message, "blue")  # display achievement in blue

def on_explore():
    result = explore_current_room(skeleton)

    if not skeleton.is_alive():
        game_over()
        return

    if skeleton.has_won():
        win_game()
        return

    if "Random fact found:" in result:
        update_result_display(result, "orange")
    elif "Achievement unlocked:" in result:
        update_result_display(result, "green", delay_achievement=True)
    elif "Event:" in result or "Success:" in result:
        update_result_display(result, "red")
    else:
        update_result_display(result, "black")
    update_status()

    # check for new achievements
    achievement_messages = achievement_manager.check_achievements(skeleton)
    for message in achievement_messages:
        update_result_display(message, "blue")  # display achievement in blue
    
def on_quit():
    pygame.mixer.music.stop()
    window.destroy()

def update_result_display(message, color, delay_achievement=False):
    """Update the result display with a message of the given color."""
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)  # clear prev

    result_text_widget.insert(tk.END, message)
    start_index = '1.0'
    end_index = 'end'

    result_text_widget.tag_configure(color, foreground=color)
    result_text_widget.tag_add(color, start_index, end_index)

    result_text_widget.config(state=tk.DISABLED)  # make read-only

    # check if achievement should display after delay
    if delay_achievement and "Achievement unlocked:" in message:
        window.after(3500, lambda: update_result_display("Achievement unlocked!", "green"))

def show_achievements():
    """Display a pop-up window listing unlocked achievements."""
    achievements_window = tk.Toplevel(window)
    achievements_window.title("Journal - Achievements")

    tk.Label(achievements_window, text="Unlocked Achievements:").pack(pady=(10, 5))

    if skeleton.achievements:
        for achievement in skeleton.achievements:
            tk.Label(achievements_window, text=f"- {achievement}").pack(anchor="w", padx=10)
    else:
        tk.Label(achievements_window, text="No achievements unlocked yet.").pack(pady=10)

# init game, tkinter window here as well
skeleton = Skeleton()
window = tk.Tk()
window.title("Haunted House Adventure")

# disp elements

frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

room_icon_label = tk.Label(frame)
room_icon_label.pack(side=tk.TOP, anchor='n')  # top middle

room_text = tk.StringVar()
room_label = tk.Label(frame, textvariable=room_text, justify="left")
room_label.pack()

status_text = tk.StringVar()
status_label = tk.Label(frame, textvariable=status_text, justify="left")
status_label.pack()

result_text_widget = tk.Text(frame, height=5, width=50)
result_text_widget.pack(pady=(10, 0))
result_text_widget.config(state=tk.DISABLED)  # make read-only

journal_button = tk.Button(frame, text="Journal", command=show_achievements)
journal_button.pack(pady=(5, 0))

room_icons = {
    "Entrance Hall": PhotoImage(file="icons/entrance_hall.png"),
    "Creepy Library": PhotoImage(file="icons/creepy_library.png"),
    "Dark Cellar": PhotoImage(file="icons/dark_cellar.png"),
    "Spooky Kitchen": PhotoImage(file="icons/spooky_kitchen.png"),
    "Cursed Ballroom": PhotoImage(file="icons/cursed_ballroom.png"),
    "Mystic Garden": PhotoImage(file="icons/mystic_garden.png"),
    "Haunted Attic": PhotoImage(file="icons/haunted_attic.png"),
    "Forgotten Graveyard": PhotoImage(file="icons/forgotten_graveyard.png"),
    "Phantom Cave": PhotoImage(file="icons/phantom_cave.png")
}

# diamond layout
button_frame = tk.Frame(frame)
button_frame.pack(pady=5)

# diamond shape
up_button = tk.Button(button_frame, text="Up", command=lambda: on_move("up"))
up_button.grid(row=0, column=1)

left_button = tk.Button(button_frame, text="Left", command=lambda: on_move("left"))
left_button.grid(row=1, column=0)

explore_button = tk.Button(button_frame, text="Explore", command=on_explore)
explore_button.grid(row=1, column=1)

down_button = tk.Button(button_frame, text="Down", command=lambda: on_move("down"))
down_button.grid(row=2, column=1)

right_button = tk.Button(button_frame, text="Right", command=lambda: on_move("right"))
right_button.grid(row=1, column=2)

quit_button = tk.Button(frame, text="Quit", command=on_quit)
quit_button.pack(pady=5)

update_status()
window.mainloop()
