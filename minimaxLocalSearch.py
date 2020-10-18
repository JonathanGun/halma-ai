from node import Node
from typing import List, Tuple
from minimax import Minimax
import random

class MinimaxLocalSearch(Minimax):
    def __init__(self, targets, config: List[List[int]], t_limit: float, active_player, n_restart: int = None):
        super().__init__(targets, config, t_limit, active_player)
        self.n_restart = n_restart
        
    def __find_pawns(self, node, active_player) -> List[Tuple[int,int]]:
        result = super().__find_pawns(node, active_player)
        return random.shuffle(result)[:self.n_restart]

if __name__ == "__main__":
    node = [
        [-1, -1,  0, -1,  0,  0,  0,  0], 
        [-1, -1,  0,  0,  0,  0,  0,  0], 
        [-1, -1,  0, -1,  0,  0,  0,  0],
        [-1,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0, -1,  0,  1],
        [ 0,  0,  0,  0,  0,  0,  1,  1],
        [ 0,  0,  0,  0,  0,  1,  1,  1],
        [ 0,  0,  0,  0,  1,  1,  1,  1]]
    from collections import defaultdict
    from pion import Pion
    from globals import BOARD_SIZE
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
    
    print(MinimaxLocalSearch(targets = TARGETS, config = node, t_limit = 10, n_restart=3).result)