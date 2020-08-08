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
        self.sudoku.set_at(5, 5, 5)
        self.assertEqual(self.sudoku.grid[5][5], 5)
        self.assertEqual(self.sudoku.get_at(5, 5), 5)
        self.sudoku.clear()
        for i in range(9):
            self.sudoku.set_at(i, i, i + 1)
        self.sudoku.set_at(0, 1, 5)
    def test_read_row(self):
        self.assertSetEqual(self.sudoku.read_row(0), {2, 3, 4, 6, 7, 8,9})
        self.assertSetEqual(self.sudoku.read_row(1), {1, 3, 4, 5, 6, 7, 8, 9})
        self.assertSetEqual(self.sudoku.read_col(1), {1, 3, 4, 6, 7, 8, 9})
        self.assertSetEqual(self.sudoku.read_block(0, 0), self.sudoku.read_block(1, 1))
        self.assertSetEqual(self.sudoku.read_block(0, 0), {4, 6, 7, 8, 9})
        self.assertSetEqual(self.sudoku.get_options(2, 1), {4, 6, 7, 8, 9})
