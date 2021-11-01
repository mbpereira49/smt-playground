from z3 import *

SQUARE_ROWS = 3 # Number of rows in a square
SQUARE_COLS = 3 # Number of cols in a square
SQUARE_X = 3 # Number of squares in vertical direction
SQUARE_Y = 3 # Number of squares in horizontal direction
ROWS = SQUARE_ROWS * SQUARE_X
COLS = SQUARE_COLS * SQUARE_Y
SQUARES = SQUARE_X * SQUARE_Y

class Sudoku:
    def __init__(self, board):
        self.board = board

        self.rows = [set() for i in range(ROWS)]
        self.cols = [set() for i in range(COLS)]
        self.squares = [set() for i in range(SQUARES)]
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] != 0:
                    self._fill_box(i, j, board[i][j])

    def _fill_box(self, i, j, val):
        self.board[i][j] = val
        self.rows[i].add(val)
        self.cols[j].add(val)
        self.squares[self._get_square(i,j)].add(val)

    def _get_square(self, i, j):
        row = i//SQUARE_X
        col = j//SQUARE_Y
        return SQUARE_Y * row + col
    
    def solve(self):
        s = Solver()
        cells = [[Int(f"{i}.{j}") for j in range(COLS)] for i in range(ROWS)]
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 0:
                    s.add(cells[i][j] >= 1, cells[i][j] <= SQUARE_ROWS * SQUARE_COLS)
                    for val in self.rows[i]:
                        s.add(Not(cells[i][j] == val))
                    for val in self.cols[j]:
                        s.add(Not(cells[i][j] == val))
                    for val in self.squares[self._get_square(i, j)]:
                        s.add(Not(cells[i][j] == val))
                    self._fill_box(i, j, cells[i][j])
                else:
                    s.add(cells[i][j] == self.board[i][j])
        if s.check() == sat:
            return s.model(), cells
        else:
            return None
    
    def print_board(self, board, accessor):
        for i in range(ROWS):
            for j in range(COLS):
                rep = accessor(board[i][j])
                print(rep, end=' ')
            print()