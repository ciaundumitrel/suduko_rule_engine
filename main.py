from sudoku import Sudoku


def get_all_items(x, y, z):
    all_items = []

    seen = set()  # Keep track of seen values to avoid duplicates
    for gen in (x, y, z):
        for item in gen:
            item_tuple = tuple(item.items()) if isinstance(item, dict) else item
            if item_tuple not in seen:
                all_items.append(item)
                seen.add(item_tuple)
    return all_items


def get_len(r, c, s):
    pos = 0
    try:
        for _ in r:
            print(_)
            pos += 1
    except:
        pass
    try:
        for _ in c:
            print(_)

            pos += 1
    except:
        pass

    try:
        for _ in s:
            print(_)

            pos += 1
    except:
        pass

    return pos

def get_pos(r, c, s):
    pos = []
    print(type(s))
    for y in r:
        print(y)
    try:
        for _ in r:
            print(type(_))
    except Exception as e:
        print(e)
    try:
        for _ in c:
            print(type(_))
    except Exception as e:
        print(e)
    try:
        for _ in s:
            print(type(_))
    except Exception as e:
        print(e)

    print(pos)
    return pos


if __name__ == "__main__":

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
            [0, 0, 0, 0, 2, 0, 0, 1, 3]]
    )

    possibilities = {}
    for i in range(9):
        for j in range(9):
            pos_len = 0
            pos = []
            sudoku_copy = sudoku.copy()
            for y in range(1, 10):
                if (i, j) not in sudoku.solved_cells:
                    filtered_row = sudoku.filter_row(row=j, value=y)
                    filtered_col = sudoku.filter_col(col=i, value=y)
                    filtered_square = sudoku.filter_square(col=i, row=j, value=y)
                    pos_len = get_len(filtered_row, filtered_col, filtered_square)
                    pos = get_pos(filtered_row, filtered_col, filtered_square)
            possibilities.update({(i, j): pos_len})

    print(possibilities)

    # while filtered:
    #     try:
    #         print(next(filtered))
    #     except StopIteration:
    #         print('done')
    #         break

    # cells = init_cells()
    # print(cells)
    # solve(cells)
