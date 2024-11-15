import tkinter as tk
import pygame.mixer
import toml
import match_manager
import time
import threading
import pandas as pd
import sys
import os
import utils
import launchpad_constants
import launchpad_py
import launchpad_wrapper
from scores_screens.prepatec_scores_screen import PrepatecScoresScreen
from overlays.prepatec_overlay import PrepatecOverlay

try:
    import pyi_splash
    pyi_splash.update_text("Loading MechaLeague Match Manager")
except:
    pass

if getattr(sys, 'frozen', False):
    dirname = getattr(sys, "_MEIPASS")
elif __file__:
    dirname = os.path.dirname(__file__)

# * Config
try:
    pyi_splash.update_text("Loading Config from fms.config.toml")
except:
    pass
with open("./fms.config.toml", "r") as config_file:
    config = toml.loads(config_file.read())

# * Matches
try:
    pyi_splash.update_text("Loading Matches from " + config["event"]["matches_file"])
except:
    pass
matches = pd.read_csv(config["event"]["matches_file"])

# * Sounds
try:
    pyi_splash.update_text("Loading Sounds")
except:
    pass

pygame.mixer.init()
sound_auto_start = pygame.mixer.Sound(os.path.join(dirname, "./res/sounds/Start Auto_normalized.wav"))
sound_teleop_start = pygame.mixer.Sound(os.path.join(dirname, "./res/sounds/Start Teleop_normalized.wav"))
sound_endgame_start = pygame.mixer.Sound(os.path.join(dirname, "./res/sounds/Start of End Game_normalized.wav"))
sound_match_end = pygame.mixer.Sound(os.path.join(dirname, "./res/sounds/Match End_normalized.wav"))
sound_match_pause = pygame.mixer.Sound(os.path.join(dirname, "./res/sounds/Match Pause_normalized.wav"))

sound_auto_start.set_volume(config["sounds"]["volume"])
sound_teleop_start.set_volume(config["sounds"]["volume"])
sound_endgame_start.set_volume(config["sounds"]["volume"])
sound_match_end.set_volume(config["sounds"]["volume"])
sound_match_pause.set_volume(config["sounds"]["volume"])

# * Match
try:
    pyi_splash.update_text("Starting Match Manager")
except:
    pass
match = match_manager.MatchManager(config["event"]["save_directory"])
match_start_time = None
total_match_time = config["timing"]["auto_time_seconds"] + config["timing"]["teleop_time_seconds"]
time_update_thread: threading.Thread = None

# * Main Window
try:
    pyi_splash.update_text("Starting Main Window")
except:
    pass
main_window = tk.Tk()
main_window.title("MechaLeague Match Manager")
main_window.attributes('-topmost', True)
main_window.resizable(False, False)
main_window.iconbitmap(os.path.join(dirname, "./res/images/APPICON.ico"))

# * Launchpad integration
try:
    pyi_splash.update_text("Starting Launchpad Integration")
except:
    pass

lp: launchpad_py.LaunchpadMk2 = None
lp_wapper: launchpad_wrapper.LaunchpadWrapper = None
try: 
    lp = launchpad_py.LaunchpadMk2()
    lp_wapper = launchpad_wrapper.LaunchpadWrapper(lp)
    lp.Open()
    lp.LedAllOn(0)

    def launchpad_start():
        lp.LedCtrlPulseXYByCode(8, 1, 46)
        lp.LedCtrlXYByCode(*launchpad_constants.START_MATCH_PAD, 23)
    launchpad_start()

    def launchpad_loop():
        lp_wapper.update()
        main_window.after(100, launchpad_loop)
    launchpad_loop()

    @lp_wapper.on_button_press(*launchpad_constants.START_MATCH_PAD)
    def launchpad_start_match():
        match_start()
except:
    pass

# * Overlay
try:
    pyi_splash.update_text("Starting overlay")
except:
    pass
overlay_window = PrepatecOverlay(main_window, os.path.join(dirname, "./res/images/overlay_prepatec.png"), os.path.join(dirname, "./res/images/APPICON.ico"))

# * Scores Screen
try:
    pyi_splash.update_text("Starting scores screen")
except:
    pass
scores_screen_window = PrepatecScoresScreen(main_window, os.path.join(dirname, "./res/images/scores_screen_prepatec.png"), os.path.join(dirname, "./res/images/APPICON.ico"))

# * Match select
match_select_frame = tk.LabelFrame(main_window, text="Match Number", padx=5, pady=5)
match_select_frame.pack()

