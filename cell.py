from kivy.uix.button import Button
from pion import Pion
from globals import BOARD_SIZE

selected_cell = None


def enemy(pion):
    return Pion((pion + 1) % 2)


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

    def __init__(self, i, j, pion=None, game=None, **kwargs):
        self.i = i
        self.j = j
        self.pion = pion
        self.is_highlighted = False
        self.is_reachable = False
        self.game = game

        super().__init__(**kwargs)
        self.bind(on_press=self._on_press)
        self.background_color = Cell.colors.get(self.pion, Cell.default_color)

    def get_background_color(self):
        if self.is_reachable:
            return Cell.reachable_color
        if self.is_selected:
            return Cell.selected_colors.get(self.pion, Cell.default_color)
        if self.pion is None:
            for base, targets in self.game.TARGETS.items():
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

        if self.game.active_player.mode == "Human":
            # First click
            if selected_cell is None:
                if instance.pion == self.game.active_player.pion:
                    instance.set_selected(True)

                    # Highlight selected cell
                    selected_cell.set_highlighted(True)

                    # Highlight reachable cells
                    frm = selected_cell
                    reachableCells = self.game.get_valid_moves(frm)
                    for reachableCell in reachableCells:
                        self.game.board.board[reachableCell[0]][reachableCell[1]].set_reachable(True)

            # Second click
            else:
                if selected_cell == instance:
                    # Revert reachable cells
                    reachableCells = self.game.get_valid_moves(selected_cell)
                    for reachableCell in reachableCells:
                        self.game.board.board[reachableCell[0]][reachableCell[1]].set_reachable(False)

                    selected_cell = None
                    instance.set_selected(False)

                else:
                    frm = selected_cell
                    to = instance
                    self._on_press(frm)
                    move_success = self.game.move(frm, to)

                    # Revert reachable cells
                    reachableCells = self.game.get_valid_moves(frm)
                    for reachableCell in reachableCells:
                        if reachableCell[0] == to.i and reachableCell[1] == to.j:
                            continue
                        else:
                            self.game.board.board[reachableCell[0]][reachableCell[1]].set_reachable(False)

                    # Revert frm if move success
                    if move_success:
                        self.game.next_turn()
                    else:
                        self._on_press(to)

    def is_inside_board(self):
        return 0 <= self.i < BOARD_SIZE and 0 <= self.j < BOARD_SIZE

    def __str__(self):
        return f"({self.i}, {self.j})"
