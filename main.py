from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
import enum
from collections import defaultdict
from queue import Queue


TARGETS = defaultdict(list)
BOARD_SIZE = 8

selected_cell = None
game = None

dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

def enemy(pion):
    return (pion + 1) % 2

class Pion(enum.IntEnum):
    RED = 0
    BLUE = 1

class Cell(Button):
    colors = {
        Pion.RED: (0.9, 0.1, 0.1, 1),
        Pion.BLUE: (0.3, 0.3, 0.9, 1),
    }
    default_color = (0.3, 0.3, 0.3, 1)
    reachable_color = (1, 1, 0, 1)

    def __init__(self, i, j, pion=None, **kwargs):
        self.i = i
        self.j = j
        self.pion = pion

        super(Button, self).__init__(**kwargs)
        self.bind(on_press=self._on_press)
        self.font_size = 40
        self.background_color = Cell.colors.get(self.pion, Cell.default_color)

    def _on_press(self, instance):
        print("clicked", instance.i, instance.j)
        global selected_cell
        if selected_cell == instance:
            # Revert reachable cells
            reachableCells = game.get_valid_moves(selected_cell)
            for reachableCell in reachableCells:
                game.board.board[reachableCell[0]][reachableCell[1]].background_color = Cell.default_color

            (x, y, z, a) = selected_cell.background_color
            selected_cell.background_color = (x / 1.5, y / 1.5, z / 1.5, a)
            selected_cell = None

        elif selected_cell is None:
            if instance.pion is not None:
                selected_cell = instance
                if selected_cell.pion != game.active_player.pion:
                    selected_cell = None
                    return
                (x, y, z, a) = selected_cell.background_color
                selected_cell.background_color = (x * 1.5, y * 1.5, z * 1.5, a)

                
                # Highlight reachable cells
                frm = selected_cell
                reachableCells = game.get_valid_moves(frm)
                for reachableCell in reachableCells:
                    game.board.board[reachableCell[0]][reachableCell[1]].background_color = Cell.reachable_color
                
        else:
            frm = selected_cell
            to = instance
            self._on_press(frm)
            move_success = game.move(frm, to)
            
            # Revert frm if move success
            if move_success:
                frm.background_color = Cell.default_color
                game.next_turn()

            # Revert reachable cells
            reachableCells = game.get_valid_moves(frm)
            for reachableCell in reachableCells:
                if reachableCell[0] == to.i and reachableCell[1] == to.j:
                    continue
                else:
                    game.board.board[reachableCell[0]][reachableCell[1]].background_color = Cell.default_color

    def is_inside_board(self):
        return 0 <= self.i < BOARD_SIZE and 0 <= self.j < BOARD_SIZE

    def __str__(self):
        return f"({self.i},{self.j})"


