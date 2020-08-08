import json
import pygame as pg
from sudoku import Sudoku


# Load settings
with open("visual.json", 'r') as f:
    config = json.load(f)

# Build font
pg.font.init()
font = pg.font.SysFont(config['font']['name'], 30)

def col_locations():
    # Generates left-most coordinate of each column
    for i in range(9):
        yield config['cell']['border']*(1+2*i) + \
              config['cell']['width']*(i) + \
              config['grid']['border']*2*(i//3 + 1)

def row_locations():
    # Generates top-most coordinate of each row
    for i in range(9):
        yield config['cell']['border']*(1+2*i) + \
              config['cell']['height']*(i) + \
              config['grid']['border']*2*(i//3 + 1)

def screen_size():
    # Returns screen size as tuple based on visual.json
    w = 9*config['cell']['width'] + 18*config['cell']['border'] + \
        8*config['grid']['border']
    h = 9*config['cell']['height'] + 18*config['cell']['border'] + \
        8*config['grid']['border']
    return (w, h)

def get_screen():
    # Returns screen of appropriate size
    screen = pg.display.set_mode(screen_size())
    return screen

def json_to_color(json_color):
    # Converts color format in visual.json into a tuple
    return tuple(int(x) for x in json_color.split(','))

def draw_sudoku_solve_state(screen, sudoku, box_list=[]):
    # Draws everything on screen with highlights behind cells being solved
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    screen.fill(json_to_color(config['bg']['color']))
    for ((x, y), color) in box_list:
        draw_box(screen, x, y, json_to_color(config['box'][color]))
    draw_cells(screen=screen)
    draw_values(screen=screen, sudoku=sudoku)
    pg.display.flip()

def draw_sudoku(screen, sudoku):
    # Draws everything on screen
    screen.fill(json_to_color(config['bg']['color']))
    draw_cells(screen=screen)
    draw_values(screen=screen, sudoku=sudoku)
    pg.display.flip()

def draw_cells(screen):
    # Draws all 81 cells on the screen
    color = json_to_color(config['cell']['color'])
    height, width = config['cell']['height'], config['cell']['width']
    for x in row_locations():
        for y in col_locations():
            pg.draw.rect(screen, color, pg.Rect(y, x, width, height))

def draw_values(screen, sudoku):
    # Draws cell text on the screen
    color = json_to_color(config['font']['color'])
    for i, x in enumerate(row_locations()):
        for j, y in enumerate(col_locations()):
            if (n := sudoku.getAt(i, j)) != 0:
                # TODO: Modify the location of characters to fit inside cells
                cell_text = font.render(str(n), False, color)
                screen.blit(cell_text, (y, x))

def draw_box(screen, x, y, color):
    # Draws highlights behind cells to show solve progress
    border = config['cell']['border']
    x = tuple(row_locations())[x] - border
    y = tuple(col_locations())[y] - border
    border *= 2
    box = pg.Rect(y, x, config['cell']['width']+border, config['cell']['height']+border)
    pg.draw.rect(screen, color, box)

if __name__ == '__main__':
    visual = get_screen()
    board = Sudoku(40)
    draw_sudoku_solve_state(visual, board, (((0, 0), 'highlight'), ((0, 1), 'rollback')))
    import time
    time.sleep(3)