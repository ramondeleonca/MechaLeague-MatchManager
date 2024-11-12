import tkinter as tk
import pygame.mixer
import toml

# * Config
with open("./fms.config.toml", "r") as config_file:
    config = toml.load(config_file)

# * Sounds
pygame.mixer.init()
sound_auto_start = pygame.mixer.Sound("./res/sounds/Start Auto_normalized.wav")
sound_teleop_start = pygame.mixer.Sound("./res/sounds/Start Teleop_normalized.wav")
sound_endgame_start = pygame.mixer.Sound("./res/sounds/Start of End Game_normalized.wav")
sound_match_end = pygame.mixer.Sound("./res/sounds/Match End_normalized.wav")
sound_match_pause = pygame.mixer.Sound("./res/sounds/Match Pause_normalized.wav")

# * Main Window
main_window = tk.Tk()
main_window.title("MechaLeague Match Manager")

# * Match
match_frame = tk.LabelFrame(main_window, text="Match", padx=5, pady=5)
match_frame.pack()

# Blue Alliance
blue_alliance_frame = tk.LabelFrame(match_frame, text="Blue Alliance", padx=5, pady=5, background="#0000FF", foreground="white")
blue_alliance_frame.pack(side=tk.LEFT)

blue_alliance_team_1 = tk.Entry(blue_alliance_frame, width=5)
blue_alliance_team_1.pack()
blue_alliance_team_2 = tk.Entry(blue_alliance_frame, width=5)
blue_alliance_team_2.pack()
blue_alliance_team_3 = tk.Entry(blue_alliance_frame, width=5)
blue_alliance_team_3.pack()

# Red Alliance
red_alliance_frame = tk.LabelFrame(match_frame, text="Red Alliance", padx=5, pady=5, background="#FF0000", foreground="white")
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

# * Match Control
match_control_frame = tk.LabelFrame(main_window, text="Match Control", padx=5, pady=5)
match_control_frame.pack()

# Start Match
start_match_button = tk.Button(match_control_frame, text="Start Match", command=lambda: sound_auto_start.play())
start_match_button.pack(side=tk.LEFT)

# End Match
end_match_button = tk.Button(match_control_frame, text="End Match", command=lambda: sound_match_end.play())
end_match_button.pack(side=tk.LEFT)

# Pause Match
pause_match_button = tk.Button(match_control_frame, text="Pause Match", command=lambda: sound_match_pause.play())
pause_match_button.pack(side=tk.LEFT)

# * Timer
timer_label = tk.Label(main_window, text="00:00", font=("Arial", 32), foreground="black")
timer_label.pack()

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

if __name__ == "__main__":
    main_window.mainloop()