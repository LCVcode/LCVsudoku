from sudoku import Sudoku


def solve(sudoku, i=0):
    '''
    Solves sudoku game
    '''
    if i == 81:
        return True
    # print(i)
    x, y = i // 9, i % 9
    if (sudoku.grid[x][y] != 0):
        return solve(sudoku, i + 1)
    for k in sudoku.getOptions(x, y):
        sudoku.setAt(x, y, k)
        if solve(sudoku, i + 1):
            return True
    sudoku.setAt(x, y, 0)
    return False


if __name__ == '__main__':
    test = Sudoku(20)
    print("Sudoku Board:")
    test.print()
    print()
    solve(test)
    print("Solution:")
    test.print()
