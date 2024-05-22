from pprint import pprint

from sudoku import Sudoku
import rule_engine

if __name__ == '__main__':
    easy_sudoku = Sudoku(
        board=[
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
    )

    # merge super greu??????????????? gen vreo 5 - 10 minute
    hard_sudoku = Sudoku(
        board=[
            [8, 4, 0, 0, 5, 0, 0, 0, 0],
            [3, 0, 0, 6, 0, 8, 0, 4, 0],
            [0, 0, 0, 4, 0, 9, 0, 0, 0],
            [0, 2, 3, 0, 0, 0, 8, 9, 0],
            [1, 0, 0, 8, 0, 0, 0, 0, 4],
            [0, 9, 8, 0, 0, 0, 1, 6, 0],
            [0, 0, 0, 5, 0, 3, 0, 0, 0],
            [0, 3, 0, 1, 0, 6, 0, 0, 7],
            [0, 0, 0, 0, 2, 0, 0, 1, 3]],
    )

    context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
        'row': rule_engine.DataType.FLOAT,
        'col': rule_engine.DataType.FLOAT,
        'value': rule_engine.DataType.FLOAT,
    }))

    with open('log.txt', 'w') as f:
        if easy_sudoku.solve_rules(f, True):
            print("Solution found:")
            for d in easy_sudoku.cells:
                easy_sudoku.matrix[d['row']][d['col']] = d['value']
            for line in easy_sudoku.matrix:
                print(line)

        else:
            print("There is no solution.")
