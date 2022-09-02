from typing import Tuple, Union, List, Dict
from rich.console import Console
from itertools import cycle
from enum import Enum

RL = "──"
UD = "│"
DR = "┌"
DL = "┐"
UR = "└"
UL = "┘"
F = "██"
E = "▒▒"

BW = f"[white]{F}[/white]"
BC = f"[cyan]{F}[/cyan]"
BY = f"[yellow]{F}[/yellow]"
BR = f"[red]{F}[/red]"
BB = f"[dark_blue]{F}[/dark_blue]"
BG = f"[green]{F}[/green]"
BP = f"[purple]{F}[/purple]"
BO = f"[dark_orange]{F}[/dark_orange]"
BK = f"[black]{F}[/black]"

R = True
L = False

MIN_RANDOM_Y_LOC = 1

DEFAULT_X_LOC = 0

SCORE_FOR_EACH_ROW = 300
SCORE_FOR_EACH_SHAPE = 100

console = Console()

queue_shape = []
MAX_LEN_Q = 4

MAIN_MUSICS = cycle([15, 16, 17, 18, 19])

BANNER = f"""
 {BY}{BY}{BY}{BY}{BY}           {BC}           {BR}
░░░░░{BY}░░░           ░{BC}          ░░
    ░{BY}      {BG}{BG}{BG}  {BC}{BC}{BC} {BO}{BO}{BO} {BR}  {BP}{BP}{BP}
    ░{BY}     {BG}░░░░{BG}░░{BC}░ ░░{BO}░░{BO}░{BR} {BP}░░░░
    ░{BY}    ░{BG}{BG}{BG}{BG} ░{BC}   ░{BO} ░  ░{BR}░░{BP}{BP}{BP}
    ░{BY}    ░{BG}░░░░   ░{BC}   ░{BO}    ░{BR} ░░░░░{BP}
    ░{BY}    ░░{BG}{BG}{BG}  ░░{BC}░{BO}{BO}    ░{BR} {BP}{BP}{BP}
    ░░      ░░░░░░    ░░  ░░░    ░░ ░░░░░░

     ████████████████████████████████████
     █▒▒▒▒▒ Dev By mehrdad-mixtape ▒▒▒▒▒█
     ████████████████████████████████████

  {BO}     {BY}{BY}   {BR}{BR}      {BB}   {BC}    {BG}{BG}  {BP}
  {BO}     {BY}{BY}     {BR}{BR}    {BB}   {BC}  {BG}{BG}    {BP}{BP}
  {BO}{BO}                  {BB}{BB}   {BC}          {BP}
                               {BC}

        [white]Welcome to Tetris[/white]
        [red]Levels[/red]: 1 2 3 4 5 6 7 8 9 10
"""

THREE = f"""
            {BG}{BG}{BG}
                {BG}
            {BG}{BG}{BG}
                {BG}
            {BG}{BG}{BG}
"""

TWO = f"""
            {BY}{BY}{BY}
                {BY}
            {BY}{BY}{BY}
            {BY}
            {BY}{BY}{BY}
"""

ONE = f"""
            {BR}{BR}
              {BR}
              {BR}
              {BR}
            {BR}{BR}{BR}
"""

GO = f"""
        {BW}{BW}{BW}{BW} {BW}{BW}{BW}{BW}
        {BW}       {BW}    {BW}
        {BW}  {BW}{BW} {BW}    {BW}
        {BW}    {BW} {BW}    {BW}
        {BW}{BW}{BW}{BW} {BW}{BW}{BW}{BW}
"""

class Game_state(Enum):
    GAME_OVER = 'Game Over'
    PLAY = 'Play'
    PAUSE = 'Pause'

class Level:
    def __init__(self, l_num: int, delay: float, max_score: int):
        self.l_num = l_num
        self.delay = delay
        self.max_score = max_score

class Block:
    """ Screen of Tetris filled with Blocks """
    def __init__(self, color: str=E, fill: int=0):
        self.color = color
        self._fill = fill

    @property
    def fill(self) -> int:
        return self._fill
    
    @fill.setter
    def fill(self, new: int) -> None:
        self._fill = new

class Base_shape:
    """ Father of All-Shapes, All rotations of shapes store on 'cycle' data-structure """
    def __init__(self):
        self._limit_h = 0 # height of shape
        self._limit_w = 0 # width of shape
        self._x = 0 # current loc_x
        self._y = 0 # current loc_y
        self._limit_x = 0 # maximum loc_x value that the shape can have on screen.
        self._limit_y = 0 # maximum loc_y value that the shape can have on screen.
        self._current: Tuple[Tuple[str]] = None
        self._pool_shape: cycle = None # store all rotations of shape

    def __iter__(self):
        return self.pool_shape

    def __next__(self):
        for shape in self.pool_shape:
            return shape

    def rotate(self):
        return next(self)

    @property
    def pool_shape(self):
        return self._pool_shape
    @pool_shape.setter
    def pool_shape(self, new: cycle):
        self._pool_shape = new

    @property
    def current(self):
        return self._current
    @current.setter
    def current(self, new: Tuple[Tuple[str]]):
        self._current = new

    @property
    def h(self) -> int:
        return self._limit_h
    @h.setter
    def h(self, new: int) -> None:
        self._limit_h = new

    @property
    def w(self) -> int:
        return self._limit_w
    @w.setter
    def w(self, new: int) -> None:
        self._limit_w = new

    @property
    def limit_x(self) -> int:
        return self._limit_x
    @limit_x.setter
    def limit_x(self, new: int) -> None:
        self._limit_x = new

    @property
    def limit_y(self) -> int:
        return self._limit_y
    @limit_y.setter
    def limit_y(self, new: int) -> None:
        self._limit_y = new

    @property
    def x(self) -> int:
        return self._x
    @x.setter
    def x(self, new: int) -> None:
        self._x = new

    @property
    def y(self) -> int:
        return self._y
    @y.setter
    def y(self, new: int) -> None:
        self._y = new

class Shape_L(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_01

class Shape_J(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_11

class Shape_I(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_22

class Shape_S(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_32

class Shape_Z(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_42

class Shape_T(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_51

class Shape_O(Base_shape):
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
    def main(self) -> Tuple[Tuple[str]]:
        return self._shape_61

ALL_SHAPES = [eval(f"Shape_{char}()") for char in "LJISZTO"]

Statics_level: Dict[int, Tuple[float, int]] = { # level_number: (delay, max_score)
    0: (0.50, 5000),
    1: (0.45, 10000),
    2: (0.40, 20000),
    3: (0.35, 30000),
    4: (0.30, 40000),
    5: (0.25, 50000),
    6: (0.20, 60000),
    7: (0.15, 70000),
    8: (0.10, 80000),
    9: (0.05, 100000),
}

LEVELS: List[Level] = [Level(n, Statics_level[n][0], Statics_level[n][1]) for n in range(0, 10)]
Statics_level.clear()

Shape = Union[Shape_L, Shape_J, Shape_I, Shape_S, Shape_Z, Shape_T, Shape_O]

key_binds = """

[white]Key Binds:[/white]
[red]▲ Arrow OR T: Rotate[/red]
[green]▼ Arrow OR G: Move Down[/green]
[dark_orange]► Arrow OR F: Move Right[/dark_orange]
[purple]◄ Arrow OR H: Move Left[/purple]
[yellow]Space OR P: Pause[/yellow]
[cyan]Shift OR M: Stop Music[/cyan]
[blue]Alt OR N: Next Music
          Play Music[/blue]
"""