match_select_previous_button = tk.Button(match_select_frame, text=" < ")
match_select_previous_button.pack(side=tk.LEFT)

match_select_variable = tk.IntVar(match_select_frame, value=1)
match_select_entry = tk.Entry(match_select_frame, width=5, textvariable=match_select_variable)
match_select_entry.pack(padx=5, side=tk.LEFT)
match_select_variable.trace_add("write", lambda *args: match_select_variable.set(1) if match_select_variable.get() < 1 else None)

match_select_next_button = tk.Button(match_select_frame, text=" > ")
match_select_next_button.pack(side=tk.RIGHT)

match_select_previous_button.config(command=lambda: match_select_variable.set(match_select_variable.get() - 1 if match_select_variable.get() > 1 else 1))
match_select_next_button.config(command=lambda: match_select_variable.set(match_select_variable.get() + 1))

# * Teams
teams_frame = tk.LabelFrame(main_window, text="Teams", padx=5, pady=5)
teams_frame.pack()

# Red Alliance
red_alliance_frame = tk.LabelFrame(teams_frame, text="Red Alliance", padx=5, pady=5, background="#FF0000", foreground="white")
red_alliance_frame.pack(side=tk.LEFT)

red_alliance_team_1_variable = tk.IntVar(red_alliance_frame)
red_alliance_team_1 = tk.Entry(red_alliance_frame, width=5, textvariable=red_alliance_team_1_variable)
red_alliance_team_1.pack()

red_alliance_team_2_variable = tk.IntVar(red_alliance_frame)
red_alliance_team_2 = tk.Entry(red_alliance_frame, width=5, textvariable=red_alliance_team_2_variable)
red_alliance_team_2.pack()

red_alliance_team_3_variable = tk.IntVar(red_alliance_frame)
red_alliance_team_3 = tk.Entry(red_alliance_frame, width=5, textvariable=red_alliance_team_3_variable)
red_alliance_team_3.pack()

# Blue Alliance
blue_alliance_frame = tk.LabelFrame(teams_frame, text="Blue Alliance", padx=5, pady=5, background="#0000FF", foreground="white")
blue_alliance_frame.pack(side=tk.RIGHT)

blue_alliance_team_1_variable = tk.IntVar(blue_alliance_frame)
blue_alliance_team_1 = tk.Entry(blue_alliance_frame, width=5, textvariable=blue_alliance_team_1_variable)
blue_alliance_team_1.pack()

blue_alliance_team_2_variable = tk.IntVar(blue_alliance_frame)
blue_alliance_team_2 = tk.Entry(blue_alliance_frame, width=5, textvariable=blue_alliance_team_2_variable)
blue_alliance_team_2.pack()

blue_alliance_team_3_variable = tk.IntVar(blue_alliance_frame)
blue_alliance_team_3 = tk.Entry(blue_alliance_frame, width=5, textvariable=blue_alliance_team_3_variable)
blue_alliance_team_3.pack()

# Teams interactivity
red_alliance_team_1.bind("<Return>", lambda e: red_alliance_team_2.focus())
red_alliance_team_2.bind("<Return>", lambda e: red_alliance_team_3.focus())
red_alliance_team_3.bind("<Return>", lambda e: blue_alliance_team_1.focus())

blue_alliance_team_1.bind("<Return>", lambda e: blue_alliance_team_2.focus())
blue_alliance_team_2.bind("<Return>", lambda e: blue_alliance_team_3.focus())
blue_alliance_team_3.bind("<Return>", lambda e: main_window.focus())
blue_alliance_team_3.bind("<Tab>", lambda e: main_window.focus())

red_alliance_team_1_variable.trace_add("write", lambda *args: match.set_red_alliance_team_1(red_alliance_team_1_variable.get()))
red_alliance_team_2_variable.trace_add("write", lambda *args: match.set_red_alliance_team_2(red_alliance_team_2_variable.get()))
red_alliance_team_3_variable.trace_add("write", lambda *args: match.set_red_alliance_team_3(red_alliance_team_3_variable.get()))

blue_alliance_team_1_variable.trace_add("write", lambda *args: match.set_blue_alliance_team_1(blue_alliance_team_1_variable.get()))
blue_alliance_team_2_variable.trace_add("write", lambda *args: match.set_blue_alliance_team_2(blue_alliance_team_2_variable.get()))
blue_alliance_team_3_variable.trace_add("write", lambda *args: match.set_blue_alliance_team_3(blue_alliance_team_3_variable.get()))

# * Match Setup
try:
    pyi_splash.update_text("Loading initial match")
