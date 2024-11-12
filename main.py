import tkinter as tk
import pygame.mixer
import toml
import match_manager
import time
import threading
import pandas as pd

# * Config
with open("./fms.config.toml", "r") as config_file:
    config = toml.loads(config_file.read())

# * Matches
matches = pd.read_csv(config["event"]["matches_file"])

# * Sounds
pygame.mixer.init()
sound_auto_start = pygame.mixer.Sound("./res/sounds/Start Auto_normalized.wav")
sound_teleop_start = pygame.mixer.Sound("./res/sounds/Start Teleop_normalized.wav")
sound_endgame_start = pygame.mixer.Sound("./res/sounds/Start of End Game_normalized.wav")
sound_match_end = pygame.mixer.Sound("./res/sounds/Match End_normalized.wav")
sound_match_pause = pygame.mixer.Sound("./res/sounds/Match Pause_normalized.wav")

sound_auto_start.set_volume(config["sounds"]["volume"])
sound_teleop_start.set_volume(config["sounds"]["volume"])
sound_endgame_start.set_volume(config["sounds"]["volume"])
sound_match_end.set_volume(config["sounds"]["volume"])
sound_match_pause.set_volume(config["sounds"]["volume"])

# * Match
match = match_manager.MatchManager(config["event"]["save_directory"])
match_start_time = None
total_match_time = config["timing"]["auto_time_seconds"] + config["timing"]["teleop_time_seconds"]
time_update_thread: threading.Thread = None

# * Main Window
main_window = tk.Tk()
main_window.title("MechaLeague Match Manager")
main_window.attributes('-topmost', True)

# * Match select
match_select_frame = tk.LabelFrame(main_window, text="Match Number", padx=5, pady=5)
match_select_frame.pack()

match_select_previous_button = tk.Button(match_select_frame, text=" < ")
match_select_previous_button.pack(side=tk.LEFT)

match_select_variable = tk.IntVar(match_select_frame, value=1)
match_select_entry = tk.Entry(match_select_frame, width=5, textvariable=match_select_variable)
match_select_entry.pack(padx=5, side=tk.LEFT)

match_select_next_button = tk.Button(match_select_frame, text=" > ")
match_select_next_button.pack(side=tk.RIGHT)

match_select_previous_button.config(command=lambda: match_select_variable.set(match_select_variable.get() - 1 if match_select_variable.get() > 1 else 1))
match_select_next_button.config(command=lambda: match_select_variable.set(match_select_variable.get() + 1))

# * Teams
teams_frame = tk.LabelFrame(main_window, text="Teams", padx=5, pady=5)
teams_frame.pack()

# Blue Alliance
blue_alliance_frame = tk.LabelFrame(teams_frame, text="Blue Alliance", padx=5, pady=5, background="#0000FF", foreground="white")
blue_alliance_frame.pack(side=tk.LEFT)

blue_alliance_team_1 = tk.Entry(blue_alliance_frame, width=5)
blue_alliance_team_1.pack()
blue_alliance_team_2 = tk.Entry(blue_alliance_frame, width=5)
blue_alliance_team_2.pack()
blue_alliance_team_3 = tk.Entry(blue_alliance_frame, width=5)
blue_alliance_team_3.pack()

# Red Alliance
red_alliance_frame = tk.LabelFrame(teams_frame, text="Red Alliance", padx=5, pady=5, background="#FF0000", foreground="white")
red_alliance_frame.pack(side=tk.RIGHT)

red_alliance_team_1 = tk.Entry(red_alliance_frame, width=5)
red_alliance_team_1.pack()
red_alliance_team_2 = tk.Entry(red_alliance_frame, width=5)
red_alliance_team_2.pack()
red_alliance_team_3 = tk.Entry(red_alliance_frame, width=5)
red_alliance_team_3.pack()

# Teams interactivity
blue_alliance_team_1.bind("<Return>", lambda e: blue_alliance_team_2.focus())
blue_alliance_team_2.bind("<Return>", lambda e: blue_alliance_team_3.focus())
blue_alliance_team_3.bind("<Return>", lambda e: red_alliance_team_1.focus())
red_alliance_team_1.bind("<Return>", lambda e: red_alliance_team_2.focus())
red_alliance_team_2.bind("<Return>", lambda e: red_alliance_team_3.focus())
red_alliance_team_3.bind("<Return>", lambda e: main_window.focus())
red_alliance_team_3.bind("<Tab>", lambda e: main_window.focus())

# * Match Setup
def load_match():
    match_number = match_select_variable.get()

    blue_alliance_team_1.delete(0, tk.END)
    blue_alliance_team_2.delete(0, tk.END)
    blue_alliance_team_3.delete(0, tk.END)
    red_alliance_team_1.delete(0, tk.END)
    red_alliance_team_2.delete(0, tk.END)
    red_alliance_team_3.delete(0, tk.END)

    blue_alliance_team_1.insert(0, matches.at[match_number - 1, "blue_alliance_team_1"])
    blue_alliance_team_2.insert(0, matches.at[match_number - 1, "blue_alliance_team_2"])
    blue_alliance_team_3.insert(0, matches.at[match_number - 1, "blue_alliance_team_3"])
    red_alliance_team_1.insert(0, matches.at[match_number - 1, "red_alliance_team_1"])
    red_alliance_team_2.insert(0, matches.at[match_number - 1, "red_alliance_team_2"])
    red_alliance_team_3.insert(0, matches.at[match_number - 1, "red_alliance_team_3"])

