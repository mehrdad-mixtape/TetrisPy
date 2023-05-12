#!/bin/python3
# -*- coding: utf8 -*-

#   GPLv3 License

# Copyright (c) 2022 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/TetrisPy

# Python Version 3.6 or higher
# Tetris

__repo__ = "https://github.com/mehrdad-mixtape/TetrisPy"
__version__ = "v0.6.9"

from os import getpid
from random import randint
from parallel import threader
from time import time
from base import *
try:
    # Game run on GUI Terminal(pts)
    from pynput.keyboard import Listener as Keyboard
    pts = True
except ImportError:
    # Game run on TUI Terminal(tty)
    if system() in 'Linux Darwin':
        from captureKeyboard import KeyGetterLinux as Keyboard
    elif system() == 'Windows':
        from captureKeyboard import KeyGetterWindows as Keyboard
    pts = False

# Global variables: -----------------------------------------------------------
button = ""
pid_of_music = None
duration_of_music = None
loop_of_music = 0
kill_music = False

class Tetris:
    """ Class of Tetris, Include important variables of game """
    def __init__(self, screen: Screen, level: Level=LEVELS[0], joystick=None):
        self._screen = screen
        self._current_shape: Shape = None

        self._level = level
        self._delay = self._level.delay
        self.joystick: Keyboard = joystick
        self.score = 0
        self.line = 0
        self.state: Game_state = Game_state.PLAY
        self.music = None

        self.__read_input()

    @property    
    def current_shape(self) -> Shape:
        """ Get current shape that is on screen """
        return self._current_shape
    @current_shape.setter
    def current_shape(self, new: Shape) -> None:
        """ Set new shape on current shape and update important variables of shape """
        self._current_shape = new
        self.current_shape.current = new.rotate()
        self._current_shape.h = len(self._current_shape.current)
        self._current_shape.w = len(self._current_shape.current[0])
        self._current_shape.limit_x = Screen.height - self._current_shape.h
        self._current_shape.limit_y = Screen.width - self._current_shape.w

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def level(self) -> Level:
        return self._level
    @level.setter
    def level(self, new: Level) -> None:
        self._level = new

    @property
    def delay(self) -> float:
        """ Get current delay """
        return self._delay
    @delay.setter
    def delay(self, new: float) -> None:
        """ Set new delay """
        self._delay = new

    def check(self) -> None:
        """ Base on score, level and delay will change """
        if self.score >= self.level.max_score:
            if not LEVELS:
                self.state = Game_state.GAME_OVER
            else:
                self._level = LEVELS.pop(0)
                self.delay = self._level.delay
                play_music(14)

    def update(self) -> None:
        """ Update game, try to map shapes and draw screen of game """
        # I Try to map the shape on screen, If I couldn't, 
        # then release the shape on current loc_x & loc_y.
        if not self.screen.map_shape(
            self.current_shape.current,
            self.current_shape.x,
            self.current_shape.y
        ): self.current_shape.x = Screen.height

        # Draw the screen of game.
        self.screen.draw(
            current_score=self.score,
            current_line=self.line,
            state=self.state,
            level=self.level
        )

    def pause(self) -> None:
        """ Pause game """
        self.screen.draw(
            self.score,
            self.line,
            self.state,
            self.level,
            empty=True
        ) # Draw the empty screen to avoid cheating.
        while self.state == Game_state.PAUSE:
            sleep(1)

    @threader(join=False)
    def __read_input(self) -> None:
        """ read keyboard inputs """
        if self.joystick is not None:
            while True:
                if self.joystick.kbhit():
                    self.joystick.op_press(self.joystick.getchar(block=False))
                sleep(0.001)

current_game: Tetris = None # Global access to game.

@keyboard_lock
def event_handler() -> None:
    """ Handle keyboard events """
    global kill_music, pid_of_music, duration_of_music, loop_of_music

    if button == 't' or button == 'A' or button == 'Key.up': # rotate shape
        play_music(12)
        new_shape = current_game.current_shape.rotate()
        new_limit_h, new_limit_w = len(new_shape), len(new_shape[0])
        new_limit_x = Screen.height - new_limit_h
        new_limit_y = Screen.width - new_limit_w
    
        temp_x = new_limit_h + current_game.current_shape.x
        temp_y = new_limit_w + current_game.current_shape.y

        ## Check bottom and right side of screen:
        # 1. if I close to bottom and rotate my shape, I must change my x loc.
        if temp_x >= current_game.current_shape.limit_x:
            current_game.current_shape.x = temp_x - new_limit_h - 1

        # 2. if I close to right wall and rotate my shape, I must change my y loc.
        if current_game.current_shape.y == current_game.current_shape.limit_y:
            current_game.current_shape.y = new_limit_y
        
        elif current_game.current_shape.y == current_game.current_shape.limit_y - 1:
            current_game.current_shape.y = new_limit_y - 1

        elif current_game.current_shape.y == current_game.current_shape.limit_y - 2:
            current_game.current_shape.y = new_limit_y - 2

        ## Check the location of new_shape that wanna map on screen.
        ## When shape close to walls or bottom or other location on screen.
        if current_game.screen.map_shape(
            new_shape,
            current_game.current_shape.x,
            current_game.current_shape.y
        ): 
            current_game.current_shape.current = new_shape
            current_game.current_shape.h = new_limit_h
            current_game.current_shape.w = new_limit_w
            current_game.current_shape.limit_x = new_limit_x
            current_game.current_shape.limit_y = new_limit_y
        else: # When shape close to other shapes.
            current_game.current_shape.x = temp_x - new_limit_h
            current_game.current_shape.y = temp_y - new_limit_w
            current_game.screen.map_shape(
                current_game.current_shape.current,
                current_game.current_shape.x,
                current_game.current_shape.y
            )
        current_game.update()

    elif button == 'g' or button == 'B' or button == 'Key.down': # move down shape
        play_music(10)
        current_game.delay = 0.06

    elif button == 'f' or button == 'D' or button == 'Key.left': # move left shape
        play_music(11)
        if current_game.current_shape.y - 1 >= 0:
            if current_game.screen.map_shape(
                current_game.current_shape.current,
                current_game.current_shape.x,
                current_game.current_shape.y - 1    
            ): current_game.current_shape.y -= 1

    elif button == 'h' or button == 'C' or button == 'Key.right': # move right shape
        play_music(11)
        if current_game.current_shape.y + 1 <= current_game.current_shape.limit_y:
            if current_game.screen.map_shape(
                current_game.current_shape.current,
                current_game.current_shape.x,
                current_game.current_shape.y + 1
            ): current_game.current_shape.y += 1
    
    elif button == 'n' or button == 'Key.alt' or button == 'Key.alt_r':
        current_game.current_shape.music = next_music()
        if not kill_music: kill_process(pid_of_music) # stop previous music
        pid_of_music, duration_of_music = play_music(current_game.current_shape.music) # play new music
        loop_of_music = time()
        kill_music = False
    
    elif button == 'm' or button == 'Key.shift' or button == 'Key.shift_r':
        current_game.current_shape.music = None
        if not kill_music: kill_process(pid_of_music)
        kill_music = True
        pid_of_music = -1
        duration_of_music = -1
        loop_of_music = 0
    
    else: pass

