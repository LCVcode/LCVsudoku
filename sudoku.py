import random


class Sudoku:
    def __init__(self, count=0, filepath=''):
        # Generate empty cells
        self.clear()
        if len(filepath):  # Import board from file
            with open(filepath, 'r') as f:
                self.load_from_string(''.join(tuple(s.strip() for s in f.readlines())))
        elif count:  # Populate some cells
            self.random_game(count)

    @property
    def free_cells(self):
        # Counts free cells
        return sum([row.count(0) for row in self.grid])

    @classmethod
    def intersect(cls, s1, s2, s3):
        return s1.intersection(s2.intersection(s3))

    def load_from_string(self, load_string):
        '''
        Sets grid based on load_string, which must be 81 characters long
        '''
        if len(load_string) != 81:
            raise ValueError("Expected string of length 81, got string of length", len(load_string))
        for i, char in enumerate(load_string):
            self.grid[i//9][i%9] = int(char)

    def set_at(self, x, y, value):
        '''
        Sets value at (x, y)
        '''
        self.grid[x][y] = int(value)

    def get_at(self, x, y):
        '''
        Returns int value at (x, y)
        '''
        return self.grid[x][y]

    def get_options(self, x, y):
        '''
        Returns set containing all legal values for cell (x, y)
        '''
        return Sudoku.intersect(self.read_row(x),
                                self.read_col(y),
                                self.read_block(x, y))

    def read_row(self, row_id):
        '''
        Returns set containing values in row row_id
        '''
        return set([x for x in range(1, 10) if x not in self.grid[row_id]])

    def read_col(self, col_id):
        '''
        Returns set containing values in col col_id
        '''
        column = tuple([self.grid[x][col_id] for x in range(9)])
        return set([x for x in range(1, 10) if x not in column])

    def read_block(self, row_id, col_id):
        '''
        Returns set containing values in block at row_id and col_id
        '''
        row_id, col_id = row_id//3, col_id//3
        block = []
        for i in range(3):
            block.extend(self.grid[3*row_id + i][3*col_id:3*col_id+3])
        return set([x for x in range(1, 10) if x not in block])

    def print(self):
        '''
        Prints the board's state
        '''
        def _row(i: int):
            row = [str(x) if (x != 0) else ' ' for x in self.grid[i]]
            row.insert(6, '|')
            row.insert(3, '|')
            return ''.join(row)
        ref = range(3)
        bar = '\n' + '+'.join('---' for _ in ref) + '\n'
        result = bar.join(['\n'.join(_row(x+3*y) for x in ref) for y in ref])
        print(result)

    def random_game(self, n=10):
        '''
        Generates random board with n starting values
        '''
        self.clear()
        self._randomize_cell()
        while self.free_cells + n + 1 < 81:
            x, y = random.randint(0, 8), random.randint(0, 8)
            if self.grid[x][y] == 0 or (x == y == 4):
                continue
            self.grid[x][y] = 0
            self.grid[8-x][8-y] = 0

        if n % 2 == 0:
            self.grid[4][4] = 0

    def _randomize_cell(self, x=0, y=0):
        '''
        Recursively populates empty cells with legal values.
        '''
        options = list(self.get_options(x, y))
        random.shuffle(options)
        for value in options:
            self.grid[x][y] = value
            if x == 8 and y == 8:
                return True
            i, j = (x + 1) % 9, y + (x + 1) // 9
            if self._randomize_cell(i, j):
                return True
        self.grid[x][y] = 0
        return False

    def clear(self):
        '''
        Clears grid.  Every cell is reset to 0.
        '''
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
