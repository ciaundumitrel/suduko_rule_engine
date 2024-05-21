from Cell import Cell
from rule_engine import Rule


class Sudoku:
    def __init__(self, board: [[]]):
        self.matrix = board
        self.cells = self.init_cells(board)
        self.solved_cells = []
        self.possibilities = None
        self.possibilities_count = None

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
                if min_pos < self.possibilities_count[i][j]:
                    min_pos = self.possibilities_count[i][j]
                    min_row = i
                    min_col = j

        pos_count = self.possibilities_count
        pos_count[min_row][min_col] -= 1

        pos = self.possibilities
        new_move = pos[min_row][min_col].pop()

        return min_row, min_col, new_move, pos, pos_count

    @staticmethod
    def init_cells(board):
        return [Cell(i, j, board[i][j]).as_dict() for i in range(9) for j in range(9) if board[i][j] != 0]

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

    def filter_row(self, row, value):
        if not value:
            return

        rule = Rule(f'row == {row} and value == {value} ')
        return rule.filter(self.cells)

    def filter_col(self, col, value):
        if not value:
            return

        rule = Rule(f' col == {col} and value == {value}')
        return rule.filter(self.cells)

    def filter_square(self, row, col, value):
        col = int(col / 3)
        row = int(row / 3)

        rule = Rule(f"col >= {col * 3 - 1} and col <= {col * 3 + 3 - 1} and row >= {row * 3 - 1}  and row <= {row * 3 + 3 -1 } "
                    f"and value == {value}")

        return rule.filter(self.cells)
    #
    # def copy(self):
    #     return Sudoku(cells=self.cells, solved_cells=self.solved_cells, board=None)
