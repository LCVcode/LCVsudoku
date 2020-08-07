import time

from sudoku import Sudoku
from visual import draw_sudoku_solve_state, get_screen


def solve(sudoku, i=0):
    '''
    Solves sudoku game
    '''
    if i == 81:
        return True
    x, y = i // 9, i % 9
    if (sudoku.grid[x][y] != 0):
        return solve(sudoku, i + 1)
    for k in sudoku.getOptions(x, y):
        sudoku.setAt(x, y, k)
        if solve(sudoku, i + 1):
            return True
    sudoku.setAt(x, y, 0)
    return False

def animate_solve(screen, sudoku, i=0):
    '''
    Solves sudoku game and animates each step
    '''
    if i == 81:
        return True
    x, y = i // 9, i % 9
    if (sudoku.grid[x][y] != 0): # Skip populated cells
        return animate_solve(screen, sudoku, i + 1)
    for k in sudoku.getOptions(x, y): # Loop through possible values
        sudoku.setAt(x, y, k)
        draw_sudoku_solve_state(screen, sudoku, [((x, y), 'highlight')])
        time.sleep(0.02)
        if animate_solve(screen, sudoku, i + 1):
            return True
    sudoku.setAt(x, y, 0)
    draw_sudoku_solve_state(screen, sudoku, [((x, y), 'rollback')])
    return False


if __name__ == '__main__':
    test = Sudoku(20)
    # print("Sudoku Board:")
    # test.print()6
    # print()
    # solve(test)
    # print("Solution:")
    # test.print()
    screen = get_screen()
    animate_solve(screen, test)
