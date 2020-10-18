from collections import defaultdict
from config import *
import json
from pion import Pion

BOARD_SIZE = DEFAULT_BOARD_SIZE
TIMELIMIT = DEFAULT_TIMELIMIT
ISRED = DEFAULT_ISRED
# TARGETS = defaultdict(list)


def load_data():
    global BOARD_SIZE
    global TIMELIMIT
    global ISRED
    global TARGETS
    try:
        with open("settings.json", "r") as settings:
            data = json.loads(settings.read())
            BOARD_SIZE = data['BOARD_SIZE']
            TIMELIMIT = data['TIMELIMIT']
            ISRED = data['ISRED']
            # TARGETS = data['TARGETS']
            # print(TARGETS)
    except:
        pass


def add_targets(targets):
    global TARGETS
    TARGETS = targets
    with open("settings.json", "w") as settings:
        settings.write(json.dumps({'BOARD_SIZE': BOARD_SIZE, 'TIMELIMIT': TIMELIMIT, 'ISRED': ISRED}))
        # settings.write(json.dumps({'BOARD_SIZE' : BOARD_SIZE, 'TIMELIMIT' : TIMELIMIT, 'ISRED' : ISRED, 'TARGETS' : TARGETS}))


load_data()