match_select_variable.trace_add("write", lambda *args: load_match())
load_match()

# * Match Control
match_control_frame = tk.LabelFrame(main_window, text="Match Control", padx=5, pady=5)
match_control_frame.pack()

# Start Match
start_match_button = tk.Button(match_control_frame, text="Start Match")
start_match_button.pack(side=tk.LEFT)

# Pause Match
pause_match_button = tk.Button(match_control_frame, text="Pause Match")
pause_match_button.pack(side=tk.LEFT)

# * Timer
match_control_timer_label = tk.Label(main_window, text="00:00", font=("Arial", 32), foreground="black")
match_control_timer_label.pack()

# * Scoring
scoring_frame = tk.LabelFrame(main_window, text="Scoring", padx=5, pady=5)
scoring_frame.pack()

# Blue Alliance
blue_alliance_score_frame = tk.LabelFrame(scoring_frame, text="Blue Alliance", padx=5, pady=5, background="#0000FF", foreground="white")
blue_alliance_score_frame.pack(side=tk.LEFT)

blue_alliance_score = tk.Label(blue_alliance_score_frame, text="0", font=("Arial", 32), foreground="white", background="#0000FF")
blue_alliance_score.pack()

blue_alliance_score_goals = tk.Label(blue_alliance_score_frame, text="Goals: 0", font=("Arial", 8), foreground="white", background="#0000FF")
blue_alliance_score_goals.pack()

blue_alliance_score_fouls = tk.Label(blue_alliance_score_frame, text="Fouls: 0", font=("Arial", 8), foreground="white", background="#0000FF")
blue_alliance_score_fouls.pack()

# Buttons
# Goals
blue_alliance_score_goal_button_frame = tk.Frame(blue_alliance_score_frame)
blue_alliance_score_goal_button_frame.pack(side=tk.LEFT)

blue_alliance_score_goal_add_button = tk.Button(blue_alliance_score_goal_button_frame, text="Goal+", command=match.blue_alliance_goal_add)
blue_alliance_score_goal_add_button.pack()

blue_alliance_score_goal_sub_button = tk.Button(blue_alliance_score_goal_button_frame, text="Goal-", command=match.blue_alliance_goal_sub)
blue_alliance_score_goal_sub_button.pack()

# Fouls
blue_alliance_score_foul_button_frame = tk.Frame(blue_alliance_score_frame)
blue_alliance_score_foul_button_frame.pack(side=tk.RIGHT)

blue_alliance_score_foul_add_button = tk.Button(blue_alliance_score_foul_button_frame, text="Foul+", command=match.blue_alliance_foul_add)
blue_alliance_score_foul_add_button.pack()

blue_alliance_score_foul_sub_button = tk.Button(blue_alliance_score_foul_button_frame, text="Foul-", command=match.blue_alliance_foul_sub)
blue_alliance_score_foul_sub_button.pack()

# Red Alliance
red_alliance_score_frame = tk.LabelFrame(scoring_frame, text="Red Alliance", padx=5, pady=5, background="#FF0000", foreground="white")
red_alliance_score_frame.pack(side=tk.RIGHT)

red_alliance_score = tk.Label(red_alliance_score_frame, text="0", font=("Arial", 32), foreground="white", background="#FF0000")
red_alliance_score.pack()

red_alliance_score_goals = tk.Label(red_alliance_score_frame, text="Goals: 0", font=("Arial", 8), foreground="white", background="#FF0000")
red_alliance_score_goals.pack()

red_alliance_score_fouls = tk.Label(red_alliance_score_frame, text="Fouls: 0", font=("Arial", 8), foreground="white", background="#FF0000")
red_alliance_score_fouls.pack()

# Buttons
# Goals
red_alliance_score_goal_button_frame = tk.Frame(red_alliance_score_frame)
red_alliance_score_goal_button_frame.pack(side=tk.LEFT)

red_alliance_score_goal_add_button = tk.Button(red_alliance_score_goal_button_frame, text="Goal+", command=match.red_alliance_goal_add)
red_alliance_score_goal_add_button.pack()

red_alliance_score_goal_sub_button = tk.Button(red_alliance_score_goal_button_frame, text="Goal-", command=match.red_alliance_goal_sub)
red_alliance_score_goal_sub_button.pack()

# Fouls
red_alliance_score_foul_button_frame = tk.Frame(red_alliance_score_frame)
red_alliance_score_foul_button_frame.pack(side=tk.RIGHT)

red_alliance_score_foul_add_button = tk.Button(red_alliance_score_foul_button_frame, text="Foul+", command=match.red_alliance_foul_add)
red_alliance_score_foul_add_button.pack()

