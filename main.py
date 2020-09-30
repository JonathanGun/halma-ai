from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from queue import Queue
import enum


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
                if i + j < 4:
                    self.board[i][j] = Cell(i, j, Pion.RED)
                elif i + j > self.cols + self.rows - 6:
                    self.board[i][j] = Cell(i, j, Pion.GREEN)
                elif self.players != 2:
                    # ujung kanan atas sama kiri bawah
                    self.board[i][j] = Cell(i, j, None)  # placeholder
                else:
                    self.board[i][j] = Cell(i, j, None)


class Player:
    def __init__(self, pion):
        self.pion = pion
        print(pion)
        self.targets = []  # koordinat / pointer ke petak tujuan

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
        self.players = players
        self.next_players = Queue()
        for i in range(self.players):
            self.next_players.put(Player(Pion(i)))
        self.active_player = self.next_players.get()
        self.board_size = board_size
        super().__init__(**kwargs)

    def build(self):
        self.board = Board(size=self.board_size, players=self.players)
        for cell in self.board:
            self.board.add_widget(cell)
        return self.board

    def check_winner(self):
        # for player in board.players:
        #     for goal in goal_cells[player.pion]:
        #       if goal.pion != player.pion:
        #         break
        #     else:
        #       return player
        return None


if __name__ == "__main__":
    # pseudocode: https://pastebin.com/n8yMAMhz
    Game(players=2).run()
