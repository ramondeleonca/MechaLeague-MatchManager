import launchpad_py as launchpad
from typing import Callable

class LaunchpadWrapper:
    lp: launchpad.Launchpad
    button_press_callbacks: list[list[int, int, Callable]] = []
    button_release_callbacks: list[list[int, int, Callable]] = []

    def __init__(self, launchpad_instance) -> None:
        self.lp = launchpad_instance

    def update(self):
        button = self.lp.ButtonStateXY()

        if len(button) == 0:
            return

        if button[2] > 10:
            for [x, y, callback] in self.button_press_callbacks:
                if button[0] == x and button[1] == y or (x == None and y == None):
                    callback()
        else:
            for [x, y, callback] in self.button_release_callbacks:
                if (button[0] == x and button[1] == y) or (x == None and y == None):
                    callback()

    def add_button_press_callback(self, x: int, y: int, callback: Callable):
        self.button_press_callbacks.append([x, y, callback])

    def add_button_release_callback(self, x: int, y: int, callback: Callable):
        self.button_release_callbacks.append([x, y, callback])

    def on_button_press(self, x: int, y: int):
        def decorator(func):
            self.add_button_press_callback(x, y, func)
            return func
        return decorator
    
    # def on_button_press(self):
    #     def decorator(func):
    #         self.add_button_press_callback(None, None, func)
    #         return func
    #     return decorator
    
    def on_button_release(self, x: int, y: int):
        def decorator(func):
            self.add_button_release_callback(x, y, func)
            return func
        return decorator
    
    # def on_button_release(self):
    #     def decorator(func):
    #         self.add_button_release_callback(None, None, func)
    #         return func
    #     return decorator

