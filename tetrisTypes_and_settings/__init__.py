from typing import Tuple
from rich.console import Console
from itertools import cycle
Shape = Tuple[Tuple[str]]

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

OFF = False
ON = True

MIN_SCORE_TO_LEVEL_UP = 5000

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

SCORE_FOR_EACH_ROW = 300
SCORE_FOR_EACH_SHAPE = 100

console = Console()

queue_shape = []
MAX_LEN_Q = 4

MAIN_MUSICS = cycle([15, 16, 17, 18, 19])

GAME_OVER = 'Game Over'
PLAY = 'Play'
PAUSE = 'Pause'

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
            {BW}{BW}{BW}
                {BW}
            {BW}{BW}{BW}
                {BW}
            {BW}{BW}{BW}
"""

TWO = f"""
            {BW}{BW}{BW}
                {BW}
            {BW}{BW}{BW}
            {BW}
            {BW}{BW}{BW}
"""

ONE = f"""
            {BW}{BW}
              {BW}
              {BW}
              {BW}
            {BW}{BW}{BW}
"""

GO = f"""
        {BW}{BW}{BW}{BW} {BW}{BW}{BW}{BW}
        {BW}       {BW}    {BW}
        {BW}  {BW}{BW} {BW}    {BW}
        {BW}    {BW} {BW}    {BW}
        {BW}{BW}{BW}{BW} {BW}{BW}{BW}{BW}
"""