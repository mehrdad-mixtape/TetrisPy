from typing import Tuple
from rich.console import Console

Shape = Tuple[Tuple[str]]

RL = "──"
UD = "│"
DR = "┌"
DL = "┐"
UR = "└"
UL = "┘"
F = "██"
E = "▒▒"

BW = f"[cyan]{F}[/cyan]"
BY = f"[yellow]{F}[/yellow]"
BR = f"[red]{F}[/red]"
BB = f"[dark_blue]{F}[/dark_blue]"
BG = f"[green]{F}[/green]"
BP = f"[purple]{F}[/purple]"
BO = f"[dark_orange]{F}[/dark_orange]"
BK = f"[black]{F}[/black]"

R = True
L = False

OFF = False
ON = True

MIN_SCORE_TO_CHANGE_DELAY = 3000

MIN_RANDOM_Y_LOC = 1

DEFAULT_X_LOC = 0

LEVELS = {
    1: 0.5,
    2: 0.45,
    3: 0.40,
    4: 0.35,
    5: 0.30,
    6: 0.25,
    7: 0.20,
    8: 0.15,
    9: 0.10,
    10: 0.05,
}

SCORE_FOR_EACH_ROW = 200
SCORE_FOR_EACH_SHAPE = 50

console = Console()

queue_shape = []
MAX_LEN_Q = 4