class Board(GridLayout):
    def __init__(self, size, **kwargs):
        super(Board, self).__init__(**kwargs)
        Window.size = (500, 500)
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.cols = size
        self.rows = size
        self.board = [[None for j in range(self.cols)] for i in range(self.rows)]
        self.setup()

    def valid_cell(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def __iter__(self):
        for row in self.board:
            for cell in row:
                yield cell

    def setup(self):
        for i in range(self.rows):
            for j in range(self.cols):
                for pion, target in TARGETS.items():
                    if (i, j) in target:
                        self.board[i][j] = Cell(i, j, enemy(pion))
                        break
                else:
                    self.board[i][j] = Cell(i, j, None)

    def is_occupied(self, i, j):
        return self.board[i][j].pion is not None


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
        value = 0
        # sum of max distance of each pion
        return -value

class Game(App):
    def __init__(self, board_size=8, **kwargs):
        self.active_player = Player(Pion.RED)
        self.enemy = Player(Pion.BLUE)
        self.board_size = board_size
        super().__init__(**kwargs)

    def build(self):
        self.board = Board(size=self.board_size)
        for cell in self.board:
            self.board.add_widget(cell)
        self.active_player.targets = [self.board.board[i][j] for (i, j) in TARGETS[self.active_player.pion]]
        self.enemy.targets = [self.board.board[i][j] for (i, j) in TARGETS[self.enemy.pion]]
        return self.board

    def check_winner(self):
        for player in [self.active_player, self.enemy]:
            for goal in player.targets:
                if goal.pion != player.pion:
                    break
            else:
                return player
        return None

    def get_valid_moves(self, frm):
        reachableCells = []
        
        # For normal move
        for k in range(8):
            # Get next cell
            next = (frm.i + dx[k], frm.j + dy[k])
            if self.board.valid_cell(next[0], next[1]) and not self.board.is_occupied(next[0], next[1]):
                if (frm.i, frm.j) in TARGETS[self.active_player.pion] and (next[0], next[1]) not in TARGETS[self.active_player.pion]:
                    continue
                if (frm.i, frm.j) not in TARGETS[self.enemy.pion] and (next[0], next[1]) in TARGETS[self.enemy.pion]:
                    continue
                reachableCells.append(next)

        # For jumping moves
        # Bool array
        visited = [[False for i in range(self.board_size)] for j in range(self.board_size)]

        # Queue for BFS, only contains (x,y) coordinate and boolean that indicates whether the piece has jumped
        q = Queue()

        # Insert starting pos and mark it visited
        q.put((frm.i, frm.j))
        visited[frm.i][frm.j] = True

        # BFS
        while not q.empty():
            cur = q.get()
            # Iterate all 8 directions
            for k in range(8):
                # Get next cell
                next = (cur[0] + dx[k], cur[1] + dy[k])

                if not self.board.valid_cell(next[0], next[1]):
                    continue
                # Jump a piece if this cell is occupied
                if self.board.is_occupied(next[0], next[1]):
                    next = (next[0] + dx[k], next[1] + dy[k])
                else:
                    continue
                if not self.board.valid_cell(next[0], next[1]):
                    continue
                # Don't insert to queue if cell is visited or occupied
                if visited[next[0]][next[1]] or self.board.is_occupied(next[0], next[1]):
                    continue
                
                # Pass all check, mark it as reachable and insert to queue if jumped
                visited[next[0]][next[1]] = True
                q.put((next[0], next[1]))

        # Return all reachable cells
        for i in range(self.board_size):
            for j in range(self.board_size):
                if visited[i][j] and not (i == frm.i and j == frm.j):
                    if (frm.i, frm.j) in TARGETS[self.active_player.pion] and (i, j) not in TARGETS[self.active_player.pion]:
                        continue
                    if (frm.i, frm.j) not in TARGETS[self.enemy.pion] and (i, j) in TARGETS[self.enemy.pion]:
                        continue
                    reachableCells.append((i, j))
        return reachableCells

    def is_valid_move(self, frm, to):
        reachableCells = self.get_valid_moves(frm)
        print(reachableCells)
        if (to.i, to.j) not in reachableCells:
            return False
        return all([
            self.board.valid_cell(to.i, to.j),
            to.pion is None
        ])

    def move(self, frm, to):
        if self.is_valid_move(frm, to):
            print("moved", frm, "to", to)
            to.background_color, frm.background_color = frm.background_color, to.background_color
            to.pion = frm.pion
            frm.pion = None
            return True
        else:
            print("failed to move", frm, "to", to)
            return False

    def next_turn(self):
        self.active_player, self.enemy = self.enemy, self.active_player

if __name__ == "__main__":
    # pseudocode: https://pastebin.com/n8yMAMhz
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i + j < 4:
                TARGETS[Pion.BLUE].append((i, j))
            elif i + j > BOARD_SIZE + BOARD_SIZE - 6:
                TARGETS[Pion.RED].append((i, j))
    game = Game(board_size=BOARD_SIZE)
    game.run()
