from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
import enum
from collections import defaultdict, deque


TARGETS = defaultdict(list)
PLAYERS = 4
BOARD_SIZE = 8

def enemy(pion):
    if pion == Pion.RED:
        return Pion.GREEN
    if pion == Pion.GREEN:
        return Pion.RED
    if pion == Pion.BLUE:
        return Pion.YELLOW
    if pion == Pion.YELLOW:
        return Pion.BLUE

class Pion(enum.IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3

class Cell(Button):
    colors = {
        Pion.RED: (0.9, 0.1, 0.1, 1),
        Pion.GREEN: (0.1, 0.9, 0.1, 1),
        Pion.BLUE: (0.3, 0.3, 0.9, 1),
        Pion.YELLOW: (0.9, 0.9, 0.1, 1),
    }
    default_color = (0.3, 0.3, 0.3, 1)

    def __init__(self, i, j, pion, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.bind(on_press=self._on_press)
        self.i = i
        self.j = j
        self.pion = pion
        self.font_size = 40
        self.background_color = Cell.colors.get(self.pion, Cell.default_color)

    def _on_press(self, instance):
        print("clicked", instance.i, instance.j)


class Board(GridLayout):
    def __init__(self, size, players=2, **kwargs):
        super(Board, self).__init__(**kwargs)
        Window.size = (500, 500)
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.cols = size
        self.rows = size
        self.players = players
        self.board = [[None for j in range(self.cols)] for i in range(self.rows)]
        self.setup()

    def validCell(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def __iter__(self):
        for row in self.board:
            for cell in row:
                yield cell

    def setup(self):
        for i in range(self.rows):
            for j in range(self.cols):
                for pion, target in TARGETS.items():
                    if (i, j) in target and pion < PLAYERS:
                        self.board[i][j] = Cell(i, j, enemy(pion))
                        break
                else:
                    self.board[i][j] = Cell(i, j, None)


class Player:
    def __init__(self, pion):
        self.pion = pion

    def minimax(self):
        pass


class Tree:
    def __init__(self, state):
        self.node = state
        self.successors = []

    @property
    def objective(self):
        return 0

class Game(App):
    def __init__(self, players=2, board_size=8, **kwargs):
        self.players = deque([Player(Pion(i)) for i in range(players)])
        self.board_size = board_size
        super().__init__(**kwargs)

    def build(self):
        self.board = Board(size=self.board_size, players=self.players)
        for cell in self.board:
            self.board.add_widget(cell)
        for player in self.players:
            player.targets = [self.board.board[i][j] for (i, j) in TARGETS[player.pion]]
        return self.board

    def check_winner(self):
        for player in self.players:
            for goal in player.targets:
                if goal.pion != player.pion:
                    break
            else:
                return player
        return None


if __name__ == "__main__":
    # pseudocode: https://pastebin.com/n8yMAMhz
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i + j < 4:
                TARGETS[Pion.GREEN].append((i, j))
            elif i + j > BOARD_SIZE + BOARD_SIZE - 6:
                TARGETS[Pion.RED].append((i, j))
            elif j - i >= BOARD_SIZE - 4:
                TARGETS[Pion.YELLOW].append((i, j))
            elif i - j >= BOARD_SIZE - 4:
                TARGETS[Pion.BLUE].append((i, j))
    Game(players=PLAYERS, board_size=BOARD_SIZE).run()
