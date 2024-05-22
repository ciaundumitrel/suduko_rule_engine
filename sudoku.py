import numpy as np

from Cell import Cell
from rule_engine import Rule


class Sudoku:
    def __init__(self, board: [[]] = None, cells=None):
        self.matrix = board

        if not cells:
            self.cells = self.init_cells(board)
        else:
            self.cells = cells

        self.solved_cells = []

    def find_empty_cell_with_rules(self):
        for row in range(9):
            for col in range(9):
                rule = Rule(f'row == {row} and col == {col} and value == 0 ')
                match = rule.filter(self.cells)
                _ = 0
                for m in match:
                    _ += 1
                if _ > 0:
                    return row, col
        return None, None

    def solve_rules(self, f):
        row, col = self.find_empty_cell_with_rules()

        if row is None and col is None:
            return True

        for value in range(1, 10):
            if self.is_valid_move(row, col, value):
                remove = self.get_cells_without(row, col)
                self.cells.remove(remove)
                self.cells.append({'row': row, 'col': col, 'value': value})
                f.write(f'wrote   [{row}:{col}] >> {value} \n')
                if self.solve_rules(f):
                    return True
                f.write(f'erased  [{row}:{col}] << {value} \n')

                self.cells.append({'row': row, 'col': col, 'value': 0})
                self.cells.remove({'row': row, 'col': col, 'value': value})
        return False

    def get_cells_without(self, row, col):
        rule = Rule(f' row == {row} and col == {col}')

        matches = rule.filter(self.cells)
        for _ in matches:
            return _
        return None

    def is_valid_move(self, row, col, num):
        return (self.check_row(row, num) and
                self.check_col(col, num) and
                self.check_square(row, col, num))

    @staticmethod
    def init_cells(board):
        return [Cell(i, j, board[i][j]).as_dict() for i in range(9) for j in range(9)]

    def match_row(self, row, value):
        if not value:
            return

        rule = Rule(f' row == {row} and value == {value}')
        data = self.cells[0]
        return rule.matches(data)

    def valid_move(self, row, col):
        rule = Rule(f' row == {row} and col == {col} and value != 0')
        return rule.filter(self.cells)

    def match_col(self, col, value):
        if not value:
            return

        rule = Rule(f' col == {col} and value != {value}')
        data = self.cells[0]
        return rule.matches(data)

    def check_row(self, row, value):
        if not value:
            return

        rule = Rule(f'row == {row} and value == {value} ')
        matches = rule.filter(self.cells)
        for _ in matches:
            return False
        return True

    def check_col(self, col, value):
        if not value:
            return

        rule = Rule(f' col == {col} and value == {value}')
        matches = rule.filter(self.cells)
        for _ in matches:
            return False
        return True

    def check_square(self, row, col, value):

        col = int(col / 3)
        row = int(row / 3)
        rule = Rule(
            f"col >= {col * 3} and col <= {col * 3 + 2} and row >= {row * 3} and row <= {row * 3 + 2} "
            f"and value == {value}")

        matches = rule.filter(self.cells)
        for _ in matches:
            return False
        return True

    def count_zeroes(self):
        return sum([1 for d in self.cells if d['value'] == 0])
