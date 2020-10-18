from queue import Queue
from typing import List
from globals import BOARD_SIZE, ISRED
from cell import Cell
from node import Node
from pion import Pion

dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]


def get_valid_moves(board: Node, x: int, y: int, targets):
    reachableCells = []
    active_player = Pion.BLUE if ISRED else Pion.RED
    enemy = Pion.RED if ISRED else Pion.BLUE
    # For normal move
    for k in range(8):
        # Get next cell
        next = (x + dx[k], y + dy[k])
        if board.valid_cell(next[0], next[1]) and not board.is_occupied(next[0], next[1]):
            if (x, y) in targets[active_player] and (next[0], next[1]) not in targets[active_player]:
                continue
            if (x, y) not in targets[enemy] and (next[0], next[1]) in targets[enemy]:
                continue
            reachableCells.append(next)
    # For jumping moves
    # Bool array
    visited = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    # Queue for BFS, only contains (x,y) coordinate and boolean that indicates whether the piece has jumped
    q = Queue()
    # Insert starting pos and mark it visited
    q.put((x, y))
    visited[x][y] = True
    # BFS
    while not q.empty():
        cur = q.get()
        # Iterate all 8 directions
        for k in range(8):
            # Get next cell
            next = (cur[0] + dx[k], cur[1] + dy[k])
            if not board.valid_cell(next[0], next[1]):
                continue
            # Jump a piece if this cell is occupied
            if board.is_occupied(next[0], next[1]):
                next = (next[0] + dx[k], next[1] + dy[k])
            else:
                continue
            if not board.valid_cell(next[0], next[1]):
                continue
            # Don't insert to queue if cell is visited or occupied
            if visited[next[0]][next[1]] or board.is_occupied(next[0], next[1]):
                continue
            # Pass all check, mark it as reachable and insert to queue if jumped
            visited[next[0]][next[1]] = True
            q.put((next[0], next[1]))
    # Return all reachable cells
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if visited[i][j] and not (i == x and j == y):
                if (x, y) in targets[active_player] and (i, j) not in targets[active_player]:
                    continue
                if (x, y) not in targets[enemy] and (i, j) in targets[enemy]:
                    continue
                reachableCells.append((i, j))
    print("from", x, y, "can reach", reachableCells)
    return reachableCells

# def is_valid_move(frm, to):
#     reachableCells = get_valid_moves(frm)
#     print(reachableCells)
#     if (to.i, to.j) not in reachableCells:
#         return False
#     return all([
#         board.valid_cell(to.i, to.j),
#         to.pion is None
#     ])


def dist(cell1x, cell1y, cell2x, cell2y):
    return abs(cell1x - cell2x) + abs(cell1y - cell2y)


def objective(board: Node, targets):
    value = 0
    player = Pion.BLUE if ISRED else Pion.RED
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (board.is_occupied(row, col)):
                cell = Pion.RED if (board[row][col] == 1) != ISRED else Pion.BLUE
                maxDist = -(BOARD_SIZE-1)*2  # berikan N poin jika berhasil mencapai goal
                win_cells = []
                # print("ini cell yang dicek : ", cell)
                for (iGoal, jGoal) in targets[cell]:
                    goal = Pion.RED if (board[iGoal][jGoal] == 1) != ISRED else Pion.BLUE
                    # print("ini cell goal : ", goal)
                    if not board.is_occupied(iGoal, jGoal):
                        maxDist = max(maxDist, dist(row, col, iGoal, jGoal))
                        # print(cell, goal, dist(row, col, iGoal, jGoal))
                    else:
                        win_cells.append(goal == player)

                # kalau semua sudah occupied, tapi bukan sama kita punya
                if not all(win_cells):
                    maxDist = dist(row, col, 0, 0) if player == Pion.BLUE else dist(row, col, BOARD_SIZE-1, BOARD_SIZE-1)

                # print("ini pion di ", row, col, "punya ", end="")
                if cell == player:
                    # print("pemain dengan value:", value, "ditambah", maxDist)
                    value += maxDist
                else:
                    # print("musuh dengan value :", value, "dikurang", maxDist)
                    value -= maxDist
    return -value


def check_winner(board: Node, targets):
    player = Pion.BLUE if ISRED else Pion.RED
    goal = targets[player]
    for x, y in goal:
        cell = Pion.RED if (board[x][y] == 1) != ISRED else Pion.BLUE
        if cell != player or board[x][y] == 0:
            break
    else:
        return True
    return False


if __name__ == "__main__":
    node = Node([
        [-1, -1, -1, -1,  0,  0,  0,  0],
        [-1, -1, -1,  0,  0,  0,  0,  0],
        [-1, -1,  0,  0,  0,  0,  0,  0],
        [-1,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  1],
        [0,  0,  0,  0,  0,  0,  1,  1],
        [0,  0,  0,  0,  0,  1,  1,  1],
        [0,  0,  0,  0,  1,  1,  1,  1]])
    from collections import defaultdict
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

    # TESTING OBJECTIVE FUNCTION
    node.print_debug()
    print(objective(node, TARGETS))
    node.swap(3, 0, 4, 0)
    node.print_debug()
    print(objective(node, TARGETS))
    node.swap(4, 0, 5, 0)
    node.print_debug()
    print(objective(node, TARGETS))

    # TESTING GET VALIDE MOVES FUNCTION
    print(get_valid_moves(node, 5, 0, TARGETS))
    print(get_valid_moves(node, 6, 6, TARGETS))
    print(get_valid_moves(node, 7, 7, TARGETS))

    # TESTING WIN FUNCTION
    node.swap(0, 0, 7, 7)
    node.swap(0, 1, 7, 6)
    node.swap(0, 2, 7, 5)
    node.swap(0, 3, 7, 4)
    node.swap(1, 0, 6, 7)
    node.swap(1, 1, 6, 6)
    node.swap(1, 2, 6, 5)
    node.swap(2, 0, 5, 7)
    node.swap(2, 1, 5, 6)
    node.swap(5, 0, 4, 7)
    node.print_debug()
    global ISRED
    ISRED = False
    print(check_winner(node, TARGETS))
