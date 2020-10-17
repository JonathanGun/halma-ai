import atexit
from collections import defaultdict
import json
import os
from config import DEFAULT_BOARD_SIZE, DEFAULT_TIMELIMIT, DEFAULT_ISRED

def remove_temporary_settings():
    """
    Removes settings.json when program exits

    PARAMETERS
    ----------
    None

    RETURNS
    -------
    None
    """
    if os.path.exists("settings.json"):
        os.remove("settings.json")

if __name__ == "__main__":
    print(f"[Board Size] optional; integer: board size (8, 10, or 16), default = {DEFAULT_BOARD_SIZE}")
    BOARD_SIZE = input(">>> ")

    print(f"[Timelimit] optional; integer: timelimit in miliseconds (100-5000), default = {DEFAULT_TIMELIMIT}")
    TIMELIMIT = input(">>> ")

    print(f"[Is Red] optional; boolean: choose red pion, else blue, default = {DEFAULT_ISRED}")
    ISRED = input(">>> ")

    try:
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE not in [8, 10, 16]:
            BOARD_SIZE = DEFAULT_BOARD_SIZE
    except:
        BOARD_SIZE = DEFAULT_BOARD_SIZE

    try:
        TIMELIMIT = int(TIMELIMIT)
        if not 100 < TIMELIMIT < 5000:
            TIMELIMIT = DEFAULT_TIMELIMIT
    except:
        TIMELIMIT = DEFAULT_TIMELIMIT

    try:
        ISRED = bool(ISRED)
    except:
        ISRED = DEFAULT_ISRED

    with open("settings.json", "w") as settings:
        # settings.write(json.dumps({'BOARD_SIZE' : BOARD_SIZE, 'TIMELIMIT' : TIMELIMIT, 'ISRED' : ISRED, 'TARGETS' : None}))
        settings.write(json.dumps({'BOARD_SIZE' : BOARD_SIZE, 'TIMELIMIT' : TIMELIMIT, 'ISRED' : ISRED}))
        atexit.register(remove_temporary_settings)

    from app import Game
    game = Game(board_size=BOARD_SIZE, timelimit=TIMELIMIT, is_red=ISRED)
    game.run()