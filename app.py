from kivy.app import App
from kivy.uix.button import Button
from queue import Queue
from config import DEFAULT_BOARD_SIZE, DEFAULT_TIMELIMIT, DEFAULT_ISRED, DEFAULT_MODE
from globals import BOARD_SIZE, load_data
from board import Board
from cell import Cell
from minimax import Minimax
from pion import Pion

# pseudocode: https://pastebin.com/n8yMAMhz
# TARGETS = defaultdict(list)
# BOARD_SIZE = DEFAULT_BOARD_SIZE
# TIMELIMIT = DEFAULT_TIMELIMIT
# ISRED = DEFAULT_ISRED
game = None

dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]


class Player:
    def __init__(self, pion, mode):
        self.pion = pion
        self.mode = mode # Human, Minimax, or LocSearch
        


class Game(App):
    def __init__(self, board_size=DEFAULT_BOARD_SIZE, timelimit=DEFAULT_TIMELIMIT, is_red=DEFAULT_ISRED, mode=DEFAULT_MODE, **kwargs):
        global BOARD_SIZE
        global TIMELIMIT
        global ISRED
        global game
        BOARD_SIZE = board_size
        TIMELIMIT = timelimit
        ISRED = is_red
        self.TARGETS = []
        game = self

        self.init_players(mode)
        super().__init__(**kwargs)

    def build(self):
        self.board = Board(self)
        for cell in self.board:
            self.board.add_widget(cell)
        self.active_player.targets = [self.board.board[i][j] for (i, j) in self.TARGETS[self.active_player.pion]]
        self.enemy.targets = [self.board.board[i][j] for (i, j) in self.TARGETS[self.enemy.pion]]
        return self.board

    def init_players(self, mode):
        self.active_player = Player(Pion.RED, 
            "Human" if (ISRED and mode != "EvE") or mode == "PvP" else 
            "Minimax" if (ISRED and mode == "EvE") or (not ISRED and mode == "Min") else
            "LocSearch")
        self.enemy = Player(Pion.BLUE,
            "Human" if (not ISRED and mode != "EvE") or mode == "PvP" else 
            "Minimax" if (not ISRED and mode == "EvE") or (ISRED and mode == "Min") else
            "LocSearch")
        print(ISRED)
        print(mode)
        print(self.active_player.mode)


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
                if (frm.i, frm.j) in self.TARGETS[self.active_player.pion] and (next[0], next[1]) not in self.TARGETS[self.active_player.pion]:
                    continue
                if (frm.i, frm.j) not in self.TARGETS[self.enemy.pion] and (next[0], next[1]) in self.TARGETS[self.enemy.pion]:
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
                    if (frm.i, frm.j) in self.TARGETS[self.active_player.pion] and (i, j) not in self.TARGETS[self.active_player.pion]:
                        continue
                    if (frm.i, frm.j) not in self.TARGETS[self.enemy.pion] and (i, j) in self.TARGETS[self.enemy.pion]:
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
            print("objective = ", objective(self.board, self.active_player, self.TARGETS))
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

        # auto move if player is a bot
        if (self.active_player.mode == "Minimax"):
            (frm_x, frm_y), (to_x, to_y) = Minimax(self.TARGETS, self.board.to_ozer_board(), TIMELIMIT/1000).result
            self.move(self.board.board[frm_x][frm_y], self.board.board[to_x][to_y])
            self.next_turn()



def dist(cell1, cell2):
    return abs(cell1.i - cell2.i) + abs(cell1.j - cell2.j)


def objective(board, player, targets):
    value = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (board.is_occupied(row, col)):
                cell = board.board[row][col]
                maxDist = -(BOARD_SIZE-1)*2  # berikan N poin jika berhasil mencapai goal
                win_cells = []
                # print("ini cell yang dicek : ", cell)
                for (iGoal, jGoal) in targets[cell.pion]:
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
