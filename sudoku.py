import random

class Sudoku:
    def __init__(self):
        self.clear()

    @classmethod
    def clamp(cls, value: int, low: int, high: int):
        '''
        Returns int(value) clamped between low and high
        '''
        return max(low, min(high, int(value)))

    @classmethod
    def rowColClamp(cls, i: int) -> int:
        '''
        Clamps i between 0 and 8, to match list indices
        '''
        return Sudoku.clamp(i, 0, 8)

    @classmethod
    def blockClamp(cls, i):
        '''
        Clamps i between 0 and 2, to match block sizes
        '''
        return Sudoku.clamp(i, 0, 2)

    def setAt(self, x, y, value):
        '''
        Sets one value in the grid
        '''
        self.grid[x][y] = value

    def getAt(self, x, y) -> int:
        '''
        Returns value at (x, y)
        '''
        return self.grid[x][y]

    def getOptions(self, x, y) -> set:
        '''
        Returns set containing all legal values for cell (x, y)
        '''
        return self.readRow(x).intersection(self.readCol(y)).intersection(self.readBlock(x, y))

    def readRow(self, row_id: int) -> set:
        '''
        Returns set containing values in row row_id
        '''
        row_id = Sudoku.rowColClamp(row_id)
        return set([x for x in range(1, 10) if x not in self.grid[row_id]])

    def readCol(self, col_id: int) -> set:
        '''
        Returns set containing values in col col_id
        '''
        col_id = Sudoku.rowColClamp(col_id)
        column = tuple([self.grid[x][col_id] for x in range(9)])
        return set([x for x in range(1, 10) if x not in column])

    def readBlock(self, row_id: int, col_id: int) -> set:
        '''
        Returns set containing values in block at row_id and col_id
        '''
        row_id, col_id = Sudoku.blockClamp(row_id // 3), Sudoku.blockClamp(col_id // 3)
        block = []
        for i in range(3):
            block.extend(self.grid[3*row_id + i][3*col_id:3*col_id+3])
        return set([x for x in range(1, 10) if x not in block])

    def print(self):
        def _rowPrintable(i: int):
            row = [str(x) if (x!=0) else ' ' for x in self.grid[i]]
            row.insert(6, '|')
            row.insert(3, '|')
            return ''.join(row)
        ref = range(3)
        bar = '\n' + '+'.join('---' for _ in ref) + '\n'
        result = bar.join(['\n'.join(_rowPrintable(x+3*y) for x in ref) for y in ref])
        # result = '\n'.join(_rowPrintable(x) for x in ref)
        print(result)

    def solve(self, i: int = 0):
        '''
        Solves sudoku game
        '''
        if i == 81:
            return True
        # print(i)
        x, y = i // 9, i % 9
        if (self.grid[x][y] != 0):
            return self.solve(i + 1)
        for k in self.getOptions(x, y):
            self.setAt(x, y, k)
            if self.solve(i + 1):
                return True
        self.setAt(x, y, 0)
        return False

    def random_game(self, count: int = 10):
        '''
        Populates count number of cells with a random legal value
        '''
        self.clear()
        self._randomize_cell()
    
    def _randomize_cell(self, x=0, y=0):
        options = list(self.getOptions(x, y))
        random.shuffle(options)
        for value in options:
            self.grid[x][y] = value
            if x==8 and y==8:
                return True
            if self._randomize_cell((x+1)%9, y+(x+1)//9):
                return True
        self.grid[x][y] = 0
        return False


    def clear(self):
        '''
        Clears grid.  Every cell is reset to 0.
        '''
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

if __name__ == '__main__':
    test = Sudoku()

    test.random_game(count=30)
    print("Randomly generated Sudoku board:")
    test.print()
    print()
    test.solve()
    print("Solution:")
    test.print()
