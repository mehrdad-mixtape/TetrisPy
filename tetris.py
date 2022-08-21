# tetris by mehrdad-mixtape

from typing import Callable
from os import kill, getpid
from time import sleep
from pynput import keyboard
from signal import SIGTERM
from base import *

button = ""
delay = 0.2

__repo__ = "https://github.com/mehrdad-mixtape/TetrisPy"
__version__ = "0.1.0v"

class Tetris:
    screen: Screen = None
    limit_h = None
    limit_w = None
    limit_x = None
    limit_y = None
    x = None
    y = None
    shape: Shape = None
    shapes: cycle = None
    delay = None
    score = 0
    pause = False

def play_Tetris() -> bool:
    if not Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y):
        Tetris.x = Screen.height
        return False
    Tetris.screen.show(score=Tetris.score, state='Pause' if Tetris.pause else 'Play')
    return True

def update_Tetris() -> None:
    Tetris.limit_h, Tetris.limit_w = len(Tetris.shape), len(Tetris.shape[0])
    Tetris.limit_x = Screen.height - Tetris.limit_h
    Tetris.limit_y = Screen.width - Tetris.limit_w

def on_press(key) -> None:
    global button
    button = f"{key}"
    event_handler()
    play_Tetris()
    button = ""

def event_handler() -> None:
    if button == 'Key.up':
        new_shape = rotate(Tetris.shapes)

        temp_x = len(new_shape) + Tetris.x
        temp_y = len(new_shape[0]) + Tetris.y

        ## Check button and right side of screen:
        # 1. if I close to down side and rotate my shape, I must change my x loc to control my distance.
        if temp_x >= Tetris.limit_x:
            Tetris.x -= temp_x - Tetris.limit_x
        # 2. if close to right side and rotate my shape, I must change my y loc to control my distance.
        if temp_y >= Tetris.limit_y:
            Tetris.y -= temp_y - Tetris.limit_y - 1

        ## Check the location of new_shape that wanna map on screen.
        if Tetris.screen.map_shape(new_shape, Tetris.x, Tetris.y):
            Tetris.shape = new_shape
        else:
            Tetris.delay = 0.01
    elif button == 'Key.down':
        Tetris.delay = 0.02
    elif button == 'Key.left':
        if Tetris.y - 1 >= 0:
            if Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y - 1):
                Tetris.y -= 1
    elif button == 'Key.right':
        if Tetris.y + 1 <= Tetris.limit_y:
            if Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y + 1):
                Tetris.y += 1
    elif button == 'Key.space':
        if Tetris.pause: Tetris.pause = False
        else: Tetris.pause = True
        
def main() -> None:
    clear_screen(default=3)
    console.print("[white]Welcome to Tetris[/white]\nPress any key to startDev\nBy mehrdad-mixtape")
    music_start()
    input()
    with Screen() as screen:
        with keyboard.Listener(on_press=on_press):
            Tetris.delay = delay
            Tetris.shapes = random_shape()
            Tetris.shape = rotate(Tetris.shapes)
            update_Tetris()
            Tetris.x = 0
            Tetris.y = randint(0, Tetris.limit_y - 1)
            while not screen.is_full:
                Tetris.screen = screen
                update_Tetris()
                play_Tetris()
                sleep(Tetris.delay)
                while Tetris.pause:
                    sleep(Tetris.delay) # pause game
                if Tetris.x < Tetris.limit_x:
                    Tetris.x += 1
                else:
                    Tetris.score += Tetris.screen.calc_score()
                    Tetris.shapes = random_shape()
                    Tetris.shape = rotate(Tetris.shapes)
                    update_Tetris()
                    Tetris.delay = delay
                    Tetris.x = 0
                    Tetris.y = randint(0, Tetris.limit_y - 1)
                    Tetris.screen.reset_shape()

    Tetris.screen.show(Tetris.score, 'Game Over!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        kill(getpid(), SIGTERM)
