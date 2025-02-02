from node import Node
import timeit
from typing import List, Tuple
from pion import Pion
from helper_functions import objective, get_valid_moves, check_winner
import numpy as np


class Minimax():
    """
    A class containing all functions required to run the minimax algorithm

    Attributes
    ----------
    (from, to) : Tuple[Tuple[int, int], Tuple[int, int]]
        from is a tuple representing the x, y coordinate of the moved pawn
        to is a tuple representing the x, y coordinate of the destination

    Methods
    -------
    None
    """

    def __init__(self, targets, config: List[List[int]], t_limit: float, active_player):
        """
        Constructs all necessary attributes to run the minimax function

        Parameters
        ----------
        config : List[List[int]]
            A 2d list of size row x col containing -1, 0, or 1 where...
                1 is the current piece
                0 is an empty cell
                -1 is an opposing piece
        t_limit : float
            The time limit for running the minimax algorithm
        """
        self.__start_time = timeit.default_timer()
        self.T_LIMIT = t_limit - 0.0025  #
        self.targets = targets
        self.bot = active_player

        max_depth = 2
        best_value = float("-inf")
        best_move = None
        while (self.__compute_time() < self.T_LIMIT):
            val, move = self.__max_value(Node(config), float('-inf'), float('inf'), 0, max_depth, active_player)
            # self.__print_node(val, move, 0)
            # print("max_depth:", max_depth)
            max_depth += 1
            if max_depth > 5:
                break
            if (best_value < val):
                best_value = val
                best_move = move

        self.result = best_move

    def __compute_time(self) -> float:
        """
        Gets how long the object has been alive

        For use locally.

        Parameters
        ----------
        None

        Returns
        -------
        run_time : float
            The amount of time the object has been alive, in seconds
        """
        return timeit.default_timer() - self.__start_time

    def __find_pawns(self, node, active_player) -> List[Tuple[int, int]]:
        # find all child
        result = []
        for i in range(len(node.config)):
            for j in range(len(node[i])):
                if (node[i][j] == (1 if (active_player == self.bot) else -1)):
                    result.append((i, j))
        # print("available pion:", result)
        return result

    def __min_value(self, node: Node, alpha: int, beta: int, depth: int, max_depth: int, active_player) -> Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Picks the best move where the best move is the children with the worst objective value

        Parameters
        ----------
        node : Node
            The node containing the current configuration
        alpha : int
            Alpha value in alpha-beta pruning
        beta : int
            Beta value in alpha-beta pruning
        depth : int
            The current depth of node on the generated tree
        max_depth : int
            The maximum tree depth that can be generated

        Returns
        -------
        (value, (from, to))) : Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]
            value is the score of node
            from is a tuple representing the x, y coordinate of the moved pawn
            to is a tuple representing the x, y coordinate of the destination
        """
        best_move = None
        best_value = float('inf')

        # Return if we have reached the bottom of the tree or ...
        # ... node is a win state of ...
        # ... time limit exceeded
        if depth == max_depth or check_winner(node, self.targets, active_player) or self.__compute_time() > self.T_LIMIT:
            return objective(node, self.targets, self.bot), best_move

        # Loop through all pawns for this player
        pawns = self.__find_pawns(node, active_player)
        for (i, j) in pawns:
            x1, y1 = i, j

            # Loop through all valid moves for a pawn
            for x2, y2 in get_valid_moves(node, i, j, self.targets, active_player):

                # Stop generating children if time limit exceeded
                if self.__compute_time() > self.T_LIMIT:
                    return best_value, best_move

                # Get value of child node
                child_node = node.copy()
                child_node.swap(x1, y1, x2, y2)
                val, move = self.__max_value(child_node, alpha, beta, depth + 1, max_depth, Pion.RED if active_player == Pion.BLUE else Pion.BLUE)
                # self.__print_node(val, ((x1, y1), (x2, y2)), depth + 1)

                # Check if this child node is better
                if (val < best_value):
                    best_value = val
                    best_move = ((x1, y1), (x2, y2))
                    beta = min(beta, val)

                # Pruning - check if there is no use generating more children
                if (best_value <= alpha):
                    return best_value, best_move

        # Return the best value
        return best_value, best_move

    def __max_value(self, node: Node, alpha: int, beta: int, depth: int, max_depth: int, active_player) -> Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Picks the best move where the best move is the children with the best objective value

        Parameters
        ----------
        node : Node
            The node containing the current configuration
        alpha : int
            Alpha value in alpha-beta pruning
        beta : int
            Beta value in alpha-beta pruning
        depth : int
            The current depth of node on the generated tree
        max_depth : int
            The maximum tree depth that can be generated

        Returns
        -------
        (value, (from, to)) : Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]
            value is the score of node
            from is a tuple representing the x, y coordinate of the moved pawn
            to is a tuple representing the x, y coordinate of the destination
        """
        best_move = None
        best_value = float('-inf')

        # Return if we have reached the bottom of the tree or ...
        # ... node is a win state of ...
        # ... time limit exceeded
        if depth == max_depth or check_winner(node, self.targets, active_player) or self.__compute_time() > self.T_LIMIT:
            return objective(node, self.targets, self.bot), best_move
        # Loop through all pawns for this player
        pawns = self.__find_pawns(node, active_player)
        for (i, j) in pawns:
            x1, y1 = i, j

            # Loop through all valid moves for a pawn
            for x2, y2 in get_valid_moves(node, i, j, self.targets, active_player):

                # Stop generating children if time limit exceeded
                if self.__compute_time() > self.T_LIMIT:
                    return best_value, best_move

                # Get value of child node
                child_node = node.copy()
                child_node.swap(x1, y1, x2, y2)
                val, move = self.__min_value(child_node, alpha, beta, depth + 1, max_depth, Pion.RED if active_player == Pion.BLUE else Pion.BLUE)
                # self.__print_node(val, ((x1, y1), (x2, y2)), depth + 1)

                # Check if this child node is better
                if (val > best_value):
                    best_value = val
                    best_move = ((x1, y1), (x2, y2))
                    alpha = max(alpha, val)

                # Pruning - check if there is no use generating more children
                if (beta <= best_value):
                    return best_value, best_move

        # Return the best value
        return best_value, best_move

    def __print_node(self, value, move, depth):
        """
        docstring
        """
        if depth > 1:
            return
        for i in range(depth):
            print("\t", end="")
        print(value, move)


if __name__ == "__main__":
    node = [
        [-1, -1,  0, -1,  0,  0,  0,  0],
        [-1, -1,  0,  0,  0,  0,  0,  0],
        [-1, -1,  0, -1,  0,  0,  0,  0],
        [-1,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0, -1,  0,  1],
        [0,  0,  0,  0,  0,  0,  1,  1],
        [0,  0,  0,  0,  0,  1,  1,  1],
        [0,  0,  0,  0,  1,  1,  1,  1]]
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

    print(Minimax(TARGETS, node, 10).result)
