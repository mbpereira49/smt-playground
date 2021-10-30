from z3 import *

N = 3

class Sudoku:
    def __init__(self, board):
        self.board = board

        self.rows = [set() for i in range(N * N)]
        self.cols = [set() for i in range(N * N)]
        self.squares = [set() for i in range(N * N)]
        for i in range(N * N):
            for j in range(N * N):
                if board[i][j] != 0:
                    self.fill_box(i, j, board[i][j])

    def fill_box(self, i, j, val):
        self.board[i][j] = val
        self.rows[i].add(val)
        self.cols[j].add(val)
        self.squares[self.get_square(i,j)].add(val)

    def get_square(self, i, j):
        row = i//N
        col = j//N
        return N * row + col
    
    def solve(self):
        s = Solver()
        vars = [[None for i in range(N*N)] for j in range(N*N)]
        for i in range(N * N):
            for j in range(N * N):
                if board[i][j] == 0:
                    vars[i][j] = Int('{0}.{1}'.format(i + 1, j + 1))
                    s.add(vars[i][j] >= 1, vars[i][j] <= N * N)
                    for val in self.rows[i]:
                        s.add(Not(vars[i][j] == val))
                    for val in self.cols[j]:
                        s.add(Not(vars[i][j] == val))
                    for val in self.squares[self.get_square(i, j)]:
                        s.add(Not(vars[i][j] == val))
                    self.fill_box(i, j, vars[i][j])
                else:
                    vars[i][j] = Int('{0}.{1}'.format(i + 1, j + 1))
                    s.add(vars[i][j] == self.board[i][j])
        print(s.check())
        return s.model()

#board = [[None, 2, 1, None], [4, None, None, 3], [2, None, None, 1], [1, None, None, None]]


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

lst = []
for var in m:
    lst.append((var, m[var]))

sorted_lst = sorted(lst, key = lambda tup: str(tup[0]))
for i in range(N * N):
    for j in range(N * N):
       print(sorted_lst[N * N * i + j][1], end=' ')
    print()