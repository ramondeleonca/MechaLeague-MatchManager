import time
import launchpad_py as launchpad

def LedCtrlMatrix(lp: launchpad.LaunchpadPro, matrix: list[list[int]] | list[list[list[int]]], pad_offset_y: int = 0, pad_offset_x: int = 0):
    for [y_index, x] in enumerate(matrix):
        for [x_index, y] in enumerate(x):
            
            if isinstance(y, list):
                lp.LedCtrlXY(x_index + pad_offset_x, y_index + pad_offset_y, y[0], y[1], y[2])

            else:
                lp.LedCtrlXYByCode(x_index + pad_offset_x, y_index + pad_offset_y, y)

def LedCtrlMatrixAnimation(lp: launchpad.LaunchpadPro, matrix: list[list[list[int]]], pad_offset_y: int = 0, pad_offset_x: int = 0, delay: float = 0.15):
    for frame in matrix:
        LedCtrlMatrix(lp, frame, pad_offset_y, pad_offset_x)
        time.sleep(delay)

def cmppad(pad1: list[int], pad2: list[int]) -> bool:
    return pad1[0] == pad2[0] and pad1[1] == pad2[1]