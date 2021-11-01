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

        # Create a 
        self.rows = [set() for i in range(ROWS)]
        self.cols = [set() for i in range(COLS)]
        self.squares = [set() for i in range(SQUARES)]

        self.cells = [[Int(f"{i}.{j}") for j in range(COLS)] for i in range(ROWS)]


    def solve(self):
        s = Solver()
        for i in range(ROWS):
            for j in range(COLS):

                if self.board[i][j] != 0:
                    # If a number on the board is fixed, add a constraint requiring this
                    s.add(self.cells[i][j] == self.board[i][j])
                else:
                    # Otherwise the cell can be any number in the range
                    s.add(self.cells[i][j] >= 1, self.cells[i][j] <= SQUARE_ROWS * SQUARE_COLS)

                # Add row, column, and box constraints, compared to cells already processed
                s = self._add_neq_constraints(s, self.cells[i][j], self.rows[i])
                s = self._add_neq_constraints(s, self.cells[i][j], self.cols[j])
                s = self._add_neq_constraints(s, self.cells[i][j], self.squares[self._get_square(i, j)])

                # Add this cell to row, column, and box sets to indicate that it has been processed
                self._fill_cell(i, j, self.cells[i][j])
                
        if s.check() == sat:
            return s.model()
        else:
            return None
    
    def print_board(self, board, accessor = lambda x : x):
        for i in range(ROWS):
            for j in range(COLS):
                rep = accessor(board[i][j])
                print(rep, end=' ')
            print()

    def _add_neq_constraints(self, solver, cell, iterator):
        for val in iterator:
            solver.add(Not(cell == val))
        return solver

    def _fill_cell(self, i, j, cell):
        self.rows[i].add(cell)
        self.cols[j].add(cell)
        self.squares[self._get_square(i,j)].add(cell)

    def _get_square(self, i, j):
        row = i//SQUARE_X
        col = j//SQUARE_Y
        return SQUARE_Y * row + col
    