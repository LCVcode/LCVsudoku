from PyQt5.QtWidgets import *
from sudoku import Sudoku


class Cell(QStackedWidget):
    '''
    Cells display values from the Sudoku grid and are selectable by the user
    '''
    def __init__(self, parent: QWidget, *a, **kw):
        super().__init__(parent, *a, **kw)
        self.parent = parent
        self.value = 0
        # self.options = []

        self.button = QPushButton()
        self.static = QLabel()

        self.addWidget(self.button)
        self.addWidget(self.static)

        self.setFixedSize(26, 26)

        self.button.clicked.connect(lambda: self.parent.parent.toggleMode(self))

    def setButton(self):
        ''' Sets cell to button mode and clears any text'''
        self.setCurrentIndex(0)
        self.button.setText('')

    def setStatic(self, value: int):
        ''' Sets cell to static mode and displays value'''
        self.setCurrentIndex(1)
        self.value = value
        self.static.setText(str(self.value))

    def setValue(self, value: int):
        ''' Changes value displayed in button mode'''
        print(f'Setting value to {value} from {self.value}')
        self.value = value
        self.button.setText(str(self.value))


class ButtonGrid(QWidget):
    def __init__(self, parent: QWidget, *a, **kw):
        super().__init__(parent, *a, **kw)
        self.parent = parent

        # Build cells
        self.cells = [Cell(parent=self) for _ in range(81)]

        # Build layout and add widgets
        self.layout = QGridLayout(self)
        for row in range(9):
            for col in range(9):
                self.layout.addWidget(self.cells[9*row + col], row, col)


class ActionsPanel(QWidget):
    def __init__(self, parent: QWidget, *a, **kw):
        super().__init__(parent, *a, **kw)
        self.parent = parent

        # Build buttons
        self.randomButton = QPushButton('Random')
        self.resetButton = QPushButton('Reset')
        self.solveButton = QPushButton('Solve')
        self.clearButton = QPushButton('Clear')

        # Build layout and add widgets 
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.randomButton)
        self.layout.addWidget(self.solveButton)
        self.layout.addWidget(self.resetButton)
        self.layout.addWidget(self.clearButton)

        # Setup button connections
        self.randomButton.clicked.connect(self.random)
        self.resetButton.clicked.connect(self.reset)
        self.clearButton.clicked.connect(self.clear)

    def readSudokuBoard(self):
        '''
        Reads sudoku board and sets fixed values on the grid
        '''
        cells = self.parent.grid.cells
        for x in range(9):
            for y in range(9):
                value = self.parent.sudoku.get_at(x, y)
                button = cells[9*x + y]
                if value == 0:
                    button.setButton()
                else:
                    button.setStatic(str(value))

    def random(self):
        self.parent.sudoku.partialPopulate(18)
        self.readSudokuBoard()

    def clear(self):
        self.parent.sudoku.clear()
        self.readSudokuBoard()

    def reset(self):
        for cell in self.parent.grid.cells:
            if cell.currentIndex() == 0:
                cell.setButton()

class SettingsPanel(QWidget):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # Build buttons and check boxes
        self.autoOptions = QCheckBox('Auto Options', self)

        # Add widgets to layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.autoOptions)


class NumpadKey(QPushButton):
    def __init__(self, parent: QWidget, value: int, *a, **kw):
        super().__init__(parent, *a, **kw)
        self.parent = parent
        self.value = value
        self.setText(str(self.value))

        self.clicked.connect(lambda: self.parent.numPressed(self.value))


class Numpad(QWidget):
    def __init__(self, parent: QWidget, *a,  **kw):
        super().__init__(parent, *a, **kw)
        self.parent = parent

        # Build keys
        # self.keys = [QPushButton(text=str(x)) for x in range(1, 10)]
        self.nums = []
        for x in range(1, 10):
            self.nums.append(NumpadKey(self, x))
        self.clearCellButton = QPushButton(text='Clear Cell')

        # Build layout
        self.layout = QGridLayout(self)
        for i in range(9):
            x, y = i // 3, i % 3
            self.layout.addWidget(self.nums[i], x, y)
        self.layout.addWidget(self.clearCellButton, 4, 0, 3, 0)
        
        # Set up connections
        self.clearCellButton.clicked.connect(self.clearCell)
        for i, key in enumerate(self.nums):
            print(f'Setting key connection value to {i + 1}')
            key.clicked.connect(lambda: self.numPressed(i + 1))

    def clearCell(self):
        self.parent.activeCell.setButton()
        self.parent.toggleMode(None)

    def numPressed(self, value: int):
        self.parent.activeCell.setValue(value)
        self.parent.toggleMode(None)


class SudokuViewer(QWidget):
    VIEW = 0
    EDIT = 1
    def __init__(self):
        super().__init__()
        self.sudoku = Sudoku()
        self.mode = self.VIEW
        self.initUI()
        self.activeCell = None

    def initUI(self):
        self.setWindowTitle('LCV Sudoku')

        # Setup widgets
        self.grid = ButtonGrid(self)
        self.stack = QStackedWidget(self)
        self.tabs = QTabWidget(self)
        self.numpad = Numpad(self)
        self.actionsPanel = ActionsPanel(self)
        self.settingsPanel = SettingsPanel(self)

        # Build tabs and stack
        self.stack.addWidget(self.tabs)
        self.stack.addWidget(self.numpad)
        self.tabs.addTab(self.actionsPanel, 'Actions')
        self.tabs.addTab(self.settingsPanel, 'Settings')

        # Add widgets to layout
        self.baseLayout = QHBoxLayout(self)
        self.baseLayout.addWidget(self.grid)
        self.baseLayout.addWidget(self.stack)

        self.show()

    def toggleMode(self, activeCell: Cell):
        '''
        Toggles the current mode between EDIT and VIEW
        '''
        self.mode = (self.EDIT, self.VIEW)[self.mode]
        self.stack.setCurrentIndex(self.mode)
        self.activeCell = activeCell

if __name__ == '__main__':
    app = QApplication([])
    ex = SudokuViewer()
    app.exec_()
