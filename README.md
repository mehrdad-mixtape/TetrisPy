# TetrisPy
- Funny Old School Tetris With `Python`, Let's Play!
## Interview:
![image](https://github.com/mehrdad-mixtape/TetrisPy/blob/master/index.png)

## Platforms:
- Linux
- Windows (sound effects maybe don't work)
- Mac (sound effects maybe don't work)

## Python version:
- 3.6 or higher

## How to Play?
1. Create and Active the venv like: **Tetris-env**.
2. If you have problem for install `pyaudio` or `wave` on linux:
    - Install Important dev-libs for portaudio.
        - Debian: 
        ```bash
        (venv) $ sudo apt-get install portaudio19-dev
        (venv) $ pip3 install -r requirements.txt
        ```
3. Enjoy!
    - Run:
    ```bash
    (venv) $ python3 tetris.py
    ```

## Game:
![image](https://github.com/mehrdad-mixtape/TetrisPy/blob/master/index2.png)

## Audios & Sound Effects:
 - Audios & Sound effects are *.wav files and have **large** size.
 1. You can download the all audios & sound effect from this [link]("https://drive.google.com/file/d/1QfO3Gv5QSvyZmKgrRNVax6bBWKC4jhJG/view?usp=sharing")
 2. Create a directory on project path with name: `audios`
 3. Extract *audios.rar* to audios.

## Issus:
I fixed many `Critical Bugs`, But maybe ... :)
- I made the first version in ***5 days*** on my free time! Just for Fun.

## TODO:
- [x] **clean code**
- [x] **sound effects** aren't complete
- [ ] **shape generator** is so dumb
- [x] **tui** is not complete
- [x] **delay** can't change automatically
- [x] **levels** aren't implemented
- [x] **comments** aren't complete
- ...
