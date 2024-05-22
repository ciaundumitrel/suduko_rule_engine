from Cell import Cell
from rule_engine import Rule
import time as time

class Sudoku:
    def __init__(self, board: [[]] = None, cells=None):
        self.matrix = board

        if not cells:
            self.cells = self.init_cells(board)
            self.init_posibilities()
        else:
            self.cells = cells

        self.solved_cells = []

    def find_empty_cell_with_rules(self):
        for row in range(9):
            for col in range(9):
                rule = Rule(f'row == {row} and col == {col} and value == 0 ')
                match = rule.filter(self.cells)
                if any(match) > 0:
                    return row, col
        return None, None

    
    def is_valid_move(self, row, col, num):
        return (self.check_row(row, num) and
                self.check_col(col, num) and
                self.check_square(row, col, num))

    def solve_rules(self, f, use_mrv = False):
        row, col, posibilities = self.find_empty_cell_with_rules_mrv() # first cell with value 0
        if row is None and col is None:
            return True

        startTime = time.time()
        for value in posibilities:
            if self.is_valid_move(row, col, value):
                # remove = self.get_cells_without(row, col)
                remove = [cell for cell in self.cells if cell["row"] == row and cell["col"] == col][0]
                self.cells.remove(remove)
                self.cells.append({'row': row, 'col': col, 'value': value, 'posibilities': set()})
                f.write(f'wrote   [{row}:{col}] >> {value} \n')
                if self.solve_rules(f):
                    print(time.time() - startTime)
                    return True
                f.write(f'erased  [{row}:{col}] << {value} \n')

                self.cells.append({'row': row, 'col': col, 'value': 0, 'posibilities': posibilities})
                self.cells.remove({'row': row, 'col': col, 'value': value, 'posibilities': set()})
        return False
           
    def check_square(self, row, col, value):
        col = int(col / 3)
        row = int(row / 3)
        rule = Rule(
            f"col >= {col * 3} and col <= {col * 3 + 2} and row >= {row * 3} and row <= {row * 3 + 2} "
            f"and value == {value}")

        matches = rule.filter(self.cells)
        return not any(matches)
    
    def check_row(self, row, value):
        if not value:
            return

        rule = Rule(f'row == {row} and value == {value} ')
        matches = rule.filter(self.cells)
        return not any(matches)
    
    def check_col(self, col, value):
        if not value:
            return

        rule = Rule(f'col == {col} and value == {value}')
        matches = rule.filter(self.cells)
        return not any(matches)
    
    def match_col(self, col, value):
        if not value:
            return

        rule = Rule(f' col == {col} and value != {value}')
        data = self.cells[0]
        return rule.matches(data)
    
    def match_row(self, row, value):
        if not value:
            return

        rule = Rule(f' row == {row} and value == {value}')
        data = self.cells[0]
        return rule.matches(data)

    def get_cells_without(self, row, col):
        rule = Rule(f'row == {row} and col == {col}')
        matches = rule.filter(self.cells)
        return next(matches, None)

    def valid_move(self, row, col):
        rule = Rule(f' row == {row} and col == {col} and value != 0')
        return rule.filter(self.cells)
    
    def find_posibilities(self, row, col):
        if row is None or col is None:
            return set()

        results = set()
        default_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for index in range(0, 9):
            row_values_rule = Rule(f'row == {row} and col == {index} and value != 0')
            row_values_rule_match = row_values_rule.filter(self.cells)
            for element in row_values_rule_match:
                results.add(element["value"])

            col_values_rule = Rule(f'row == {index} and col == {col} and value != 0')
            col_values_rule_match = col_values_rule.filter(self.cells)
            for element in col_values_rule_match:
                results.add(element["value"])
        return default_set - results
        
    def find_empty_cell_with_rules_mrv(self):
        sorted_data = sorted(self.cells, key=lambda x: len(x["posibilities"]))
        for el in sorted_data:
            if len(el["posibilities"]) > 0:
                return el["row"], el["col"], el["posibilities"]
            
        return None, None, None

    @staticmethod
    def init_cells(board):
        return [Cell(i, j, board[i][j]).as_dict() for i in range(9) for j in range(9)]
    
    def init_posibilities(self):
        rule = Rule(f'value == 0')
        w_cells = rule.filter(self.cells)
        for cell in w_cells:
            cell["posibilities"] = self.find_posibilities(cell["row"], cell["col"])