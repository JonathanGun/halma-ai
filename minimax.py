from node import Node
import timeit
from typing import Tuple

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

    def __init__(self, config):
        """
        docstring
        """
        self.__start_time = timeit.default_timer()

        val, move = self.__max_value(Node(config), float('-inf'), float('inf'))

        self.result = move
    
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

    def __min_value(self, node : Node, alpha : int, beta : int, depth : int, max_depth : int) -> Tuple[int, int]:
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
        (value, move) : Tuple[int, int]
            value is the score of node
            move is the move done to make the node
        """
        best_move = None
        best_value = float('inf')

        # Return if we have reached the bottom of the tree or ...
        # ... node is a win state of ...
        # ... time limit exceeded
        if depth == max_depth or !!boardIsAWinner or self.__compute_time() > !!T_LIMIT:
            return !!objective(board), best_move

        # Loop through all pawns for this player
        for row, i in node:
            for data, j in row:
                x1, y1 = i, j
                if (config[i][j] == 1):

                    # Loop through all valid moves for a pawn
                    for x2, y2 in !!getValidMoves(frm):

                        # Stop generating children if time limit exceeded
                        if self.__compute_time() > !!T_LIMIT:
                            return best_value, best_move
                        
                        # Get value of child node
                        child_node = node.copy()
                        child_node.swap(x1, y1, x2, y2)
                        val, move = self.__max_value(child_node, alpha, beta, depth + 1, max_depth)

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

    def __max_value(self, node : Node, alpha : int, beta : int, depth : int, max_depth : int) -> Tuple[int, int]:
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
        (value, move) : Tuple[int, int]
            value is the score of node
            move is the move done to make the node
        """
        best_move = None
        best_value = float('-inf')

        # Return if we have reached the bottom of the tree or ...
        # ... node is a win state of ...
        # ... time limit exceeded
        if depth == max_depth or !!boardIsAWinner or self.__compute_time() > !!T_LIMIT:
            return !!objective(board), best_move

        # Loop through all pawns for this player
        for row, i in node:
            for data, j in row:
                x1, y1 = i, j
                if (config[i][j] == 1):

                    # Loop through all valid moves for a pawn
                    for x2, y2 in !!getValidMoves(frm):

                        # Stop generating children if time limit exceeded
                        if self.__compute_time() > !!T_LIMIT:
                            return best_value, best_move
                        
                        # Get value of child node
                        child_node = node.copy()
                        child_node.swap(x1, y1, x2, y2)
                        val, move = self.__min_value(child_node, alpha, beta, depth + 1, max_depth)

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

if __name__ == "__main__":
    pass