import tkinter as tk
from PIL import Image, ImageTk
from overlays.overlay import Overlay

class ITESMOverlay(Overlay):
    window: tk.Toplevel
    overlay_image: ImageTk.PhotoImage
    overlay_label: tk.Label

    # Red alliance
    red_alliance_team_1_label: tk.Label
    red_alliance_team_2_label: tk.Label
    red_alliance_team_3_label: tk.Label

    red_alliance_score_label: tk.Label

    # Blue alliance
    blue_alliance_team_1_label: tk.Label
    blue_alliance_team_2_label: tk.Label
    blue_alliance_team_3_label: tk.Label

    blue_alliance_score_label: tk.Label

    # Match info
    timer_label: tk.Label

    # Event name
    event_name_label: tk.Label

    # Match name
    match_name_label: tk.Label

    def __init__(self, master=None, image_path="./res/images/overlay_itesm.png", icon_path="./res/images/APPICON.ico"):
        self.window = tk.Toplevel(master)
        self.window.title("MechaLeague Match Manager ITESM Overlay")
        self.window.configure(bg="#00FF00")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.iconbitmap(icon_path)

        self.overlay_image = ImageTk.PhotoImage(Image.open(image_path))
        self.overlay_label = tk.Label(self.window, image=self.overlay_image, background="#00FF00")
        self.overlay_label.pack()

        # Red alliance
        self.red_alliance_team_1_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#FFFFFF", fg="#000000")
        self.red_alliance_team_1_label.place(x=355 + 20, y=875 + 5, anchor=tk.CENTER)

        self.red_alliance_team_2_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#FFFFFF", fg="#000000")
        self.red_alliance_team_2_label.place(x=355 + 20, y=915 + 5, anchor=tk.CENTER)

        self.red_alliance_team_3_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#FFFFFF", fg="#000000")
        self.red_alliance_team_3_label.place(x=355 + 20, y=955 + 5, anchor=tk.CENTER)

        # Blue alliance
        self.blue_alliance_team_1_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#FFFFFF", fg="#000000")
        self.blue_alliance_team_1_label.place(x=1525 + 20, y=875 + 5, anchor=tk.CENTER)

        self.blue_alliance_team_2_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#FFFFFF", fg="#000000")
        self.blue_alliance_team_2_label.place(x=1525 + 20, y=915 + 5, anchor=tk.CENTER)

        self.blue_alliance_team_3_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#FFFFFF", fg="#000000")
        self.blue_alliance_team_3_label.place(x=1525 + 20, y=955 + 5, anchor=tk.CENTER)

        # Timer label
        self.timer_label = tk.Label(self.window, text="00:00", font=("Arial", 48), background="#FFFFFF", fg="#000000")
        self.timer_label.place(x=876, y=895)

        # Score labels
        self.blue_alliance_score_label = tk.Label(self.window, text="00", font=("Arial", 48), background="#0101fb", fg="#fff")
        self.blue_alliance_score_label.place(x=1125, y=890 + 40, anchor=tk.CENTER)

        self.red_alliance_score_label = tk.Label(self.window, text="00", font=("Arial", 48), background="#fd0304", fg="#fff")
        self.red_alliance_score_label.place(x=750, y=890 + 40, anchor=tk.CENTER)

        # Event name
        self.event_name_label = tk.Label(self.window, text="MechaLeague Prepatec", font=("IMPACT", 16), background="#474745", fg="#fff")
        self.event_name_label.place(x=340, y=1010, anchor=tk.W)

        # Match name
        self.match_name_label = tk.Label(self.window, text="Qualification Match 99", font=("IMPACT", 16), background="#474745", fg="#fff")
        self.match_name_label.place(x=1525, y=1010, anchor=tk.E)

    def set_timer_text(self, text: str):
        self.timer_label.config(text=text)

    def set_blue_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.blue_alliance_team_1_label.configure(text=str(team_1))
        self.blue_alliance_team_2_label.configure(text=str(team_2))
        self.blue_alliance_team_3_label.configure(text=str(team_3))

    def set_red_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.red_alliance_team_1_label.configure(text=str(team_1))
        self.red_alliance_team_2_label.configure(text=str(team_2))
        self.red_alliance_team_3_label.configure(text=str(team_3))

    def set_blue_alliance_goals(self, goals: int):
        self.blue_alliance_score_label.configure(text=str(goals))

    def set_red_alliance_goals(self, goals: int):
        self.red_alliance_score_label.configure(text=str(goals))

    def set_event_name(self, event_name: str):
        self.event_name_label.configure(text=event_name)

    def set_match_name(self, match_name: str):
        self.match_name_label.configure(text=match_name)

    