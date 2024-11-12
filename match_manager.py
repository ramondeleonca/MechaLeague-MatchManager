import math
import json
import uuid
from typing import Callable

class MatchManager:
    blue_alliance_goals: int
    blue_alliance_fouls: int

    red_alliance_goals: int
    red_alliance_fouls: int

    blue_alliance_team_1: int
    blue_alliance_team_2: int
    blue_alliance_team_3: int

    red_alliance_team_1: int
    red_alliance_team_2: int
    red_alliance_team_3: int

    FOULS_PER_GOAL: int = 3

    match_active: bool = False
    locked: bool = True

    update_callback: Callable

    def __init__(self):
        self.blue_alliance_goals = 0
        self.blue_alliance_fouls = 0

        self.red_alliance_goals = 0
        self.red_alliance_fouls = 0

    # * Blue Alliance
    def set_blue_alliance_teams(self, team_1: int, team_2: int, team_3: int):
        self.blue_alliance_team_1 = team_1
        self.blue_alliance_team_2 = team_2
        self.blue_alliance_team_3 = team_3    
    
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

    def resume_match(self):
        self.match_active = True

    def end_match(self):
        self.match_active = False

    def set_match_active(self, active: bool):
        self.match_active = active

    def is_match_active(self):
        return self.match_active
    
    def set_locked(self, locked: bool):
        self.locked = locked

    def is_locked(self):
        return self.locked
    
    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def set_update_callback(self, callback: Callable):
        self.update_callback = callback