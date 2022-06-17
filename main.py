import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global Variables 
breite = 0.1
stnagebreite = 0.025
slices = 32
inner_slices = 16
loops = 1
frames = 64
fem = 1000 / frames
fsem = 0.001

class Config:

    def __init__(self):

        self.gap = None
        self.tower_radius = None
        self.tower_height = None

class Move:

    def __init__(self):

        self.fromTower = None
        self.toTower = None
        self.next = None
    
    def setNext(self):
        self.next = Move()
    

class Moves:

    def __init__(self):

        self.head = None
        self.tail = None
    
    def setHeadTail(self):
        self.head = Move()
        self.tail = Move()

class Disc:

    def __init__(self):

        self.color = None
        self.rad = None

        self.next = None
        self.prev = None
    
    def setAdj(self):
        self.next = Disc()
        self.prev = Disc()

class Stack:

    def __init__(self):

        self.top = Disc()
        self.bottom = Disc()

# Game Variables
disks = 3
rotX = 1.5
rotY = 1.5
zoom = 1.5
offsetY = 1.5
speed = 0
quadricObj = None
pos = None

tower = [Stack(), Stack(), Stack()]
tower_height = [0, 0, 0]

config = Config()
moves = Moves()
moves.setHeadTail()

curMove = Move()
curMove.setNext()

currDisc = Disc()
currDisc.setAdj()

duration = None
max_moves = None
draw = 0
seconds = "Time: 0s"


def hanoi(queue, n, tower1, tower2, tower3):

    curMove = Move() 
    curMove.setNext()

    if n > 0:
        hanoi(queue, n - 1, tower1, tower3, tower2)

        curMove.next = None
        curMove.fromTower = tower1
        curMove.toTower = tower3

        if(queue.head == None):
            queue.head = curMove

        if(queue.tail != None):
            queue.tail.next = curMove
        
        queue.tail = curMove
        
        hanoi(queue, n - 1, tower2, tower1, tower3)

def add_to_tower(tower, disc):

    disc.next = None

    if(tower.bottom == None):
        tower.bottom = disc
        tower.top = disc
        disc.prev = None
    else:
        tower.top.next = disc
        disc.prev = tower.top
        tower.top = disc

def rem_from_tower(tower):

    if tower.top != None:
        temp = tower.top

        if tower.top.prev != None :
            tower.top.prev.next = None
            tower.top = temp.prev
        else:
            tower.bottom = None
            tower.top = None
        
        return temp
    
    return None

def draw_disc(quadric, outer, inner):

    global breite, slices, loops, inner_slices, quadricObj

    glPushMatrix()

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(quadric, outer, outer, breite, slices, loops)
    gluQuadricOrientation(quadric, GLU_INSIDE)

    if inner > 0:
        gluCylinder(quadric, inner, inner, breite, inner_slices, loops)
        gluDisk(quadric, inner, outer, slices, loops)
        gluQuadricOrientation(quadric, GLU_OUTSIDE)
        glTranslatef(0.0, 0.0, breite)
        gluDisk(quadric, inner, outer, slices, loops)
        gluQuadricOrientation(quadric, GLU_OUTSIDE)
    
    glPopMatrix()

def draw_tower(quadric, radius, height):

    global breite, stnagebreite, slices, loops, inner_slices

    glPushMatrix()

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(quadric, radius, radius, breite / 2, slices, loops)
    gluQuadricOrientation(quadric, GLU_INSIDE)

    gluDisk(quadric, 0.0, radius, slices, loops)
    gluQuadricOrientation(quadric, GLU_OUTSIDE)

    glTranslatef(0.0, 0.0, breite / 2)
    gluDisk(quadric, 0.0, radius, slices, loops)
    gluCylinder(quadric, stnagebreite, stnagebreite, height, inner_slices, loops)

    glTranslatef(0.0, 0.0, height)
    gluDisk(quadric, 0.0, stnagebreite, inner_slices, loops)

    glPopMatrix()

def draw_all_towers(quadric, radius, height, gap):

    glPushMatrix()

    draw_tower(quadric, radius, height)
    glTranslatef(-gap, 0.0, 0.0)
    draw_tower(quadric, radius, height)
    glTranslatef(gap * 2, 0.0, 0.0)
    draw_tower(quadric, radius, height)

    glPopMatrix()

def drawString(x_pos, y_pos, z_pos, font, msg):

    glRasterPos3f(x_pos, y_pos, z_pos)

    for char in msg:
        glutBitmapCharacter(font, char)

def add_disc_to_tower():

    global duration, draw

    i = None

    current = Disc()

    radius = 0.1 * disks

    for i in range(disks):

        current.radius = radius
        current.color = str(i % 6)

        add_to_tower(tower[0], current)
        radius -= 0.1
    
    duration = 0
    draw = 0

def hanoi_init():

    global breite, fsem, fem, config, max_moves, moves, curMove, currDisc, pos, speed, disks

    speed = fsem * fem
    radius = 0.1 * disks

    config.tower_radius = radius + 0.1
    config.tower_height = disks * breite + 0.2
    config.gap = (radius * 2) + 0.5

    max_moves = (2 ** (disks - 1)) - 1

    add_disc_to_tower()
    moves.head = None

    hanoi(moves, disks, 0, 1, 2)
    curMove = moves.head
    currDisc = rem_from_tower(tower[int(curMove.fromTower)])
    pos = 0.001
    
