from sudoku import Sudoku, ROWS, COLS

board = [
    [0, 0, 9, 0, 0, 0, 0, 2, 0],
    [2, 4, 0, 7, 0, 0, 0, 0, 1],
    [0, 0, 6, 0, 4, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 0, 0],
    [4, 1, 0, 0, 3, 0, 0, 5, 0],
    [0, 0, 0, 9, 0, 0, 3, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 0, 0, 7],
    [5, 3, 0, 0, 9, 0, 0, 1, 0]
]

sud = Sudoku(board)
m = sud.solve()
cells = sud.cells

def access(elt):
    return m.eval(elt)

sud.print_board(cells, access)