except:
    pass
def load_match():
    match_number = match_select_variable.get()

    red_alliance_team_1_variable.set(matches.at[match_number - 1, "red_alliance_team_1"])
    red_alliance_team_2_variable.set(matches.at[match_number - 1, "red_alliance_team_2"])
    red_alliance_team_3_variable.set(matches.at[match_number - 1, "red_alliance_team_3"])
    
    blue_alliance_team_1_variable.set(matches.at[match_number - 1, "blue_alliance_team_1"])
    blue_alliance_team_2_variable.set(matches.at[match_number - 1, "blue_alliance_team_2"])
    blue_alliance_team_3_variable.set(matches.at[match_number - 1, "blue_alliance_team_3"])

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

# End match
end_match_button = tk.Button(match_control_frame, text="End Match")
end_match_button.pack(side=tk.LEFT)

# * Timer
match_control_timer_label = tk.Label(main_window, text="00:00", font=("Arial", 32), foreground="black")
match_control_timer_label.pack()

# * Scoring
scoring_frame = tk.LabelFrame(main_window, text="Scoring", padx=5, pady=5)
scoring_frame.pack()

# Red Alliance
red_alliance_score_frame = tk.LabelFrame(scoring_frame, text="Red Alliance", padx=5, pady=5, background="#FF0000", foreground="white")
red_alliance_score_frame.pack(side=tk.LEFT)

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

# Add keybinds
main_window.bind("<w>", lambda e: match.red_alliance_goal_add())
main_window.bind("<s>", lambda e: match.red_alliance_goal_sub())
main_window.bind("<d>", lambda e: match.red_alliance_foul_add())
main_window.bind("<a>", lambda e: match.red_alliance_foul_sub())

main_window.bind("<Up>", lambda e: match.blue_alliance_goal_add())
main_window.bind("<Down>", lambda e: match.blue_alliance_goal_sub())
main_window.bind("<Right>", lambda e: match.blue_alliance_foul_add())
main_window.bind("<Left>", lambda e: match.blue_alliance_foul_sub())


# * Soundboard
soundboard_frame = tk.LabelFrame(main_window, text="Soundboard", padx=5, pady=5)
soundboard_frame.pack()

soundboard_frame_left = tk.Frame(soundboard_frame, padx=5, pady=5)
soundboard_frame_left.pack(side=tk.LEFT)

soundboard_frame_right = tk.Frame(soundboard_frame, padx=5, pady=5)
soundboard_frame_right.pack(side=tk.RIGHT)

sound_auto_start_button = tk.Button(soundboard_frame_left, text="Start Auto", command=sound_auto_start.play)
sound_auto_start_button.pack()

sound_teleop_start_button = tk.Button(soundboard_frame_left, text="Start Teleop", command=sound_teleop_start.play)
sound_teleop_start_button.pack()

sound_match_end_button = tk.Button(soundboard_frame_right, text="Match End", command=sound_match_end.play)
sound_match_end_button.pack()

sound_match_pause_button = tk.Button(soundboard_frame_right, text="Match Pause", command=sound_match_pause.play)
sound_match_pause_button.pack()

