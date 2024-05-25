import tkinter as tk
from tkinter import messagebox
import random
from sudoku2 import Sudoku
import rule_engine
from SudokuGenerator import SudokuGenerator

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.create_widgets()

    def create_widgets(self):
        self.entries = [[tk.Entry(self.root, width=3, font=('Arial', 18), justify='center') for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.grid(row=10, column=3, columnspan=3, pady=10)

        self.example1_button = tk.Button(self.root, text="Example 1", command=self.load_example1)
        self.example1_button.grid(row=11, column=2, columnspan=2, pady=5)

        self.example2_button = tk.Button(self.root, text="Example 2", command=self.load_example2)
        self.example2_button.grid(row=11, column=4, columnspan=2, pady=5)

        self.random_button = tk.Button(self.root, text="Random Board", command=self.generate_random_board)
        self.random_button.grid(row=11, column=6, columnspan=2, pady=5)

    def load_example1(self):
        board = [
            [8, 2, 7, 3, 1, 6, 0, 4, 9],
            [6, 4, 9, 7, 5, 0, 8, 3, 1],
            [0, 3, 1, 4, 8, 9, 6, 7, 0],
            [7, 0, 0, 6, 0, 1, 2, 0, 0],
            [2, 1, 0, 5, 0, 7, 0, 0, 6],
            [4, 9, 6, 0, 0, 0, 1, 5, 7],
            [1, 8, 0, 0, 2, 4, 7, 0, 0],
            [0, 6, 0, 0, 7, 3, 0, 1, 0],
            [3, 7, 4, 1, 0, 0, 0, 0, 0]
        ]
        self.load_board(board)

    def load_example2(self):
        board = [
            [8, 4, 0, 0, 5, 0, 0, 0, 0],
            [3, 0, 0, 6, 0, 8, 0, 4, 0],
            [0, 0, 0, 4, 0, 9, 0, 0, 0],
            [0, 2, 3, 0, 0, 0, 8, 9, 0],
            [1, 0, 0, 8, 0, 0, 0, 0, 4],
            [0, 9, 8, 0, 0, 0, 1, 6, 0],
            [0, 0, 0, 5, 0, 3, 0, 0, 0],
            [0, 3, 0, 1, 0, 6, 0, 0, 7],
            [0, 0, 0, 0, 2, 0, 0, 1, 3]
        ]
        self.load_board(board)


    def generate_random_board(self):
        sudoku_generator = SudokuGenerator()
        board = sudoku_generator.get_board()
        self.load_board(board)

    def load_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def solve(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    row.append(int(value))
                else:
                    row.append(0)
            board.append(row)
        for row in board:
            print(row)
        sudoku = Sudoku(board=board)
        
        with open('log.txt', 'w') as f:
            if sudoku.solve_rules(f):
                for d in sudoku.cells:
                    sudoku.matrix[d['row']][d['col']] = d['value']
                for i in range(9):
                    for j in range(9):
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, str(sudoku.matrix[i][j]))
                messagebox.showinfo("Sudoku Solver", "Solution found!")
            else:
                messagebox.showinfo("Sudoku Solver", "There is no solution.")

if __name__ == '__main__':
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
