from __future__ import annotations
from typing import List


class Node:
    """
    Represents a node on a tree generated by the minimax algorithm.

    Attributes
    ----------
    None

    Methods
    -------
    copy() -> Node
        Creates a new instance of the node with the same configurations
    swap(x1 : int, y1 : int, x2 : int, y2 : int)
        Swaps the contents of two cells
    print_debug()
        Prints the current configuration of the node
    """

    def __init__(self, config: List[List[int]]) -> None:
        """
        Constructs all necessary attributes for a single node.

        Parameters
        ----------
        config : List[List[int]]
            A 2d list of size row x col containing -1, 0, or 1 where...
                1 is the current piece
                0 is an empty cell
                -1 is an opposing piece
        """

        self.config = config

    def __getitem__(self, item):
        if (isinstance(item, (int, slice))):
            return self.config[item]
        return [self.config[i] for i in item]

    def copy(self) -> Node:
        """
        Creates a new instance of the node with the same configurations

        Parameters
        ----------
        None

        Returns
        -------
        new_node : int
            The new node with same configurations
        """
        return Node(self.config.copy())

    def swap(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Swaps the contents of two cells

        Parameters
        ----------
        x1 : int
            The 0-based x position of the first cell
        y1 : int
            The 0-based y position of the first cell
        x2 : int
            The 0-based x position of the second cell
        y2 : int
            The 0-based y position of the second cell

        Returns
        -------
        None
        """
        self.config[x1][y1], self.config[x2][y2] = self.config[x2][y2], self.config[x1][y1]

    def valid_cell(self, x: int, y: int) -> bool:
        """
        Returns true if the cell is a valid cell

        Parameters
        ----------
        x : int
            The 0-based x position of the cell
        y : int
            The 0-based y position of the cell

        Returns
        -------
        is_occupied : book
            True if the cell is within the bounds of the grid
        """
        if (x >= 0 and x < len(self.config)):
            if (y >= 0 and y < len(self.config[x])):
                return True
        return False

    def is_occupied(self, x: int, y: int) -> bool:
        """
        Returns true if the selected cell is occupied

        Parameters
        ----------
        x : int
            The 0-based x position of the cell
        y : int
            The 0-based y position of the cell

        Returns
        -------
        is_occupied : bool
            True if the cell is occupied
        """
        return self.valid_cell(x, y) and self.config[x][y] != 0

    def print_debug(self) -> None:
        """
        Prints the current configuration of the node 

        The configuration is printed with the format:

        A1 B1 C1 ⋯

        A2 B2 C2 ⋯

        A3 B3 C3 ⋯

         ⋮  ⋮  ⋮  ⋱

        With O as the current player, X as the opposing player, and _ as an empty cell

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for row in self.config:
            for item in row:
                if (item == 1):
                    print("O", end=" ")
                elif (item == -1):
                    print("X", end=" ")
                else:
                    print("_", end=" ")
            print()


if __name__ == "__main__":
    node = Node([[1, 1, 0], [1, 0, -1], [0, -1, -1]])
    node.print_debug()
    node.swap(0, 0, 2, 2)
    node.print_debug()
