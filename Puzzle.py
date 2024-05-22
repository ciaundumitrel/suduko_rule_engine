import numpy as np

from Cell import Cell
from rule_engine import Rule


class Sudoku:
    def __init__(self, board: [[]] = None, cells=None, possibilities=None, possibilities_count=None):
        if possibilities_count is None:
            possibilities_count = []
        if possibilities is None:
            possibilities = []
        self.count = 0
        self.matrix = np.array(board)

        if not cells:
            self.cells = self.init_cells(board)
        else:
            self.cells = cells

        self.solved_cells = []
        self.possibilities = possibilities
        self.possibilities_count = possibilities_count

    def set_possibilities(self, possibilities):
        self.possibilities = possibilities

    def set_possibilities_count(self, possibilities_count):
        self.possibilities_count = possibilities_count

    def get_best_move(self) -> (int, int, int, [[]], [[]]):
        """
        :return: row, col, value, pos, pos_count
        """
        min_row = 10
        min_col = 10
        min_pos = 10
        for i in range(9):
            for j in range(9):
                if min_pos > self.possibilities_count[i][j] >= 1 and self.matrix[i][i] == 0:
                    min_pos = self.possibilities_count[i][j]
                    min_row = i
                    min_col = j

        new_move = self.possibilities[min_row][min_col][0]

        return [min_row, min_col, new_move]

    @staticmethod
    def sum_gens(*gens):
        return all(not any(gen) for gen in gens)

    def find_empty_cell_good(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    return i, j
        return None, None

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

    def solve(self):
        self.cells = self.init_cells(self.matrix)
        row, col = self.find_empty_cell_good()
        if row is None and col is None:
            return True

        for value in range(1, 10):
            if self.is_valid_move_basic(row, col, value):
                self.matrix[row][col] = value

                if self.solve():
                    return True
                self.matrix[row][col] = 0

        return False

    def solve_rules(self, f):
        self.count += 1
        row, col = self.find_empty_cell_with_rules()
        if row is None and col is None:
            return True

        for value in range(1, 10):
            if self.is_valid_move(row, col, value):
                self.matrix[row][col] = value
                f.write(f"on [{row} : {col}] wrote   {value} \n")
                if self.solve():
                    return True
                self.matrix[row][col] = 0
                f.write(f"on [{row} : {col}] deleted {value} \n")

        return False

    def check_row_basic(self, row, number):
        return number not in self.matrix[row, :]

    def check_col_basic(self, col, number):
        return number not in self.matrix[:, col]

    def check_square_basic(self, i, j, number):
        i = int(i / 3)
        j = int(j / 3)

        for x in range(i * 3, i * 3 + 3):
            for y in range(j * 3, j * 3 + 3):
                if number == self.matrix[x][y]:
                    return False

        return True

    def is_valid_move_basic(self, row, col, num):
        return (self.check_row_basic(row, num) and
                self.check_col_basic(col, num) and
                self.check_square_basic(row, col, num))

    def is_valid_move(self, row, col, num):
        return (self.check_row(row, num) and
                self.check_col(col, num) and
                self.check_square(row, col, num))

    def calculate_possibilities(self):
        for i in range(9):
            self.possibilities.append([])
            for j in range(9):
                self.possibilities[i].append([])

        for i in range(9):
            self.possibilities_count.append([])
            for j in range(9):
                self.possibilities_count[i].append(0)

        for row in range(0, 9):
            for col in range(0, 9):
                for value in range(1, 10):
                    already_set = False
                    for _ in self.valid_move(row, col):
                        already_set = True

                    if not already_set:
                        filter_row = self.filter_row(row, value)
                        filter_col = self.filter_col(col, value)
                        filter_square = self.filter_square(row, col, value)
                        is_valid = self.sum_gens(filter_row, filter_col, filter_square)

                        if is_valid:
                            self.possibilities_count[row][col] += 1
                            self.possibilities[row][col].append(value)

    @staticmethod
    def init_cells(board):
        return [Cell(i, j, board[i][j]).as_dict() for i in range(9) for j in range(9)]

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
            f"col >= {col * 3 - 1} and col <= {col * 3 + 3 - 1} and row >= {row * 3 - 1}  and row <= {row * 3 + 3 - 1} "
            f"and value == {value}")

        matches = rule.filter(self.cells)
        for _ in matches:
            return False
        return True

    def copy(self):
        return Sudoku(cells=self.cells, board=self.matrix, possibilities=self.possibilities,
                      possibilities_count=self.possibilities_count)
