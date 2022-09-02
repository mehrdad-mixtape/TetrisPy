from typing import Callable, List, Tuple, Any
from rich.table import Table
from platform import system
from random import choice
from os import system as run, kill
from signal import SIGTERM
from subprocess import DEVNULL, STDOUT, Popen
from time import sleep
from playMusic import duration_music, find_audios
from tetrisTypes_and_settings import *

# define functions: -------------------------------------------
def kill_process(pid: int):
    if pid != -1:
        kill(pid, SIGTERM)

def clear_screen(default: int=1) -> None:
    """ Four methods for clear the terminal """
    if default == 1:
        if system() in 'Linux Darwin': run('clear')
        elif system() == 'Windows': run('cls')
    elif default == 2:
        print("\033[2J")
    elif default == 3:
        console.clear()
    elif default == 4:
        Popen(['./tools/clear_screen'])
    else:
        raise ValueError('default = 1 or 2 or 3 or 4')

def random_shape() -> Shape:
    """ Get random shape from queue """
    for _ in range(0, MAX_LEN_Q):
        if len(queue_shape) != MAX_LEN_Q:
            queue_shape.append(choice(ALL_SHAPES))
        else:
            break
    return queue_shape.pop(0)

def play_music(which: int) -> Tuple[int]:
    """ Play musics on the background """
    if find_audios():
        proc: Popen = None
        if system() in 'Linux Darwin':
            proc = Popen(['python3', 'playMusic.py', f"{which}"], stderr=STDOUT, stdout=DEVNULL)
        elif system() == 'Windows':
            proc = Popen(['python', 'playMusic.py', f"{which}"], stderr=STDOUT, stdout=DEVNULL)
        
        return (proc.pid, duration_music(which))
    else:
       return (-1, -1)

def next_music() -> int:
    """ Get next music number for playing """
    return next(MAIN_MUSICS)

def keyboard_lock(func: Callable) -> Callable:
    """ Lock keyboard events """
    def __decorator__(lock: bool) -> None:
        if lock:
            lambda: None
        else:
            func()
    return __decorator__

# define classes: -------------------------------------------

