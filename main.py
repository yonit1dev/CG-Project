import pygame as pyg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Global game constants
# moves, max_disks, total_curr_disks, selected_tower, disk_selected = None

class GameConstants:

    def __init__(self) -> None:
        self.window = None
        self.max_disks = 3
        self.total_curr_disks = []

class ColorConstants:

    def __init__(self):
        self.colors = {}

        # Colors for game
        self.colors['cyan'] = (0, 255, 255)
        self.colors['burgundy'] = (128, 0, 32)
        self.colors['mattegrey'] = (152, 152, 156)
        self.colors['whitesmoke'] = (255, 255, 255)
        self.colors['matteblack'] = (0, 0, 0)

# Game constant class
game = GameConstants()
color = ColorConstants()

def init():

    global game

    # Window initializations
    pyg.init()
    display_size = (800, 600)
    caption = 'Tower of Hanoi Simulation Project'

    # Display settings
    game.window = pyg.display.set_mode(display_size)
    pyg.display.set_caption(caption)

# Game constant declarations
def game_const():

    global moves, max_disks, total_curr_disks, selected_tower, disk_selected

    moves = 0 # Moves the player makes
    max_disks = 3 # Number of max disks permitted

    total_curr_disks = [] # Selected disks by user
    selected_tower = 0 # Current pointing tower
    disk_selected = False # Disk selected

# Tower drawing function
def towers():
    
    global game, color

    for horizontal_coordinate in range (120, 540 + 1, 200):

        pyg.draw.rect(game.window, color.colors['mattegrey'], pyg.Rect(horizontal_coordinate, 400, 160, 15))

        pyg.draw.rect(game.window, color.colors['burgundy'], pyg.Rect(horizontal_coordinate + 70, 200, 20, 200))

# Disk drawing function
def disk_properties():

    global game, color

    height = 25
    vertical_coordinate = 397 - height
    width = game.max_disks * 23

    for i in range(game.max_disks):
        disk = {}
        disk['rect'] = pyg.Rect(50, 50, width, height)
        disk['rect'].midtop = (120, vertical_coordinate)
        disk['val'] = game.max_disks - i
        disk['tower'] = 0
        game.total_curr_disks.append(disk)
        vertical_coordinate -= height + 3
        width -= 23

def draw_disk():
    global game, color

    for disk in game.total_curr_disks:
        pyg.draw.rect(game.window, color.colors['cyan'], disk['rect'])
    
    return

def main():
    init()
    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                quit()

        towers()
        disk_properties()
        draw_disk()

        pyg.display.flip()
        pyg.time.wait(10)

main()
