from PyQt5.QtWidgets import *
from sudoku import Sudoku

class Cell(QStackedWidget):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.button = QPushButton()
        self.static = QLabel()

        self.addWidget(self.button)
        self.addWidget(self.static)

        self.value = 0
        self.options = []

        self.setFixedSize(26, 26)

    def setButton(self):
        self.setCurrentIndex(0)
        self.button.setText('')

    def setStatic(self, value: int):
        self.setCurrentIndex(1)
        self.static.setText(str(value))

class ButtonGrid(QWidget):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # Build cells
        self.cells = [Cell() for _ in range(81)]

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
        self.clearButton.clicked.connect(self.clear)

    def readSudokuBoard(self):
        cells = self.parent.grid.cells
        for x in range(9):
            for y in range(9):
                value = self.parent.sudoku.getAt(x, y)
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


class SettingsPanel(QWidget):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # Build buttons and check boxes
        self.autoOptions = QCheckBox('Auto Options', self)

        # Add widgets to layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.autoOptions)


class SudokuViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.sudoku = Sudoku()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LCV Sudoku')

        # Setup widgets
        self.grid = ButtonGrid(self)
        self.stack = QStackedWidget(self)
        self.tabs = QTabWidget(self)
        self.actionsPanel = ActionsPanel(self)
        self.settingsPanel = SettingsPanel(self)

        # Build tabs
        self.stack.addWidget(self.tabs)
        self.tabs.addTab(self.actionsPanel, 'Actions')
        self.tabs.addTab(self.settingsPanel, 'Settings')

        # Add widgets to layout
        self.baseLayout = QHBoxLayout(self)
        self.baseLayout.addWidget(self.grid)
        self.baseLayout.addWidget(self.stack)

        self.show()

app = QApplication([])
ex = SudokuViewer()
app.exec_()