red_alliance_score_foul_sub_button = tk.Button(red_alliance_score_foul_button_frame, text="Foul-", command=match.red_alliance_foul_sub)
red_alliance_score_foul_sub_button.pack()

# Add keybinds
main_window.bind("<w>", lambda e: match.blue_alliance_goal_add())
main_window.bind("<s>", lambda e: match.blue_alliance_goal_sub())
main_window.bind("<d>", lambda e: match.blue_alliance_foul_add())
main_window.bind("<a>", lambda e: match.blue_alliance_foul_sub())

main_window.bind("<Up>", lambda e: match.red_alliance_goal_add())
main_window.bind("<Down>", lambda e: match.red_alliance_goal_sub())
main_window.bind("<Right>", lambda e: match.red_alliance_foul_add())
main_window.bind("<Left>", lambda e: match.red_alliance_foul_sub())

# * Timer Window
timer_window = tk.Toplevel(main_window)
timer_window.title("Timer")
timer_window.configure(bg="#00FF00")
timer_window.resizable(False, False)
timer_window.bind("<B1-Motion>", lambda e: timer_window.geometry(f"+{e.x_root}+{e.y_root}"))
timer_window.protocol("WM_DELETE_WINDOW", lambda: None)

# Timer Label
timer_label = tk.Label(timer_window, text="00:00", font=("Arial", 32), foreground="black", background="#00FF00")
timer_label.pack()

# * Match results
match_results_frame = tk.LabelFrame(main_window, text="Match Results", padx=5, pady=5)
match_results_frame.pack()

match_results_locked_label = tk.Label(match_results_frame, text="Match Results Locked", font=("Arial", 16), foreground="black")
match_results_locked_label.pack()

match_results_lock_button = tk.Button(match_results_frame, text="Unlock Match Results")
match_results_lock_button.pack()

def toggle_match_results_lock():
    if match.is_locked():
        match.unlock()
        match_results_locked_label.config(text="Match Results Unlocked", foreground="black")
        match_results_lock_button.config(text="Lock Match Results", foreground="green")
    else:
        match.lock()
        match_results_locked_label.config(text="Match Results Locked", foreground="black")
        match_results_lock_button.config(text="Unlock Match Results", foreground="red")

match_results_lock_button.config(command=toggle_match_results_lock)

# * Save Match Results
save_match_results_button = tk.Button(main_window, text="Save Match Results", font=("Arial", 16))
save_match_results_button.pack(fill=tk.X, padx=5, pady=5)

def save_match_results():
    try:
        match.save_match()
        save_match_results_button.config(text="Match Results Saved", foreground="green")
        save_match_results_button.after(1000, lambda: save_match_results_button.config(text="Save Match Results", foreground="black"))
    except Exception as e:
        save_match_results_button.config(text="Error Saving Match Results", foreground="red")
        save_match_results_button.after(1000, lambda: save_match_results_button.config(text="Save Match Results", foreground="black"))

save_match_results_button.config(command=save_match_results)


# * Functions
def update_scores():
    blue_alliance_score.config(text=str(match.blue_alliance_get_total_score()))
    blue_alliance_score_goals.config(text=f"Goals: {match.blue_alliance_get_goals()}")
    blue_alliance_score_fouls.config(text=f"Fouls: {match.blue_alliance_get_own_fouls()}")

    red_alliance_score.config(text=str(match.red_alliance_get_total_score()))
    red_alliance_score_goals.config(text=f"Goals: {match.red_alliance_get_goals()}")
    red_alliance_score_fouls.config(text=f"Fouls: {match.red_alliance_get_own_fouls()}")

match.set_update_callback(update_scores)

played_teleop_sound = False
played_endgame_sound = False
def match_start():
    sound_auto_start.play()

    global match_start_time
    match_start_time = time.time()

    match.start_match_with_match_number(match_select_variable.get())

    def time_update():
        global played_teleop_sound
        global played_endgame_sound

        while match.is_match_active():
            # timekeeping
            elapsed_time = time.time() - match_start_time
            match_time = total_match_time - elapsed_time

            # Check if it's time to play sounds
            if elapsed_time >= config["timing"]["auto_time_seconds"] and not played_teleop_sound:
                sound_teleop_start.play()
                played_teleop_sound = True

            if match_time - config["timing"]["endgame_time_seconds"] <= 0 and not played_endgame_sound:
                sound_endgame_start.play()
                played_endgame_sound = True

            # Update timers
            match_control_timer_label.config(text=time.strftime("%M:%S", time.gmtime(match_time)))
            timer_label.config(text=time.strftime("%M:%S", time.gmtime(match_time)))

            # Check if match is over
            if match_time <= 0:
                match.end_match()
                sound_match_end.play()
                match_control_timer_label.config(text="00:00")
                timer_label.config(text="00:00")
                break

            time.sleep(0.1)
    
    global time_update_thread
    time_update_thread = threading.Thread(target=time_update)
    time_update_thread.start()

start_match_button.config(command=match_start)

def match_pause():
    match.end_match()

    global time_update_thread
    time_update_thread.join()

    sound_match_pause.play()

pause_match_button.config(command=match_pause)

if __name__ == "__main__":
    main_window.mainloop()