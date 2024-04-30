from Cell import Cell
from rule_engine import Rule


class Sudoku:
    def __init__(self, board: [[]], cells=None, solved_cells=None):
        self.solved_cells = []
        if solved_cells:
            self.solved_cells = solved_cells

        self.cells = []
        if cells:
            self.cells = cells
        else:
            self.cells = self.get_cells(board)

        self.filtered = None

    def get_cells(self, board: [[]]):
        cells = []
        for i in range(0, 9):
            for j in range(0, 9):
                val = board[i][j]
                if val:
                    cells.append(Cell(i, j, val, True).as_dict())
                    self.solved_cells.append((i, j))

                else:
                    cells.append(Cell(i, j, y, False).as_dict() for y in range(1, 10))
        return cells

    def filter_row(self, row, value):
        if not value:
            return

        rule = Rule(f' row == {row} and value != {value}')

        self.filtered = rule.filter(self.cells)
        return self.filtered

    def filter_col(self, col, value):
        if not value:
            return

        rule = Rule(f' col == {col} and value != {value}')
        self.filtered = rule.filter(self.cells)
        return self.filtered

    def filter_square(self, col, row, value):
        col = int(col / 3)
        row = int(row / 3)

        rule = Rule(f"col >= {col * 3} and col <= {col * 3 + 3} and row >= {row * 3}  and row <= {row * 3 + 3} "
                    f"and value != {value}")
        self.filtered = rule.filter(self.cells)
        return self.filtered

    def copy(self):
        return Sudoku(cells=self.cells, solved_cells=self.solved_cells, board=None)
