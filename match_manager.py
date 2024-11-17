import math
import json
import uuid
import time
import os
from typing import Callable

class MatchManager:
    blue_alliance_goals: int = 0
    blue_alliance_fouls: int = 0

    red_alliance_goals: int = 0
    red_alliance_fouls: int = 0

    blue_alliance_team_1: int = 99
    blue_alliance_team_2: int = 99
    blue_alliance_team_3: int = 99

    red_alliance_team_1: int = 99
    red_alliance_team_2: int = 99
    red_alliance_team_3: int = 99

    FOULS_PER_GOAL: int = 3

    match_active: bool = False
    locked: bool = True

    update_callback: Callable = None

    save_directory: str

    match_number: int = 0

    def __init__(self, save_directory: str):
        self.save_directory = save_directory

    # * Blue Alliance
    def set_blue_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.blue_alliance_team_1 = team_1
        self.blue_alliance_team_2 = team_2
        self.blue_alliance_team_3 = team_3    
        if self.update_callback is not None:
            self.update_callback()

    def set_blue_alliance_team_1(self, team_1: int):
        self.blue_alliance_team_1 = team_1
        if self.update_callback is not None:
            self.update_callback()

    def set_blue_alliance_team_2(self, team_2: int):
        self.blue_alliance_team_2 = team_2
        if self.update_callback is not None:
            self.update_callback()
    
    def set_blue_alliance_team_3(self, team_3: int):
        self.blue_alliance_team_3 = team_3
        if self.update_callback is not None:
            self.update_callback()
    
    def blue_alliance_goal_add(self):
        if (self.match_active or not self.locked):
            self.blue_alliance_goals += 1
        if self.update_callback is not None:
            self.update_callback()

    def blue_alliance_goal_sub(self):
        if (self.match_active or not self.locked) and self.blue_alliance_goals > 0:
            self.blue_alliance_goals -= 1
        if self.update_callback is not None:
            self.update_callback()

    def blue_alliance_foul_add(self):
        if (self.match_active or not self.locked):
            self.blue_alliance_fouls += 1
        if self.update_callback is not None:
            self.update_callback()

    def blue_alliance_foul_sub(self):
        if (self.match_active or not self.locked) and self.blue_alliance_fouls > 0:
            self.blue_alliance_fouls -= 1
        if self.update_callback is not None:
            self.update_callback()

    def blue_alliance_reset(self):
        self.blue_alliance_goals = 0
        self.blue_alliance_fouls = 0
        if self.update_callback is not None:
                self.update_callback()
    
    def blue_alliance_get_total_score(self):
        return self.blue_alliance_goals + math.floor(self.blue_alliance_get_added_fouls() / self.FOULS_PER_GOAL)
    
    def blue_alliance_get_goals(self):
        return self.blue_alliance_goals
    
    def blue_alliance_get_added_fouls(self):
        return self.red_alliance_fouls
    
    def blue_alliance_get_own_fouls(self):
        return self.blue_alliance_fouls

    # * Red Alliance
    def set_red_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.red_alliance_team_1 = team_1
        self.red_alliance_team_2 = team_2
        self.red_alliance_team_3 = team_3
        if self.update_callback is not None:
            self.update_callback()

    def set_red_alliance_team_1(self, team_1: int):
        self.red_alliance_team_1 = team_1
        if self.update_callback is not None:
            self.update_callback()

    def set_red_alliance_team_2(self, team_2: int):
        self.red_alliance_team_2 = team_2
        if self.update_callback is not None:
            self.update_callback()
    
    def set_red_alliance_team_3(self, team_3: int):
        self.red_alliance_team_3 = team_3
        if self.update_callback is not None:
            self.update_callback()

    def red_alliance_goal_add(self):
        if (self.match_active or not self.locked):
            self.red_alliance_goals += 1
        if self.update_callback is not None:
                self.update_callback()

    def red_alliance_goal_sub(self):
        if (self.match_active or not self.locked) and self.red_alliance_goals > 0:
            self.red_alliance_goals -= 1
        if self.update_callback is not None:
                self.update_callback()

    def red_alliance_foul_add(self):
        if (self.match_active or not self.locked):
            self.red_alliance_fouls += 1
        if self.update_callback is not None:
                self.update_callback()

    def red_alliance_foul_sub(self):
        if (self.match_active or not self.locked) and self.red_alliance_fouls > 0:
            self.red_alliance_fouls -= 1
        if self.update_callback is not None:
                self.update_callback()

    def red_alliance_reset(self):
        self.red_alliance_goals = 0
        self.red_alliance_fouls = 0
        if self.update_callback is not None:
                self.update_callback()

    def red_alliance_get_total_score(self):
        return self.red_alliance_goals + math.floor(self.red_alliance_get_added_fouls() / self.FOULS_PER_GOAL)
    
    def red_alliance_get_goals(self):
        return self.red_alliance_goals
    
    def red_alliance_get_added_fouls(self):
        return self.blue_alliance_fouls
    
    def red_alliance_get_own_fouls(self):
        return self.red_alliance_fouls
    
    # * Housekeeping
    def reset_all(self):
        self.blue_alliance_reset()
        self.red_alliance_reset()

    def start_match(self):
        self.match_active = True
        self.reset_all()
        if self.update_callback is not None:
            self.update_callback()

    def start_match_with_match_number(self, match_number: int):
        self.match_number = match_number
        self.start_match()
        if self.update_callback is not None:
            self.update_callback()

    def resume_match(self):
        if self.update_callback is not None:
            self.update_callback()
        self.match_active = True

    def end_match(self):
        if self.update_callback is not None:
            self.update_callback()
        self.match_active = False

    def set_match_active(self, active: bool):
        if self.update_callback is not None:
            self.update_callback()
        self.match_active = active

    def is_match_active(self):
        return self.match_active
    
    def set_locked(self, locked: bool):
        if self.update_callback is not None:
            self.update_callback()
        self.locked = locked

    def is_locked(self):
        return self.locked
    
    def lock(self):
        self.locked = True
        if self.update_callback is not None:
            self.update_callback()

    def unlock(self):
        self.locked = False
        if self.update_callback is not None:
            self.update_callback()

    def set_update_callback(self, callback: Callable):
        self.update_callback = callback

    def set_match_number(self, match_number: int):
        self.match_number = match_number
        if self.update_callback is not None:
            self.update_callback()

    def save_match(self):
        match_data = {
            "blue_alliance": {
                "team_1": self.blue_alliance_team_1,
                "team_2": self.blue_alliance_team_2,
                "team_3": self.blue_alliance_team_3,
                "goals": self.blue_alliance_goals,
                "fouls": self.blue_alliance_fouls
            },
            "red_alliance": {
                "team_1": self.red_alliance_team_1,
                "team_2": self.red_alliance_team_2,
                "team_3": self.red_alliance_team_3,
                "goals": self.red_alliance_goals,
                "fouls": self.red_alliance_fouls
            }
        }

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory, exist_ok=True)

        date_str = time.strftime("%Y%m%d-%H%M%S")
        id = uuid.uuid4().hex
        match_file = open(f"{self.save_directory}/MATCH_{str(self.match_number)}_RESULTS_{date_str}_{id}.json", "w")
        match_file.write(json.dumps(match_data))
        match_file.close()