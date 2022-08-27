from typing import Callable, List, Any
from rich.table import Table
from platform import system
from random import choice
from os import system as run
from subprocess import DEVNULL, STDOUT, Popen
from time import sleep, time
from playMusic import duration_music
from tetrisTypes_and_settings import *

# define functions: -------------------------------------------

def show_shape(shape: Shape) -> None:
    out = ''
    for row in shape:
        out += ''.join(['  ' if piece == E else piece for piece in row]) + '\n'
    console.print(out)

def clear_screen(default: int=1) -> None:
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

def rotate(cycle_shape: cycle) -> Shape:
    return next(cycle_shape)

def random_shape() -> cycle:
    for _ in range(0, MAX_LEN_Q):
        if len(queue_shape) != MAX_LEN_Q:
            queue_shape.append(choice(ALL_SHAPES))
        else:
            break
    return queue_shape.pop(0)

def silent_music(silent: bool) -> Callable:
    def __decorator__(func: Callable):
        def __wrapper__(music_number: int) -> Any:
            if silent:
                return
            else:
                return func(music_number)
        return __wrapper__
    return __decorator__

@silent_music(OFF)
def play_music(which: int) -> int:
    proc: Popen = None
    if system() in 'Linux Darwin':
        proc = Popen(['python3', 'playMusic.py', f"{which}"], stderr=STDOUT, stdout=DEVNULL)
    elif system() == 'Windows':
        proc = Popen(['python', 'playMusic.py', f"{which}"], stderr=STDOUT, stdout=DEVNULL)
    
    return proc.pid, duration_music(which)

def keyboard_lock(func: Callable) -> Callable:
    def __decorator__(lock: bool) -> None:
        if lock:
            lambda: None
        else:
            func()
    return __decorator__

# define classes: -------------------------------------------

class Block:
    """ Screen of Tetris filled with Blocks """
    def __init__(self, color: str=E, fill: int=0):
        self.color = color
        self._fill = fill

    @property
    def fill(self) -> int:
        return self._fill
    
    @fill.setter
    def fill(self, value: int) -> None:
        self._fill = value

class SHAPE:
    """ Father of All-Shapes, All rotations of shapes store on 'cycle' data-structure """
    def __init__(self):
        self._pool_shape: cycle = None

    def __iter__(self):
        return self.pool_shape

    def __next__(self):
        for shape in self.pool_shape:
            return shape

    @property
    def pool_shape(self):
        return self._pool_shape
    
    @pool_shape.setter
    def pool_shape(self, value: cycle):
        self._pool_shape = value

class SHAPE_L(SHAPE):
    """ Shape L with 4 rotation """
    def __init__(self):
        super().__init__()
        self._shape_01 = (
            (BO, BO, BO,),
            (BO, E, E,),
        )
        self._shape_02 = (
            (BO, BO),
            (E, BO),
            (E, BO),
        )
        self._shape_03 = (
            (E, E, BO,),
            (BO, BO, BO,),
        )
        self._shape_04 = (
            (BO, E,),
            (BO, E,),
            (BO, BO,),
        )
        self.pool_shape = cycle(
            (
                self._shape_01,
                self._shape_02,
                self._shape_03,
                self._shape_04,
            )
        )
        self._weight = 5

    def __str__(self):
        return """
        Shape L:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██████▒▒████▒▒▒▒▒▒██▒▒██▒▒▒▒
        ▒▒██▒▒▒▒▒▒▒▒██▒▒██████▒▒██▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒████▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """

    @property
    def weight(self) -> int:
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_01

class SHAPE_J(SHAPE):
    """ Shape J with 4 rotation """
    def __init__(self):
        super().__init__()
        self._shape_11 = (
            (BB, E, E,),
            (BB, BB, BB,),
        )
        self._shape_12 = (
            (BB, BB,),
            (BB, E,),
            (BB, E,),
        )
        self._shape_13 = (
            (BB, BB, BB,),
            (E, E, BB,),
        )
        self._shape_14 = (
            (E, BB,),
            (E, BB,),
            (BB, BB,),
        )
        self.pool_shape = cycle(
            (
                self._shape_11,
                self._shape_12,
                self._shape_13,
                self._shape_14,
            )
        )
        self._weight = 5

    def __str__(self):
        return """
        Shape J:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒████▒▒██████▒▒▒▒██▒▒
        ▒▒██████▒▒██▒▒▒▒▒▒▒▒██▒▒▒▒██▒▒
        ▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒████▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """

    @property
    def weight(self):
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_11

class SHAPE_I(SHAPE):
    """ Shape I with 2 rotation """
    def __init__(self):
        super().__init__()
        self._shape_21 = (
            (BC,),
            (BC,),
            (BC,),
            (BC,),
        )
        self._shape_22 = (
            (BC, BC, BC, BC,),
        )
        self.pool_shape = cycle(
            (
                self._shape_21,
                self._shape_22,
            )
        )
        self._weight = 7

    def __str__(self):
        return """
        Shape I:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒████████▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """

    @property
    def weight(self):
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_22