class Screen:
    """ Screen of Tetris """
    width = 10 # 10 Columns are visible.
    height = 20 + 4 # 20 Rows are visible and 4 Rows are hidden.
    cache = None
    def __init__(self):
        self.__prev_loc_x = 0 # Previous x location of shape on screen.
        self.__prev_loc_y = 0 # Previous y location of shape on screen.
        self.__prev_mapped: Tuple[Tuple[str]] = () # Previous shape that mapped on screen.
        self.__screen: List[List[Block]] = [ # Append 20 Rows on screen that wanna be visible.
            [Block() for _ in range(0, Screen.width)] for _ in range(0, Screen.height - 4)
        ]
        for _ in range(0, 4): # Insert 4 Rows on index=0 that wanna be hidden.
            self.__screen.insert(0, [Block(color=BK) for _ in range(0, Screen.width)])
        self._is_full = False

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        del self

    def __dir__(self):
        return ['draw', 'map_shape', 'reset_prev_mapped', 'is_full']

    @property
    def is_full(self) -> bool:
        """ Screen can be full if all rows fill with shapes """
        return self._is_full

    def __shape_mapper(self, shape: Tuple[Tuple[str]], loc_x: int, loc_y: int) -> None:
        """ Map shape on loc_x + i & loc_y + j on screen"""
        for i, row in enumerate(shape):
            for j, col in enumerate(row):
                if col == E:
                    continue
                else:
                    try:
                        if self.__screen[loc_x + i][loc_y + j].color == BK:
                            self.__screen[loc_x + i][loc_y + j].fill = 1
                        else:
                            self.__screen[loc_x + i][loc_y + j].color = col
                            self.__screen[loc_x + i][loc_y + j].fill = 1
                    except IndexError:
                        continue

    def __shape_cleaner(self) -> None:
        """ Clear previous location of shape on screen """
        for i, row in enumerate(self.__prev_mapped):
            for j, col in enumerate(row):
                if col == E:
                    continue
                else:
                    try:
                        if self.__screen[self.__prev_loc_x + i][self.__prev_loc_y + j].color == BK:
                            self.__screen[self.__prev_loc_x + i][self.__prev_loc_y + j].fill = 0
                        else:
                            self.__screen[self.__prev_loc_x + i][self.__prev_loc_y + j].color = E
                            self.__screen[self.__prev_loc_x + i][self.__prev_loc_y + j].fill = 0
                    except IndexError:
                        continue

    def __shape_check_around(self, shape: Tuple[Tuple[str]], loc_x: int, loc_y: int) -> bool:
        """ Check around of shape that wanna close to other shapes or walls or button """
        flag = True
        for i, row in enumerate(shape):
            for j, col in enumerate(row):
                if col == E: continue
                else:
                    try:
                        # Other shapes maybe fill loc_x + i and loc_y + j
                        if self.__screen[loc_x + i][loc_y + j].fill:
                            flag = False
                            break
                    except IndexError:
                        flag = False
                        break
        return flag

    def __check_screen_is_full(self) -> None:
        """ Check Screen, if this was full, game is over! """
        counter = 0
        for row in self.__screen:
            for col in row:
                if col.fill == 1:
                    counter += 1
                    break
        if counter == Screen.height:
            self._is_full = True

    def calc_score(self) -> int:
        """ Find rows that were filled with block """
        score_flag = False
        index_of_rows = []
        num_of_rows = 0
        score = 0
        xp = 1
        for row in self.__screen:
            if row[0].color == BK: continue
            for block in row:
                score_flag = (lambda block: True if block.fill else False)(block)
                if not score_flag: break
            if score_flag:
                index_of_rows.append(self.__screen.index(row))

        num_of_rows = len(index_of_rows)

        if num_of_rows:
            if num_of_rows == 4:
                xp = 4; play_music(6)
            elif num_of_rows == 3:
                xp = 3; play_music(5)
            elif num_of_rows == 2:
                xp = 2; play_music(4)
            elif num_of_rows == 1:
                xp = 1; play_music(3)
            for i in index_of_rows:
                row = self.__screen.pop(i)
                for block in row:
                    block.color = E
                    block.fill = 0
                self.__screen.insert(4, row) # Skip hidden rows and insert new row of blocks.
                score += SCORE_FOR_EACH_ROW * xp
            sleep(0.2)
        return score

    def dead(self, *game_arg) -> None:
        """ Funny demo after game over """
        play_music(7)
        for row in self.__screen:
            for block in row:
                if block.color == BK:
                    continue
                block.color = BW
            clear_screen(default=4)
            self.draw(
                current_score=game_arg[0],
                state=game_arg[1],
                level=game_arg[2]
            )
            sleep(0.2)

    def draw(self, current_score: int=0, state: Game_state=Game_state.PLAY, level: Level=LEVELS[0], empty: bool=False) -> str:
        """ Draw screen """
        states = {
            Game_state.PLAY: 'green',
            Game_state.PAUSE: 'yellow',
            Game_state.GAME_OVER: 'red',
        }
        ## Create screen:
        screen = ""
        screen += f"{DR}{''.join([RL for _ in range(0, Screen.width)])}{DL}\n"
        if empty:
            for row in self.__screen:
                if row[0].color != BK:
                    if self.__screen.index(row) == 13:
                        screen += f"{UD}  {'      PAUSE     '}  {UD}\n"
                    else:
                        screen += f"{UD}{'  ' * len(row)}{UD}\n"
        else:
            for row in self.__screen:
                if row[0].color != BK:
                    screen += f"{UD}{''.join(block.color for block in row)}{UD}\n"

        screen += f"{UR}{''.join([RL for _ in range(0, Screen.width)])}{UL}\n"

        ## Create next_shape:
        next_shape = "\n"
        for obj_shape in queue_shape:
            for row in obj_shape.main:
                next_shape += f"\t{''.join(['  ' if piece == E else piece for piece in row])}\n"
            next_shape += '\n'
        
        # Create key_binds:

        nS_Kb = f"{next_shape}{key_binds}"

        remain_score_to_next_level = f"Next Level After: {level.max_score - current_score}"

        ## Create table:
        table = Table()
        table.add_column("[white]TETRIS[/white]", style="cyan", no_wrap=True, justify='center')
        table.add_column("[white]Next Shape[/white]", style=states.get(state, 'white'), no_wrap=True)
        table.add_row(screen, nS_Kb)
        table.add_row(f"Score: {current_score}\n{remain_score_to_next_level}", f"Level: {level.l_num + 1}\nState: {state.value}")
        console.print('\n' * 50, table, '\n' * 10)

    def reset_prev_mapped(self) -> None:
        """ Reset previous shape that was mapped """
        self.__prev_mapped = ()

    def map_shape(self, shape: Tuple[Tuple[str]], loc_x: int, loc_y: int) -> bool:
        """ Map shape on screen if was possible on loc_x & loc_y """
        self.__shape_cleaner()

        if not self.__shape_check_around(shape, loc_x, loc_y):
            self.__shape_mapper(self.__prev_mapped, self.__prev_loc_x, self.__prev_loc_y)
            self.__check_screen_is_full()
            return False
        else:
            self.__shape_mapper(shape, loc_x, loc_y)
            self.__prev_mapped = shape
            self.__prev_loc_x = loc_x
            self.__prev_loc_y = loc_y
            self.__check_screen_is_full()
            return True
