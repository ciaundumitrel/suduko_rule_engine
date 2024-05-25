import random

class SudokuGenerator:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.generate_sudoku()

    def is_valid(self, row, col, num):
        if num in self.board[row]:
            return False
        for i in range(9):
            if self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def solve_sudoku(self):
        empty_location = self.find_empty_location()
        if not empty_location:
            return True 

        row, col = empty_location

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0

        return False

    def generate_full_board(self):
        self.solve_sudoku()

    def remove_numbers(self, num_holes):
        count = 0
        while count < num_holes:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

    def generate_sudoku(self):
        self.generate_full_board()
        self.remove_numbers(50)

    def get_board(self):
        return self.board
