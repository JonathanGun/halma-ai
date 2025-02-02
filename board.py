from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from collections import defaultdict
from globals import BOARD_SIZE, add_targets
from cell import Cell
from pion import Pion
import numpy as np


def enemy(pion):
    return Pion((pion + 1) % 2)


class Board(GridLayout):
    def __init__(self, game=None, **kwargs):
        super(Board, self).__init__(**kwargs)
        Window.size = (500, 500)
        self.cols = BOARD_SIZE
        self.rows = BOARD_SIZE
        self.board = np.full((self.rows, self.cols), None)
        self.game = game
        self.setup()

    def valid_cell(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def __iter__(self):
        for row in self.board:
            for cell in row:
                yield cell

    def setup(self):
        # Target cells for each pion
        TARGETS = defaultdict(list)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                our_limit, enemy_limit = {
                    8: (4, 10),
                    10: (5, 13),
                    16: (6, 24)
                }.get(BOARD_SIZE)
                if i + j < our_limit:
                    TARGETS[Pion.BLUE].append((i, j))
                elif i + j > enemy_limit:
                    TARGETS[Pion.RED].append((i, j))

        self.game.TARGETS = TARGETS
        for i in range(self.rows):
            for j in range(self.cols):
                for pion, target in TARGETS.items():
                    if (i, j) in target:
                        self.board[i][j] = Cell(i, j, enemy(pion), self.game)
                        break
                else:
                    self.board[i][j] = Cell(i, j, None, self.game)

    def is_occupied(self, i, j):
        return self.board[i][j].pion is not None

    def to_ozer_board(self):
        ls = self.board.copy()
        for r in range(len(ls)):
            for c in range(len(ls[0])):
                cell = ls[r, c]
                ls[r, c] = 1 if cell.pion == self.game.active_player.pion else (-1 if cell.pion == self.game.enemy.pion else 0)
        return ls
