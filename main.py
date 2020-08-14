import sys

from solver import animate_solve, get_screen, Sudoku

value = sys.argv[1]

try:
    board = Sudoku(count=int(value))
except ValueError:
    board = Sudoku(filepath=value)

screen = get_screen()
animate_solve(screen, board)
