from globals import BOARD_SIZE
from cell import Cell
from pion import Pion


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