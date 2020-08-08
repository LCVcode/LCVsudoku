import pytest

from sudoku import Sudoku

@pytest.fixture
def sudoku():
    return Sudoku()

def test_sudoku_getters(sudoku):
    for i in range(9):
        assert sudoku.get_at(i, i) == 0

def test_sudoku_setters(sudoku):
    for i in range(9):
        sudoku.set_at(i, i, i)

        assert sudoku.get_at(i, i) == i

def test_sudoku_read_row(sudoku):
    sudoku.set_at(0, 0, 2)
    sudoku.set_at(0, 1, 5)
    sudoku.set_at(0, 2, 3)
    sudoku.set_at(0, 3, 1)

    assert sudoku.read_row(0) == {4, 6, 7, 8, 9}

def test_sudoku_read_col(sudoku):
    sudoku.set_at(1, 0, 4)
    sudoku.set_at(2, 0, 5)
    sudoku.set_at(3, 0, 3)
    sudoku.set_at(4, 0, 1)

    assert sudoku.read_col(0) == {2, 6, 7, 8, 9}

def test_sudoku_read_block(sudoku):
    sudoku.set_at(3, 3, 1)
    sudoku.set_at(4, 3, 3)
    sudoku.set_at(3, 4, 5)
    sudoku.set_at(5, 5, 9)

    assert sudoku.read_block(3, 3) == {2, 4, 6, 7, 8}
    assert sudoku.read_block(3, 3) == sudoku.read_block(4, 4)