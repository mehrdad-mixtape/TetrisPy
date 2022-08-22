# TetrisPy
- Funny Old School Tetris With `Python`, Let's Play!

## Platforms:
- Linux
- Windows (sound effects maybe don't work)
- Mac (sound effects maybe don't work)

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

## Issus:
I fix many `Critical Bugs`, But maybe ... :)
- I made it in ***5 days*** on my free time! Just for Fun.

## TODO:
- [x] **sound effects** aren't complete
- [ ] **shape generator** is so dumb
- [ ] **tui** is not complete
- [x] **delay** can't change automatically
- [ ] **levels** aren't implemented
- [ ] **comments** aren't complete
- ...