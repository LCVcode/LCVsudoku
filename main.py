import sys

from solver import animate_solve, get_screen, Sudoku


screen = get_screen()
board = Sudoku(int(sys.argv[1]))
animate_solve(screen, board)
