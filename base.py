from typing import List
from rich.table import Table
from itertools import cycle
from platform import system
from random import randint, choice
from os import system as run
from parallel import make_thread
from subprocess import call, DEVNULL, STDOUT
from time import sleep
from tetrisTypes import *

# define functions:

def show_shape(shape: Shape) -> None:
    out = ''
    for row in shape:
        out += ''.join(['  ' if piece == E else piece for piece in row]) + '\n'
    console.print(out)

def clear_screen(default: int=1) -> None:
    if default == 1:
        if system() == 'Linux': run('clear')
        elif system() == 'Windows': run('cls')
    elif default == 2:
        print("\033[2J")
    elif default == 3:
        console.clear()
    else:
        raise ValueError('default = 1 or 2 or 3')

def rotate(cycle_shape: cycle) -> Shape:
    return next(cycle_shape)

def random_shape() -> cycle:
    for _ in range(0, MAX_LEN_Q):
        if len(queue_shape) != MAX_LEN_Q:
            queue_shape.append(choice(ALL_SHAPES))
        else:
            break
    return queue_shape.pop(0)

@make_thread(join=False)
def music_clear():
    call(['python3', 'playMusic.py', '1'], stderr=STDOUT, stdout=DEVNULL)
@make_thread(join=False)
def music_main():
    call(['python3', 'playMusic.py', '2'], stderr=STDOUT, stdout=DEVNULL)
@make_thread(join=False)
def music_start():
    call(['python3', 'playMusic.py', '3'], stderr=STDOUT, stdout=DEVNULL)
@make_thread(join=False)
def music_tetrisClear():
    call(['python3', 'playMusic.py', '4'], stderr=STDOUT, stdout=DEVNULL)

# define classes: -------------------------------------------

class Block:
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

class SHAPE_0(SHAPE):
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
        Shape 0:
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

class SHAPE_1(SHAPE):
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
        Shape 1:
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

class SHAPE_2(SHAPE):
    def __init__(self):
        super().__init__()
        self._shape_21 = (
            (BW,),
            (BW,),
            (BW,),
            (BW,),
        )
        self._shape_22 = (
            (BW, BW, BW, BW,),
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
        Shape 2:
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

class SHAPE_3(SHAPE):
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
        Shape 3:
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

class SHAPE_4(SHAPE):
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
        Shape 4:
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

class SHAPE_5(SHAPE):
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
        Shape 5:
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

class SHAPE_6(SHAPE):
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
        Shape 6:
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
    width = 10
    height = 24
    def __init__(self):
        self.__prev_loc_x = 0
        self.__prev_loc_y = 0
        self.__prev_shape: Shape = ()
        self.__screen: List[List[Block]] = [
            [Block() for _ in range(0, Screen.width)] for _ in range(0, Screen.height - 4)
        ]
        for _ in range(0, 4):
            self.__screen.insert(0, [Block(color=BK) for _ in range(0, Screen.width)])

        self._is_full = False

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        del self

    def __dir__(self):
        return ['show', 'map_shape', 'reset_shape', 'is_full']

    @property
    def is_full(self) -> bool:
        return self._is_full

    def __shape_mapper(self, shape: Shape, loc_x: int, loc_y: int) -> None:
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
        for i, row in enumerate(self.__prev_shape):
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
        flag = True
        for i, row in enumerate(shape):
            for j, col in enumerate(row):
                if col == E:
                    continue
                else:
                    try:
                        if self.__screen[loc_x + i][loc_y + j].fill:
                            flag = False
                    except IndexError:
                        continue
        return flag

    def __check_end(self) -> None:
        counter = 0
        for row in self.__screen:
            for col in row:
                if col.fill == 1:
                    counter += 1
                    break
        if counter == Screen.height:
            self._is_full = True

    def calc_score(self) -> int:
        score_flag = False
        index_of_rows = []
        score = 0
        for row in self.__screen:
            if row[0].color == BK:
                continue
            for block in row:
                if block.fill:
                    score_flag = True
                else:
                    score_flag = False
                    break
            if score_flag:
                index_of_rows.append(self.__screen.index(row))
        if len(index_of_rows) == 4:
            music_tetrisClear()
            sleep(0.4)
        elif 1 <= len(index_of_rows) <= 3:
            music_clear()
            sleep(0.4)
        for i in index_of_rows:
            row = self.__screen.pop(i)
            for block in row:
                block.color = E
                block.fill = 0
            self.__screen.insert(4, row)
            score += 100

        return score

    def show(self, score: int=0, state: str='Play') -> str:
        states = {
            'Play': 'green',
            'Pause': 'yellow',
            'Game Over!': 'red',
        }
        ## Create screen:
        screen = ""
        screen += DR + ''.join([RL for _ in range(0, Screen.width)]) + DL + '\n'
        for row in self.__screen:
            if row[0].color != BK:
                screen += UD + ''.join(block.color for block in row) + UD + '\n'
        screen += UR + ''.join([RL for _ in range(0, Screen.width)]) + UL + '\n'

        ## Create next_shape:
        next_shape = ""
        for obj_shape in queue_shape:
            for row in obj_shape.main:
                next_shape += ' ' + ''.join(['  ' if piece == E else piece for piece in row]) + '\n'
            next_shape += '\n'
        
        # Create key_binds:
        key_binds = "\n\n[yellow]Key Binds:[/yellow]\n"
        key_binds += '[red]▲ UpArrow Key:\nRotate Shape[/red]\n'
        key_binds += '[green]▼ DownArrow Key:\nMove Down Shape[/green]\n'
        key_binds += '[dark_orange]► RightArrow Key:\nMove Right Shape[/dark_orange]\n'
        key_binds += '[purple]◄ LeftArrow Key:\nMove Left Shape[/purple]\n'
        key_binds += '[blue]Space Key:\nPause Game[/blue]\n'

        nS_Kb = next_shape + key_binds

        ## Create table:
        table = Table()
        table.add_column("[white]TETRIS[/white]", style="cyan", no_wrap=True, justify='center')
        table.add_column("[white]Next Shape[/white]", style=states.get(state, 'white'), no_wrap=True)
        table.add_row(screen, nS_Kb)
        table.add_row(f"Score: {score}", f"{state}")
        console.print(table)

    def reset_shape(self) -> None:
        self.__prev_shape = ()

    def map_shape(self, shape: Shape, loc_x: int, loc_y: int) -> bool:
        self.__shape_cleaner()

        if not self.__shape_check_around(shape, loc_x, loc_y):
            self.__shape_mapper(self.__prev_shape, self.__prev_loc_x, self.__prev_loc_y)
            self.__check_end()
            return False
        else:
            self.__shape_mapper(shape, loc_x, loc_y)
            self.__prev_shape = shape
            self.__prev_loc_x = loc_x
            self.__prev_loc_y = loc_y
            self.__check_end()
            return True

# define variables: -------------------------------------------

ALL_SHAPES = [eval(f"SHAPE_{i}()") for i in range(0, 7)]