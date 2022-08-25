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

console = Console()
queue_shape = []

MAX_LEN_Q = 4