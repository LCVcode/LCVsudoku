# SudokuSolver
SudokuSolver is a sudoku generator and solver built in Python.  

## Installation
Clone repository with 
```
git clone git@github.com:LCVcode/SudokuSolver.git
```
Install dependencies with 
```
pip install -r requirements.txt
```

## Usage
To watch a Sudoku solve, run `python main.py X`, where X can be a path to a file or [natural number](https://en.wikipedia.org/wiki/Natural_number).

If X is a file path, the Sudoku game at that location will be rendered and solved.  
For example:
```
python main.py board/easy00.txt
```

If X is an integer, a random Sudoku game with X filled cells will be generated and solved.  
For example:
```
python main.py 25
```

### Configuation
The values in visual.json are intended to be modified to your liking.
Every visual element is adjustable, with further functionality to come.

## What I Learned
* GitHub Actions
* Pytest
* Pygame 2D graphics
* GitHub repository management
* Depth-first search
* Python 'yield'
* Refined json skills
* Git practice

## Contact
Connor Chamberlain - lcvcode@gmail.com