class SHAPE_S(SHAPE):
    """ Shape S with 2 rotation """
    def __init__(self):
        super().__init__()
        self._shape_31 = (
            (BG, E,),
            (BG, BG,),
            (E, BG,),
        )
        self._shape_32 = (
            (E, BG, BG,),
            (BG, BG, E,),
        )
        self.pool_shape = cycle(
            (
                self._shape_31,
                self._shape_32,
            )
        )
        self._weight = 3

    def __str__(self):
        return """
        Shape S:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒████▒▒
        ▒▒████▒▒████▒▒▒▒
        ▒▒▒▒██▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_32

class SHAPE_Z(SHAPE):
    """ Shape Z with 2 rotation"""
    def __init__(self):
        super().__init__()
        self._shape_41 = (
            (E, BR,),
            (BR, BR,),
            (BR, E,),
        )
        self._shape_42 = (
            (BR, BR, E,),
            (E, BR, BR,),
        )
        self.pool_shape = cycle(
            (
                self._shape_41,
                self._shape_42,
            )
        )
        self._weight = 3

    def __str__(self):
        return """
        Shape Z:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒██▒▒████▒▒▒▒
        ▒▒████▒▒▒▒████▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_42

class SHAPE_T(SHAPE):
    """ Shape T with 4 rotation"""
    def __init__(self):
        super().__init__()
        self._shape_51 = (
            (E, BP, E,),
            (BP, BP, BP,),
        )
        self._shape_52 = (
            (BP, E,),
            (BP, BP,),
            (BP, E,),
        )
        self._shape_53 = (
            (BP, BP, BP,),
            (E, BP, E,),
        )
        self._shape_54 = (
            (E, BP,),
            (BP, BP,),
            (E, BP,),
        )
        self.pool_shape = cycle(
            (
                self._shape_51,
                self._shape_52,
                self._shape_53,
                self._shape_54,
            )
        )
        self._weight = 4

    def __str__(self):
        return """
        Shape T:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒██▒▒▒▒██▒▒▒▒██████▒▒▒▒██▒▒
        ▒▒██████▒▒████▒▒▒▒██▒▒▒▒████▒▒
        ▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_51

class SHAPE_O(SHAPE):
    """ Shape O with 1 rotation """
    def __init__(self):
        super().__init__()
        self._shape_61 = (
            (BY, BY,),
            (BY, BY,),
        )
        self.pool_shape = cycle(
            (
                self._shape_61,
            )
        )
        self._weight = 6

    def __str__(self):
        return """
        Shape O:
        ▒▒▒▒▒▒▒▒
        ▒▒████▒▒
        ▒▒████▒▒
        ▒▒▒▒▒▒▒▒
        """
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def main(self) -> Shape:
        return self._shape_61

class Screen:
    """ Screen of Tetris """
    width = 10 # 10 Columns are visible.
    height = 20 + 4 # 20 Rows are visible and 4 Rows are hidden.
    def __init__(self):
        self.__prev_loc_x = 0 # Previous x location of shape on screen.
        self.__prev_loc_y = 0 # Previous y location of shape on screen.
        self.__prev_mapped: Shape = () # Previous shape that mapped on screen.
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

    def __shape_mapper(self, shape: Shape, loc_x: int, loc_y: int) -> None:
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

    def __shape_check_around(self, shape: Shape, loc_x: int, loc_y: int) -> bool:
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
        """ Find rows that filled with block """
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
                prev_score=game_arg[1],
                state=GAME_OVER,
                level=game_arg[2]
            )
            sleep(0.2)

    def draw(self, current_score: int=0, prev_score: int=0, state: str='Play', level: int=0) -> str:
        """ Draw screen """
        states = {
            PLAY: 'green',
            PAUSE: 'yellow',
            GAME_OVER: 'red',
        }
        ## Create screen:
        screen = ""
        screen += DR + ''.join([RL for _ in range(0, Screen.width)]) + DL + '\n'
        for row in self.__screen:
            if row[0].color != BK:
                screen += UD + ''.join(block.color for block in row) + UD + '\n'
        screen += UR + ''.join([RL for _ in range(0, Screen.width)]) + UL + '\n'

        ## Create next_shape:
        next_shape = "\n"
        for obj_shape in queue_shape:
            for row in obj_shape.main:
                next_shape += ' ' + ''.join(['  ' if piece == E else piece for piece in row]) + '\n'
            next_shape += '\n'
        
        # Create key_binds:
        key_binds = "\n\n[white]Key Binds:[/white]\n"
        key_binds += '[red]▲ Arrow: Rotate[/red]\n'
        key_binds += '[green]▼ Arrow: Move Down[/green]\n'
        key_binds += '[dark_orange]► Arrow: Move Right[/dark_orange]\n'
        key_binds += '[purple]◄ Arrow: Move Left[/purple]\n'
        key_binds += '[yellow]Space: Pause[/yellow]\n'
        key_binds += '[cyan]Left Ctrl: Stop Music[/cyan]\n'
        key_binds += '[blue]Left Alt: Next Music\n\t  Play Music[/blue]\n'

        nS_Kb = next_shape + key_binds

        remain_score_to_next_level = f"Next Level After: {MIN_SCORE_TO_LEVEL_UP - (current_score - prev_score)}"
        ## Create table:
        table = Table()
        table.add_column("[white]TETRIS[/white]", style="cyan", no_wrap=True, justify='center')
        table.add_column("[white]Next Shape[/white]", style=states.get(state, 'white'), no_wrap=True)
        table.add_row(screen, nS_Kb)
        table.add_row(f"Score: {current_score}\n{remain_score_to_next_level}", f"Level: {level}\nState: {state}")
        console.print(table)

    def reset_prev_mapped(self) -> None:
        """ Reset previous shape that was mapped """
        self.__prev_mapped = ()

    def map_shape(self, shape: Shape, loc_x: int, loc_y: int) -> bool:
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

# define variables: -------------------------------------------

ALL_SHAPES = [eval(f"SHAPE_{char}()") for char in "LJISZTO"]