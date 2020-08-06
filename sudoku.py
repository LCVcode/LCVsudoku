import random

class Sudoku:
    def __init__(self, count=0):
        self.clear()
        if count:
            self.random_game(count)

    @property
    def free_cells(self):
        return sum([row.count(0) for row in self.grid])

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
        return set([x for x in range(1, 10) if x not in self.grid[row_id]])

    def readCol(self, col_id: int) -> set:
        '''
        Returns set containing values in col col_id
        '''
        column = tuple([self.grid[x][col_id] for x in range(9)])
        return set([x for x in range(1, 10) if x not in column])

    def readBlock(self, row_id: int, col_id: int) -> set:
        '''
        Returns set containing values in block at row_id and col_id
        '''
        row_id, col_id = row_id//3, col_id//3
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
        print(result)


    def random_game(self, count: int = 10):
        '''
        Populates count number of cells with a random legal value
        '''
        self.clear()
        self._randomize_cell()
        while self.free_cells + count + 1 < 81:
            x, y = random.randint(0, 8), random.randint(0, 8)
            if self.grid[x][y] == 0 or (x == y == 4):
                continue
            self.grid[x][y] = 0
            self.grid[8-x][8-y] = 0

        if count%2==0:
            self.grid[4][4] = 0

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
