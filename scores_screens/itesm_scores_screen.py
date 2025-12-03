import tkinter as tk
from PIL import Image, ImageTk
from scores_screens.scores_screen import ScoresScreen

class ITESMScoresScreen(ScoresScreen):
    window: tk.Toplevel

    image: ImageTk.PhotoImage
    image_label: tk.Label

    # Red alliance
    red_alliance_team_1_label: tk.Label
    red_alliance_team_2_label: tk.Label
    red_alliance_team_3_label: tk.Label

    red_alliance_score_label: tk.Label

    red_alliance_added_fouls_label: tk.Label
    red_alliance_goals_label: tk.Label

    blue_alliance_total_score: int

    # Blue alliance
    blue_alliance_team_1_label: tk.Label
    blue_alliance_team_2_label: tk.Label
    blue_alliance_team_3_label: tk.Label

    blue_alliance_score_label: tk.Label

    blue_alliance_added_fouls_label: tk.Label
    blue_alliance_goals_label: tk.Label

    red_alliance_total_score: int

    # Event name
    event_name_label: tk.Label

    # Match name 
    match_name_label: tk.Label

    def __init__(self, master=None, image_path = "./res/images/scores_screen_itesm.png", icon_path="./res/images/APPICON.ico"):
        self.window = tk.Toplevel(master)
        self.window.title("MechaLeague Match Manager ITESM Scores Screen")
        self.window.configure(bg="#00FF00")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.iconbitmap(icon_path)

        self.image = ImageTk.PhotoImage(Image.open(image_path))
        self.image_label = tk.Label(self.window, image=self.image, background="#00FF00")
        self.image_label.pack()

        # Red alliance
        self.red_alliance_team_1_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#fe0000", fg="#fff")
        self.red_alliance_team_1_label.place(x=535, y=460, anchor=tk.CENTER)

        self.red_alliance_team_2_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#fe0000", fg="#fff")
        self.red_alliance_team_2_label.place(x=535, y=500, anchor=tk.CENTER)

        self.red_alliance_team_3_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#fe0000", fg="#fff")
        self.red_alliance_team_3_label.place(x=535, y=540, anchor=tk.CENTER)

        # Scores
        self.red_alliance_goals_label = tk.Label(self.window, text="00", font=("Arial", 24), background="#fff", fg="#000")
        self.red_alliance_goals_label.place(x=733, y=463, anchor=tk.CENTER)

        self.red_alliance_added_fouls_label = tk.Label(self.window, text="00", font=("Arial", 24), background="#fff", fg="#000")
        self.red_alliance_added_fouls_label.place(x=733, y=520, anchor=tk.CENTER)

        # Blue alliance
        self.blue_alliance_team_1_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#0000fe", fg="#fff")
        self.blue_alliance_team_1_label.place(x=1070, y=460, anchor=tk.CENTER)

        self.blue_alliance_team_2_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#0000fe", fg="#fff")
        self.blue_alliance_team_2_label.place(x=1070, y=500, anchor=tk.CENTER)

        self.blue_alliance_team_3_label = tk.Label(self.window, text="99", font=("Arial", 24), background="#0000fe", fg="#fff")
        self.blue_alliance_team_3_label.place(x=1070, y=540, anchor=tk.CENTER)

        # Scores
        self.blue_alliance_goals_label = tk.Label(self.window, text="00", font=("Arial", 24), background="#fff", fg="#000")
        self.blue_alliance_goals_label.place(x=880, y=463, anchor=tk.CENTER)

        self.blue_alliance_added_fouls_label = tk.Label(self.window, text="00", font=("Arial", 24), background="#fff", fg="#000")
        self.blue_alliance_added_fouls_label.place(x=880, y=520, anchor=tk.CENTER)

        # Scores
        self.blue_alliance_score_label = tk.Label(self.window, text="00", font=("Arial", 60), background="#0000fe", fg="#fff")
        self.blue_alliance_score_label.place(x=1070, y=295, anchor=tk.CENTER)

        self.red_alliance_score_label = tk.Label(self.window, text="00", font=("Arial", 60), background="#fe0000", fg="#fff")
        self.red_alliance_score_label.place(x=535, y=295, anchor=tk.CENTER)

        # Event name
        self.event_name_label = tk.Label(self.window, text="MechaLeague Event", font=("IMPACT", 16), background="#474745", fg="#fff")
        self.event_name_label.place(x=420, y=655, anchor=tk.W)

        # Match name
        self.match_name_label = tk.Label(self.window, text="Qualification Match 99", font=("IMPACT", 16), background="#474745", fg="#fff")
        self.match_name_label.place(x=1150, y=655, anchor=tk.E)
    
    def set_blue_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.blue_alliance_team_1_label.configure(text=str(team_1))
        self.blue_alliance_team_2_label.configure(text=str(team_2))
        self.blue_alliance_team_3_label.configure(text=str(team_3))

    def set_red_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.red_alliance_team_1_label.configure(text=str(team_1))
        self.red_alliance_team_2_label.configure(text=str(team_2))
        self.red_alliance_team_3_label.configure(text=str(team_3))

    def set_blue_alliance_goals(self, goals: int):
        self.blue_alliance_goals_label.configure(text=str(goals))

    def set_red_alliance_goals(self, goals: int):
        self.red_alliance_goals_label.configure(text=str(goals))

    def set_blue_alliance_added_fouls(self, fouls: int):
        self.blue_alliance_added_fouls_label.configure(text=str(fouls))

    def set_red_alliance_added_fouls(self, fouls: int):
        self.red_alliance_added_fouls_label.configure(text=str(fouls))

    def set_blue_alliance_total_score(self, score: int):
        self.blue_alliance_total_score = score
        self.blue_alliance_score_label.configure(text=str(score))
        # self.__update_winning_text__()

    def set_red_alliance_total_score(self, score: int):
        self.red_alliance_total_score = score
        self.red_alliance_score_label.configure(text=str(score))
        # self.__update_winning_text__()

    def __update_winning_text__(self):
        if self.red_alliance_total_score > self.blue_alliance_total_score:
            self.red_alliance_score_label.configure(font=("Arial", 60, "bold"))
        elif self.red_alliance_total_score < self.blue_alliance_total_score:
            self.blue_alliance_score_label.configure(font=("Arial", 60, "bold"))
        else:
            self.red_alliance_score_label.configure(font=("Arial", 60))
            self.blue_alliance_score_label.configure(font=("Arial", 60))

    
    def set_event_name(self, event_name: str):
        self.event_name_label.configure(text=event_name)

    def set_match_name(self, match_name: str):
        self.match_name_label.configure(text=match_name)