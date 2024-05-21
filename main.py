from pprint import pprint

from sudoku import Sudoku
import rule_engine
import itertools


def sum_gens(*gens):
    valid = True
    for gen in gens:
        for _ in gen:
            if _:
                valid = False

    return valid


if __name__ == '__main__':
    sudoku = Sudoku(
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
    possibilities = list()
    for i in range(9):
        possibilities.append([])
        for j in range(9):
            possibilities[i].append([])

    possibilities_count = list()
    for i in range(9):
        possibilities_count.append([])
        for j in range(9):
            possibilities_count[i].append(0)

    context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
        'row': rule_engine.DataType.FLOAT,
        'col': rule_engine.DataType.FLOAT,
        'value': rule_engine.DataType.FLOAT,
    }))

    def solve_sudoku(sudoku):
        for row in range(0, 9):
            for col in range(0, 9):
                for value in range(1, 10):
                    already_set = False

                    for _ in sudoku.valid_move(row, col):
                        already_set = True

                    if not already_set:
                        filter_row = sudoku.filter_row(row, value)
                        filter_col = sudoku.filter_col(col, value)
                        filter_square = sudoku.filter_square(row, col, value)
                        is_valid = sum_gens(filter_row, filter_col, filter_square)

                        if is_valid:
                            possibilities_count[row][col] += 1
                            possibilities[row][col].append(value)

                        print(row, col, value)
                        print(f"{is_valid=}")

        sudoku.set_possibilities(possibilities)
        sudoku.set_possibilities_count(possibilities_count)
        pprint(possibilities)

    solve_sudoku(sudoku)
