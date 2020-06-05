import unittest
from sudoku import Sudoku

class TestSudokuReads(unittest.TestCase):
    def setUp(self):
        self.sudoku = Sudoku()
        for i in range(9):
            self.sudoku.grid[i][i] =  i + 1
        self.sudoku.grid[0][1] = 5
    def test_set_and_get(self):
        self.sudoku.clear()
        for i in range(9):
            self.assertEqual(self.sudoku.grid[i].count(0), 9)
        self.sudoku.setAt(5, 5, 5)
        self.assertEqual(self.sudoku.grid[5][5], 5)
        self.assertEqual(self.sudoku.getAt(5, 5), 5)
        self.sudoku.clear()
        for i in range(9):
            self.sudoku.setAt(i, i, i + 1)
        self.sudoku.setAt(0, 1, 5)
    def test_read_row(self):
        self.assertSetEqual(self.sudoku.readRow(0), {2, 3, 4, 6, 7, 8,9})
        self.assertSetEqual(self.sudoku.readRow(1), {1, 3, 4, 5, 6, 7, 8, 9})
        self.assertSetEqual(self.sudoku.readCol(1), {1, 3, 4, 6, 7, 8, 9})
        self.assertSetEqual(self.sudoku.readBlock(0, 0), self.sudoku.readBlock(1, 1))
        self.assertSetEqual(self.sudoku.readBlock(0, 0), {4, 6, 7, 8, 9})
        self.assertSetEqual(self.sudoku.getOptions(2, 1), {4, 6, 7, 8, 9})
