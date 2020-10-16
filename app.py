from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
import enum
from collections import defaultdict
from queue import Queue
from config import DEFAULT_BOARD_SIZE, DEFAULT_TIMELIMIT, DEFAULT_ISRED

# pseudocode: https://pastebin.com/n8yMAMhz
TARGETS = defaultdict(list)
BOARD_SIZE = DEFAULT_BOARD_SIZE
TIMELIMIT = DEFAULT_TIMELIMIT
ISRED = DEFAULT_ISRED
game = None

selected_cell = None

dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]


def enemy(pion):
    return Pion((pion + 1) % 2)


class Pion(enum.IntEnum):
    RED = 0
    BLUE = 1


class Cell(Button):
    colors = {
        Pion.RED: (0.9, 0.1, 0.1, 1),
        Pion.BLUE: (0.3, 0.3, 0.9, 1),
    }
    selected_colors = {
        Pion.RED: (1, 0.15, 0.15, 1),
        Pion.BLUE: (0.5, 0.5, 1, 1),
    }
    base_colors = {
        Pion.RED: (1, 0.45, 0.45, 1),
        Pion.BLUE: (0.7, 0.7, 1, 1),
    }
    default_color = (0.3, 0.3, 0.3, 1)
    reachable_color = (1, 1, 0, 1)

    def __init__(self, i, j, pion=None, **kwargs):
        self.i = i
        self.j = j
        self.pion = pion
        self.is_highlighted = False
        self.is_reachable = False

        super().__init__(**kwargs)
        self.bind(on_press=self._on_press)
        self.background_color = Cell.colors.get(self.pion, Cell.default_color)

    def get_background_color(self):
        if self.is_reachable:
            return Cell.reachable_color
        if self.is_selected:
            return Cell.selected_colors.get(self.pion, Cell.default_color)
        if self.pion is None:
            for base, targets in TARGETS.items():
                if (self.i, self.j) in targets:
                    return Cell.base_colors.get(enemy(base), Cell.default_color)
        return Cell.colors.get(self.pion, Cell.default_color)

    def set_highlighted(self, val):
        self.is_highlighted = val
        self.background_color = self.get_background_color()

    def set_reachable(self, val):
        self.is_reachable = val
        self.background_color = self.get_background_color()

    def set_selected(self, val):
        if val:
            global selected_cell
            selected_cell = self
        self.background_color = self.get_background_color()

    @property
    def is_selected(self):
        return self is selected_cell

    def _on_press(self, instance):
        print("clicked", instance.i, instance.j)
        global selected_cell

        # First click
        if selected_cell is None:
            if instance.pion == game.active_player.pion:
                instance.set_selected(True)

                # Highlight selected cell
                selected_cell.set_highlighted(True)

                # Highlight reachable cells
                frm = selected_cell
                reachableCells = game.get_valid_moves(frm)
                for reachableCell in reachableCells:
                    game.board.board[reachableCell[0]][reachableCell[1]].set_reachable(True)

        # Second click
        else:
            if selected_cell == instance:
                # Revert reachable cells
                reachableCells = game.get_valid_moves(selected_cell)
                for reachableCell in reachableCells:
                    game.board.board[reachableCell[0]][reachableCell[1]].set_reachable(False)

                selected_cell = None
                instance.set_selected(False)

            else:
                frm = selected_cell
                to = instance
                self._on_press(frm)
                move_success = game.move(frm, to)

                # Revert reachable cells
                reachableCells = game.get_valid_moves(frm)
                for reachableCell in reachableCells:
                    if reachableCell[0] == to.i and reachableCell[1] == to.j:
                        continue
                    else:
                        game.board.board[reachableCell[0]][reachableCell[1]].set_reachable(False)

                # Revert frm if move success
                if move_success:
                    game.next_turn()
                else:
                    self._on_press(to)

    def is_inside_board(self):
        return 0 <= self.i < BOARD_SIZE and 0 <= self.j < BOARD_SIZE

    def __str__(self):
        return f"({self.i}, {self.j})"


class Board(GridLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        Window.size = (500, 500)
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.cols = BOARD_SIZE
        self.rows = BOARD_SIZE
        self.board = [[None for j in range(self.cols)]
                      for i in range(self.rows)]
        self.setup()

    def valid_cell(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def __iter__(self):
        for row in self.board:
            for cell in row:
                yield cell

    def setup(self):
        # Target cells for each pion
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


class Game(App):
    def __init__(self, board_size=DEFAULT_BOARD_SIZE, timelimit=DEFAULT_TIMELIMIT, is_red=DEFAULT_ISRED,  **kwargs):
        global BOARD_SIZE
        global TIMELIMIT
        global ISRED
        global game
        BOARD_SIZE = board_size
        TIMELIMIT = timelimit
        ISRED = is_red
        game = self

        self.active_player = Player(Pion.RED)
        self.enemy = Player(Pion.BLUE)
        super().__init__(**kwargs)

    def build(self):
        self.board = Board()
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
        visited = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

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
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
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
            # sementara player yg ngecek selalu pemain, karena tdk tw gmn dpt player dari frm
            print("moved", frm, "to", to)
            to.pion = frm.pion
            frm.pion = None
            frm.set_reachable(False)
            frm.set_highlighted(False)
            to.set_reachable(False)
            to.set_highlighted(False)
            print("objective = ", objective(self.board, self.active_player))
            return True
        else:
            print("failed to move", frm, "to", to)
            return False

    def next_turn(self):
        winner = self.check_winner()
        if(winner is not None):
            print("Game over!")
            print(winner.pion, " wins")
            exit()
        self.active_player, self.enemy = self.enemy, self.active_player


def dist(cell1, cell2):
    return abs(cell1.i - cell2.i) + abs(cell1.j - cell2.j)


def objective(board, player):
    value = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (board.is_occupied(row, col)):
                cell = board.board[row][col]
                maxDist = -(BOARD_SIZE-1)*2  # berikan N poin jika berhasil mencapai goal
                win_cells = []
                # print("ini cell yang dicek : ", cell)
                for (iGoal, jGoal) in TARGETS[cell.pion]:
                    goal = board.board[iGoal][jGoal]
                    # print("ini cell goal : ", goal)
                    if not board.is_occupied(iGoal, jGoal):
                        maxDist = max(maxDist, dist(cell, goal))
                        print(cell, goal, dist(cell, goal))
                    else:
                        win_cells.append(goal.pion == player.pion)

                # kalau semua sudah occupied, tapi bukan sama kita punya
                if not all(win_cells):
                    maxDist = dist(cell, Cell(0, 0) if player.pion == Pion.BLUE else Cell(BOARD_SIZE-1, BOARD_SIZE-1))

                # print("ini pion di ", row, col, "punya ", end="")
                if cell.pion == player.pion:
                    # print("pemain dengan value:", value, "ditambah", maxDist)
                    value += maxDist
                else:
                    print("musuh dengan value :", value, "dikurang", maxDist)
                    value -= maxDist
    return -value