def init():

    global quadricObj

    mat_specular = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
    mat_shininess = np.array([50.0], dtype=np.float32)
    light_position = np.array([0.0, 1.0, 1.0, 0.0])

    glShadeModel(GL_SMOOTH)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glClearColor(1.0, 1.0, 1.0, 1.0)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glCullFace(GL_BACK)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)

    quadricObj = gluNewQuadric()
    gluQuadricNormals(quadricObj, GLU_SMOOTH)


def display():

    global zoom, offsetY, quadricObj, config, breite, tower_height, tower, stnagebreite, curMove, currDisc

    i = None
    movY = None

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0.0, 0.0, 0.0)

    gluLookAt(0.0, 0.9, 3.6 + zoom, 0.0, offsetY, 0.0, 0.0, 1.0, 0.0)

    glRotatef(rotY, 0.0, 1.0, 0.0)
    glRotatef(rotX, 0.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.5)

    draw_all_towers(quadricObj, config.tower_radius, config.tower_height, config.gap)
    glTranslatef(-config.gap, breite / 2, 0.0)

    glPushMatrix()

    for i in range(3):
        glPushMatrix()
        tower_height[i] = 0

        cur = tower[i].bottom

        if (cur != None):
            while(cur != None):
                cur.color = glColor3f(1.0, 0.0, 0.0)
                draw_disc(quadricObj, cur.rad, stnagebreite)
                glTranslatef(0.0, breite, 0.0)
                tower_height[i] += breite
                cur = cur.next
        
        glPopMatrix()
        glTranslatef(config.gap, 0.0, 0.0)
    
    glPopMatrix()

    if(curMove != None and curMove.fromTower != -1 and currDisc != None):
        if (pos <= 1.0):

            movY = pos * (config.tower_height - tower_height[int(curMove.fromTower)])

            glTranslatef(config.gap * curMove.fromTower, tower_height[int(curMove.fromTower + movY)], 0.0)
        
        else:
            if(pos < 2.0 and curMove.fromTower != curMove.toTower):
                if(curMove.fromTower != 1 and curMove.toTower != 1):
                    glTranslatef(config.gap, config.tower_height + 0.05, 0.0)
                    
                    if (curMove.fromTower == 0):
                        glRotatef(-(pos - 2.0) * 180 - 90, 0.0, 0.0, 1.0)
                    
                    else:
                        glRotatef((pos - 2.0) * 180 + 90, 0.0, 0.0, 1.0)
                    
                    glTranslatef(0.0, config.gap, 0.0)

                else:

                    if(curMove.fromTower == 0 and curMove.toTower == 1):
                        glTranslatef(config.gap / 2, config.tower_height + 0.05, 0.0)
                        glRotatef(-(pos - 2.0) * 180 - 90, 0.0, 0.0, 1.0)
                    
                    else:
                        if(curMove.fromTower == 2 and curMove.toTower == 1):
                            glTranslatef(config.gap / 2 * 3, config.tower_height + 0.05, 0.0)
                            glRotatef((pos - 2.0) * 180 + 90, 0.0, 0.0, 1.0)
                        else:
                            if (curMove.fromTower == 1 and curMove.toTower == 2):
                                glTranslatef(config.gap / 2 * 3, config.tower_height + 0.05, 0.0)
                                glRotatef(-(pos - 2.0) * 180 - 90, 0.0, 0.0, 1.0)
                            else:
                                glTranslatef(config.gap / 2, config.tower_height + 0.05, 0.0)
                                glRotate((pos - 2.0) * 180 + 90, 0.0, 0.0, 1.0)
                    
                    glTranslatef(0.0, config.gap / 2, 0.0)
                
                glRotatef(-90, 0.0, 0.0, 1.0)
            
            else:
                if(pos >= 2.0):
                    movY = config.tower_height - 2(pos - 2.0 + speed) * (config.tower_height - tower_height[int(curMove.toTower)])
                    glTranslatef(config.gap * curMove.toTower, movY, 0.0)
                
                currDisc.color = glColor3f(0.0, 0.0, 1.0)
                draw_disc(quadricObj, currDisc.rad, stnagebreite)
        
    glutSwapBuffers()

def move_disk(param):

    global curMove, pos, tower, speed, fsem, draw, fem

    if(param == 1):
        return
    
    if (curMove != None):
        if (pos == 0 or pos >= 3 - speed):
            pos = 0
            draw += 1
            add_to_tower(tower[int(curMove.toTower)], currDisc)
            curMove = curMove.next

            if (curMove != None):
                currDisc = rem_from_tower(tower[int(curMove.fromTower)])
        
        pos += speed

        if (pos > 3.0 - fsem):
            pos = 3.0 - fsem
        
        glutTimerFunc(fem, move_disk, 0)
    
    else:
        currDisc = None
        glutTimerFunc(5000, move_disk, 1)
    
    glutPostRedisplay

def timer():

    global curMove, seconds

    if(curMove != None):
        duration += 1
        print(seconds + "Time: %ss" + duration)
    
    glutTimerFunc(1000, timer, 0)


def main():

    hanoi_init()

    glutInit()
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(800, 600)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE)
    glutCreateWindow("Tower of Hanoi Simulation Project")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(int(fem), move_disk, 0)
    glutTimerFunc(1000, timer, 0)
    glutMainLoop()

main()