def catch_input(key) -> None:
    """ Process keyboard events """
    global button, current_game
    button = f"{key}"
    if button == 'p' or button == 'Key.space': # Pause game
        if current_game.state == Game_state.PAUSE:
            current_game.state = Game_state.PLAY
        else:
            play_music(13)
            current_game.state = Game_state.PAUSE

    # Lock keyboard when game is pause.
    event_handler(current_game.state == Game_state.PAUSE)
    if current_game.state != Game_state.PAUSE:
        current_game.update()
    button = ""

def main() -> None:
    ## Banner:
    global pid_of_music, duration_of_music, \
        loop_of_music, kill_music, current_game
    
    clear_screen()

    check_terminal_size()
    pprint(BANNER)

    ## First screen:
    # Play starter music.
    pid_of_music, duration_of_music = play_music(2)
    try:
        arg = int(input("\n\t(default: level 1)? "))
        if arg > 11 or arg <= 0:
            level = LEVELS[0]
        if 1 <= arg <= 10:
            level = LEVELS[arg - 1]
    except ValueError:
        level = LEVELS[0]

    # If gamer wanna start form higher level, I remove previous levels.
    for _ in range(level.l_num + 1):
        LEVELS.pop(0)

    # Kill the starter music.
    kill_process(pid_of_music)
    print('\n\n')

    # Count down.
    for B in (THREE, TWO, ONE, GO):
        pprint(B)
        sleep(0.5)

    clear_screen()
    ## Start game:
    with Screen() as screen:
        with Keyboard(on_press=catch_input) as joystick:
            ## Initialize game:
            tetris = Tetris(screen, level=level, joystick=None if pts else joystick)
            tetris.music = next_music()

            pid_of_music, duration_of_music = play_music(tetris.music)

            loop_of_music = time()

            tetris.current_shape = random_shape()

            tetris.current_shape.x = DEFAULT_X_LOC
            tetris.current_shape.y = randint(MIN_RANDOM_Y_LOC, tetris.current_shape.limit_y - MIN_RANDOM_Y_LOC)

            current_game = tetris

            ## Tetris loop:
            while not tetris.screen.is_full:
                check_terminal_size()

                # Handle pause state.
                if tetris.state == Game_state.PAUSE:
                    tetris.pause()

                elif tetris.state == Game_state.GAME_OVER:
                        break

                elif tetris.state == Game_state.PLAY:

                    # Update the game.
                    tetris.update()

                    # Delay of Loop.
                    sleep(tetris.delay) 

                    # play next music.
                    if time() - loop_of_music >= duration_of_music and not kill_music:
                        tetris.music = next_music()
                        pid_of_music, duration_of_music = play_music(tetris.music)
                        loop_of_music = time()

                    # Current shape goes down on screen.
                    if tetris.current_shape.x < tetris.current_shape.limit_x:
                        tetris.current_shape.x += 1

                    # Current shape mapped on screen successfully.
                    else:
                        play_music(9)
                        tetris.delay = tetris.level.delay # If delay was changed, should be set again.
                        score, line = tetris.screen.calc_score()
                        tetris.score += score
                        tetris.score += SCORE_FOR_EACH_SHAPE
                        tetris.line += line

                        # Check current state, score, level.
                        tetris.check()

                        # Get new random shape.
                        tetris.current_shape = random_shape() 

                        # Set new location for new shape.
                        tetris.current_shape.x = DEFAULT_X_LOC
                        tetris.current_shape.y = randint(MIN_RANDOM_Y_LOC, tetris.current_shape.limit_y - MIN_RANDOM_Y_LOC)

                        # Reset the previous shape that was mapped on screen.
                        tetris.screen.reset_prev_mapped()

            # Game over.
            if not kill_music: kill_process(pid_of_music) # stop music.
            pid_of_music, duration_of_music = play_music(8) # game over music.
            tetris.state = Game_state.GAME_OVER
            tetris.screen.draw(
                current_score=tetris.score,
                current_line=tetris.line,
                state=tetris.state,
                level=tetris.level
            )
            sleep(duration_of_music)
            tetris.screen.dead(tetris.score, tetris.line, tetris.state, tetris.level)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        kill_process(getpid())
