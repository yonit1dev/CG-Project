import pygame as pyg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def init():
    # Window initializations
    pyg.init()
    display_size = (1000, 700)
    caption = 'Tower of Hanoi Simulation Project'

    # Display settings
    pyg.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pyg.display.set_caption(caption)

    # Set opengl version
    pyg.display.gl_set_attribute(pyg.GL_CONTEXT_MAJOR_VERSION, 4)
    pyg.display.gl_set_attribute(pyg.GL_CONTEXT_MINOR_VERSION, 1)
    pyg.display.gl_set_attribute(pyg.GL_CONTEXT_PROFILE_MASK, pyg.GL_CONTEXT_PROFILE_CORE)

    glClearColor(0.3, 0.2, 0.2, 1.0)
    glViewport(0, 0, 1000, 700)

def game_const():

    global moves, max_disks, selected_disks, selected_tower, disk_selected

    moves = 0
    max_disks = 3

    selected_disks = []
    selected_tower = 0
    disk_selected = False
    
def towers():

    # Left tower
    glBegin(GL_QUADS)

    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 0)

    glEnd()

    # Color overspill protection
    glColor4f(1, 1 ,1, 1)

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
