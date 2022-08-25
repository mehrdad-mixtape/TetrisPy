#!/usr/bin/env python
# -*- coding: utf8 -*-

#   GPLv3 License

# Copyright (c) 2022 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/TetrisPy

# Python Version 3.8 or higher
# Tetris

__repo__ = "https://github.com/mehrdad-mixtape/TetrisPy"
__version__ = "0.1.7v"

from os import kill, getpid
from time import sleep
from random import randint
from pynput import keyboard
from signal import SIGTERM
from base import *

button = ""
delay = 0.5
prev_score = 0

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
    level = 1

def play_Tetris() -> bool:
    clear_screen(default=4)
    if not Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y):
        Tetris.x = Screen.height
        return False
    Tetris.screen.draw(
        score=Tetris.score,
        state='Pause' if Tetris.pause else 'Play',
        level=Tetris.level
    )
    return True

def update_Tetris() -> None:
    Tetris.limit_h, Tetris.limit_w = len(Tetris.shape), len(Tetris.shape[0])
    Tetris.limit_x = Screen.height - Tetris.limit_h
    Tetris.limit_y = Screen.width - Tetris.limit_w

def levelUp_Tetris() -> None:
    global prev_score
    global delay
    if Tetris.score - prev_score >= MIN_SCORE_TO_CHANGE_DELAY:
        play_music(10)
        if delay < 0.2:
            delay -= 0.02
            Tetris.level += 1
        else:
            delay -= 0.05
            Tetris.level += 1
        prev_score = Tetris.score

def pause_Tetris() -> None:
    while Tetris.pause:
        sleep(1)

def event_handler() -> None:
    if button == 'Key.up': # rotate shape
        play_music(6)
        new_shape = rotate(Tetris.shapes)
        new_limit_h, new_limit_w = len(new_shape), len(new_shape[0])
        new_limit_x = Screen.height - new_limit_h
        new_limit_y = Screen.width - new_limit_w
    
        temp_x = new_limit_h + Tetris.x
        temp_y = new_limit_w + Tetris.y

        ## Check button and right side of screen:
        # 1. if I close to button and rotate my shape, I must change my x loc.
        # if temp_x >= Tetris.limit_x:
        #     Tetris.x -= temp_x - Tetris.limit_x
        if temp_x >= Tetris.limit_x:
            Tetris.x = temp_x - new_limit_h - 1
        # 2. if I close to right wall and rotate my shape, I must change my y loc.
        # if temp_y >= Tetris.limit_y:
        #     Tetris.y -= temp_y - Tetris.limit_y
        if Tetris.y == Tetris.limit_y:
            Tetris.y = new_limit_y
        
        elif Tetris.y == Tetris.limit_y - 1:
            Tetris.y = new_limit_y - 1

        elif Tetris.y == Tetris.limit_y - 2:
            Tetris.y = new_limit_y - 2

        ## Check the location of new_shape that wanna map on screen.
        ## When shape close to walls or button.
        if Tetris.screen.map_shape(new_shape, Tetris.x, Tetris.y):
            Tetris.shape = new_shape
        else: # When shape close to other shapes.
            Tetris.x = temp_x - new_limit_h
            Tetris.y = temp_y - new_limit_w
            Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y)
        update_Tetris()

    elif button == 'Key.down': # move down shape
        play_music(13)
        Tetris.delay = 0.02
    elif button == 'Key.left': # move left shape
        play_music(14)
        if Tetris.y - 1 >= 0:
            if Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y - 1):
                Tetris.y -= 1
    elif button == 'Key.right': # move right shape
        play_music(14)
        if Tetris.y + 1 <= Tetris.limit_y:
            if Tetris.screen.map_shape(Tetris.shape, Tetris.x, Tetris.y + 1):
                Tetris.y += 1
    elif button == 'Key.space': # pause game
        if Tetris.pause: Tetris.pause = False
        else:
            play_music(9)
            Tetris.pause = True

def on_press(key) -> None:
    global button
    button = f"{key}"
    event_handler()
    play_Tetris()
    button = ""

def main() -> None:
    global delay
    clear_screen(default=1)
    console.print("""
    [white]Welcome to Tetris[/white]
    Dev By mehrdad-mixtape
    Level:[1-10]""")
    play_music(2)

    try:
        arg = int(input("\n\t(default: level 1)? "))
        if arg > 11 or arg <= 0: delay = 0.5
        if 1 <= arg <= 10:
            delay = LEVELS[arg]
            Tetris.level = arg
    except ValueError:
        delay = 0.5

    with Screen() as screen:
        with keyboard.Listener(on_press=on_press):
            Tetris.delay = delay
            Tetris.shapes = random_shape()
            Tetris.shape = rotate(Tetris.shapes)
            update_Tetris()
            Tetris.x = DEFAULT_X_LOC
            Tetris.y = randint(MIN_RANDOM_Y_LOC, Tetris.limit_y - MIN_RANDOM_Y_LOC)
            while not screen.is_full:
                (lambda pause: pause_Tetris() if pause else None)(Tetris.pause)
                Tetris.screen = screen
                update_Tetris()
                play_Tetris()
                # print(Tetris.limit_h, Tetris.limit_w, Tetris.y, Tetris.limit_y)
                sleep(Tetris.delay)
                if Tetris.x < Tetris.limit_x:
                    Tetris.x += 1
                else:
                    play_music(16)
                    Tetris.score += Tetris.screen.calc_score()
                    Tetris.score += SCORE_FOR_EACH_SHAPE
                    levelUp_Tetris()
                    Tetris.shapes = random_shape()
                    Tetris.shape = rotate(Tetris.shapes)
                    update_Tetris()
                    Tetris.delay = delay
                    Tetris.x = DEFAULT_X_LOC
                    Tetris.y = randint(MIN_RANDOM_Y_LOC, Tetris.limit_y - MIN_RANDOM_Y_LOC)
                    Tetris.screen.reset_prev_mapped()
    play_music(15)
    Tetris.screen.draw(
        score=Tetris.score,
        state='Game Over!',
        level=Tetris.level
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        kill(getpid(), SIGTERM)
