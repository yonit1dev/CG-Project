import pygame as pyg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Global game constants
# moves, max_disks, total_curr_disks, selected_tower, disk_selected = None
window = None

class ColorConstants:

    def __init__(self):
        self.colors = {}

        # Colors for game
        self.colors['cyan'] = (0, 255, 255)
        self.colors['burgundy'] = (128, 0, 32)
        self.colors['mattegrey'] = (152, 152, 156)
        self.colors['whitesmoke'] = (255, 255, 255)
        self.colors['matteblack'] = (0, 0, 0)


def init():

    global window

    # Window initializations
    pyg.init()
    display_size = (800, 600)
    caption = 'Tower of Hanoi Simulation Project'

    # Display settings
    window = pyg.display.set_mode(display_size)
    pyg.display.set_caption(caption)

# Game constant declarations
def game_const():

    global moves, max_disks, total_curr_disks, selected_tower, disk_selected

    moves = 0 # Moves the player makes
    max_disks = 3 # Number of max disks permitted

    total_curr_disks = [] # Selected disks by user
    selected_tower = 0 # Current pointing tower
    disk_selected = False # Disk selected

def towers():
    
    global window

    color = ColorConstants()

    for horizontal_coordinate in range (120, 540 + 1, 200):

        pyg.draw.rect(window, color.colors['cyan'], pyg.Rect(horizontal_coordinate, 400, 160, 25))

        pyg.draw.rect(window, color.colors['mattegrey'], pyg.Rect(horizontal_coordinate + 75, 200, 20, 175))


def main():
    init()
    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                quit()

        towers()
        pyg.display.flip()
        pyg.time.wait(10)

main()
