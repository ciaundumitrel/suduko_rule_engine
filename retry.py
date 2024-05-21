import numpy as np


class Sudoku:
    def __init__(self, board: [[]]):
        self.matrix = np.array(board)
        self.count = 0

    def check_row(self, row, number):
        return number not in self.matrix[row, :]

    def check_col(self, col, number):
        return number not in self.matrix[:, col]

    def check_square(self, i, j, number):
        i = int(i / 3)
        j = int(j / 3)

        for x in range(i * 3, i * 3 + 3):
            for y in range(j * 3, j * 3 + 3):
                if number == self.matrix[x][y]:
                    return False

        return True

    def is_valid_move(self, row, col, num):
        return (self.check_row(row, num) and
                self.check_col(col, num) and
                self.check_square(row, col, num))

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    return i, j
        return None, None

    def solve(self):
        self.count += 1
        row, col = self.find_empty_cell()
        if row is None and col is None:
            return True

        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.matrix[row][col] = num
                if self.solve():
                    return True
                self.matrix[row][col] = 0
        return False

    def get_empty_cells_mrv(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    num_possibilities = sum(1 for num in range(1, 10) if self.is_valid_move(i, j, num))
                    empty_cells.append(((i, j), num_possibilities))

        empty_cells.sort(key=lambda cell: cell[1])

        return [cell[0] for cell in empty_cells]

    def solve_with_mrv(self):
        self.count += 1
        empty_cells = self.get_empty_cells_mrv()
        if not empty_cells:
            return True

        (row, col) = empty_cells[0]
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.matrix[row][col] = num
                if self.solve_with_mrv():
                    return True

                self.matrix[row][col] = 0
        return False