sound_endgame_start_button = tk.Button(soundboard_frame, text="Start Endgame", command=sound_endgame_start.play)
sound_endgame_start_button.pack()

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
save_match_results_button = tk.Button(match_results_frame, text="Save Match Results", font=("Arial", 16))
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
def update_screens():
    # Update main window
    blue_alliance_score.config(text=str(match.blue_alliance_get_total_score()))
    blue_alliance_score_goals.config(text=f"Goals: {match.blue_alliance_get_goals()}")
    blue_alliance_score_fouls.config(text=f"Fouls: {match.blue_alliance_get_own_fouls()}")

    red_alliance_score.config(text=str(match.red_alliance_get_total_score()))
    red_alliance_score_goals.config(text=f"Goals: {match.red_alliance_get_goals()}")
    red_alliance_score_fouls.config(text=f"Fouls: {match.red_alliance_get_own_fouls()}")

    # Update Overlay
    overlay_window.set_blue_alliance_teams(match.blue_alliance_team_1, match.blue_alliance_team_2, match.blue_alliance_team_3)
    overlay_window.set_red_alliance_teams(match.red_alliance_team_1, match.red_alliance_team_2, match.red_alliance_team_3)

    overlay_window.set_blue_alliance_goals(match.blue_alliance_get_total_score())
    overlay_window.set_red_alliance_goals(match.red_alliance_get_total_score())

    overlay_window.set_event_name(config["event"]["event_name"])

    # Update Scores Screen
    scores_screen_window.set_blue_alliance_teams(match.blue_alliance_team_1, match.blue_alliance_team_2, match.blue_alliance_team_3)
    scores_screen_window.set_red_alliance_teams(match.red_alliance_team_1, match.red_alliance_team_2, match.red_alliance_team_3)

    scores_screen_window.set_blue_alliance_goals(match.blue_alliance_get_goals())
    scores_screen_window.set_red_alliance_goals(match.red_alliance_get_goals())

    scores_screen_window.set_blue_alliance_added_fouls(match.blue_alliance_get_added_fouls())
    scores_screen_window.set_red_alliance_added_fouls(match.red_alliance_get_added_fouls())

    scores_screen_window.set_blue_alliance_total_score(match.blue_alliance_get_total_score())
    scores_screen_window.set_red_alliance_total_score(match.red_alliance_get_total_score())

    # Update Match names
    match_number = match_select_variable.get()
    try:
        match_type = matches.at[match_number - 1, "match_type"]
    except:
        match_type = "Match"
    
    overlay_window.set_match_name(match_type + " " + str(match_number))
    scores_screen_window.set_match_name(match_type + " " + str(match_number))

    if lp is not None:
        try:
            if match.is_match_active():
                lp.LedCtrlPulseXYByCode(*launchpad_constants.STATUS_PAD, 23)
            else:
                lp.LedCtrlXYByCode(*launchpad_constants.STATUS_PAD, 66)
        except:
            pass

        


try:
    pyi_splash.update_text("Updating screens")
except:
    pass
update_screens()
match.set_update_callback(update_screens)

teleop_sound_callback_id: int
endgame_sound_callback_id: int
end_match_sound_callback_id: int
def match_start():
    if match.is_match_active():
        return

    sound_auto_start.play()

    global match_start_time
    match_start_time = time.time()

    match.start_match_with_match_number(match_select_variable.get())

    global teleop_sound_callback_id, endgame_sound_callback_id, end_match_sound_callback_id
    teleop_sound_callback_id = main_window.after((config["timing"]["auto_time_seconds"]) * 1000, lambda: sound_teleop_start.play())
    endgame_sound_callback_id = main_window.after((config["timing"]["auto_time_seconds"] + config["timing"]["teleop_time_seconds"] - config["timing"]["endgame_time_seconds"]) * 1000, lambda: sound_endgame_start.play())
    end_match_sound_callback_id = main_window.after((config["timing"]["auto_time_seconds"] + config["timing"]["teleop_time_seconds"]) * 1000, lambda: sound_match_end.play())

    def time_update():
        while match.is_match_active():
            # timekeeping
            elapsed_time = time.time() - match_start_time
            match_time = total_match_time - elapsed_time

            if lp is not None:
                match_time_percentage = match_time / total_match_time
                try:
                    for i in range(8):
                        if i < match_time_percentage * 8:
                            lp.LedCtrlXYByCode(i, 8, 23)
                        else:
                            lp.LedCtrlXYByCode(i, 8, 0)
                except:
                    pass

            # Update timers
            match_control_timer_label.config(text=time.strftime("%M:%S", time.gmtime(match_time)))
            overlay_window.set_timer_text(time.strftime("%M:%S", time.gmtime(match_time)))

            # Check if match is over
            if match_time <= 0:
                match.end_match()
                sound_match_end.play()
                match_control_timer_label.config(text="00:00")
                overlay_window.set_timer_text("00:00")
                break

            time.sleep(0.1)
    
    global time_update_thread
    time_update_thread = threading.Thread(target=time_update)
    time_update_thread.start()

start_match_button.config(command=match_start)

def stop_match():
    match.end_match()

    main_window.after_cancel(teleop_sound_callback_id)
    main_window.after_cancel(endgame_sound_callback_id)
    main_window.after_cancel(end_match_sound_callback_id)

    global time_update_thread
    time_update_thread.join()

def match_pause():
    if match.is_match_active():
        stop_match()
        sound_match_pause.play()

def match_stop():
    if match.is_match_active():
        stop_match()
        sound_match_end.play()

pause_match_button.config(command=match_pause)
end_match_button.config(command=match_stop)

if __name__ == "__main__":
    try:
        pyi_splash.update_text("Done, enjoy the competition!")
        time.sleep(0.1)
        pyi_splash.close()
    except:
        pass
    main_window.mainloop()
    if lp is not None:
        lp.LedAllOn(0)
        lp.Close()