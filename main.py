from sys import argv
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

###################


# Configuration towers
class Config:
    def __init__(self):

        self.gap = 0.0
        self.tower_radius = 0.0
        self.tower_height = 0.0

# A move - relocation of a disk
class Move:

    def __init__(self):

        self.fromTower = 0
        self.toTower = 0
        self.next = Move

# Series of moves stored in a queue like structure    
class Moves:

    def __init__(self):

        self.head = Move
        self.tail = Move

# Disc properties
class Disc:

    def __init__(self):

        self.color = 0
        self.rad = 0.0

        # Disc above and below if any
        self.next = Disc
        self.prev = Disc

# Discs on a tower properties
class Stack:

    def __init__(self):

        self.top = Disc
        self.bottom = Disc

# Simulation Variables
disks = 3 # Total Number of Disks
rotX = 1.5 # Rotation variables - x axis
rotY = 1.5 # Rotation variables - y axis
zoom = 1.5 # Camera Zoom
offsetY = 1.5 # Offset
speed = 0
quadricObj = GLUquadricObj
pos = 0

# Initialize classes

tower1 = Stack()
tower2 = Stack()
tower3 = Stack()

tower = [tower1, tower2, tower3] # Array to store towers
tower_height = [0.0, 0.0, 0.0]

config = Config()
moves = Moves()
curMove = Move() # Current Active Move if any
currDisc = Disc() # Current Active Disc if any

duration = None
seconds = "Time: 0s"
max_moves = None  # To be calculated later
move_count = 0

# Hanoi algoirthm implementation
def hanoi(queue, n, tower1, tower2, tower3):

    curMove = Move() 

    if (n > 0):
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

# Add a disc to a tower
def add_to_tower(tower, disc):

    disc.next = None

    if (tower.bottom == None):
        tower.bottom = disc
        tower.top = disc
        disc.prev = None
    else:
        tower.top.next = disc
        disc.prev = tower.top
        tower.top = disc

# Remove a disc off a tower
def rem_from_tower(tower):

    if (tower.top != None):
        temp = tower.top

        if (tower.top.prev != None) :
            tower.top.prev.next = None
            tower.top = temp.prev

        else:
            tower.bottom = None
            tower.top = None
        
        return temp
    
    return None

# Draw a disk
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

# Draw a tower
def draw_tower(quadric, radius, height):

    global breite, stnagebreite, slices, loops, inner_slices

    glPushMatrix()

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(quadric, radius, radius, (breite / 2), slices, loops)
    gluQuadricOrientation(quadric, GLU_INSIDE)

    gluDisk(quadric, 0.0, radius, slices, loops)
    gluQuadricOrientation(quadric, GLU_OUTSIDE)

    glTranslatef(0.0, 0.0, (breite / 2))
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
    glTranslatef((gap * 2), 0.0, 0.0)
    draw_tower(quadric, radius, height)

    glPopMatrix()

# def drawString(x_pos, y_pos, z_pos, font, msg):

#     glRasterPos3f(x_pos, y_pos, z_pos)

#     for char in msg:
#         glutBitmapCharacter(font, char)

def add_discs_to_tower():

    global duration, move_count, disks

    i = 0

    currentDisc = Disc()

    radius = 0.1 * disks

    for i in range(disks):

        currentDisc.radius = radius
        currentDisc.color = int(i % 6)

        add_to_tower(tower[0], currentDisc)
        radius -= 0.1
    
    duration = 0
    move_count = 0

def clearTowers():

    global currDisc, tower

    currDisc = None

    for i in range(3):

        cur = tower[i].top

        while(cur != None):
            temp = cur.prev
            cur = temp
        
        tower[i].top = None
        tower[i].bottom = None

 # Initialize hanoi simulation       
def hanoi_init():

    global breite, fsem, fem, config, max_moves, moves, curMove, currDisc, pos, speed, disks

    speed = fsem * fem
    radius = 0.1 * disks

    config.tower_radius = radius + 0.1
    config.tower_height = (disks * breite) + 0.2
    config.gap = (radius * 2) + 0.5

    max_moves = (2 ** (disks - 1)) - 1

    add_discs_to_tower()
    moves.head = None

    hanoi(moves, disks, 0, 1, 2)
    curMove = moves.head
    print(curMove.fromTower)
    print(curMove.toTower)
    currDisc = rem_from_tower(tower[int(curMove.fromTower)])
    print(currDisc.rad)
    pos = 0.001
    
def reset():

    global moves, curMove, currDisc, tower, pos

    clearTowers()
    add_discs_to_tower()

    curMove = moves.head
    currDisc = rem_from_tower(tower[int(curMove.fromTower)])
    pos = 0.001

def reset_hanoi():
    global moves, quadricObj

    clearTowers()
    movCur = moves.head

    while True:
        movTmp = movCur.next
        movCur = movTmp

        if movCur == None:
            break
    
    gluDeleteQuadric(quadricObj)


def pick_colors(color):

    if ((color) == 0):
        return glColor3f(1.0, 0.0, 0.0)
    elif ((color) == 1):
        return glColor3f(0.0, 1.0, 0.0)
    elif ((color) == 2):
        return glColor3f(1.0, 1.0, 0.0)
    elif ((color) == 3):
        return glColor3f(0.0, 1.0, 1.0)
    elif ((color) == 4):
        return glColor3f(1.0, 0.0, 1.0)
    elif ((color) == 5):
        return glColor3f(0.0, 0.0, 0.0)
        
# Initialize GLUT Setups
def init():

    global quadricObj

    mat_specular = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
    mat_shininess = np.array([50.0], dtype=np.float32)
    light_position = np.array([0.0, 1.0, 1.0, 0.0], dtype=np.float32)

    glShadeModel(GL_SMOOTH)

    # Polygons are filled with color
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Screen Color = white
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Blender Settings
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Remove backsides
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

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0.0, 0.0, 0.0)

    # Camera view point
    gluLookAt(0.0, 0.9, (3.6 + zoom), 0.0, offsetY, 0.0, 0.0, 1.0, 0.0)

    glRotatef(rotY, 0.0, 1.0, 0.0) # y axis rotation
    glRotatef(rotX, 0.0, 1.0, 0.0) # x axis rotation
    glColor3f(0.0, 0.0, 0.5)

    draw_all_towers(quadricObj, config.tower_radius, config.tower_height, config.gap)
    glTranslatef(-config.gap, (breite / 2), 0.0)

    glPushMatrix()

    for i in range(3):

        glPushMatrix()
        tower_height[i] = 0

        currentDisc = tower[i].bottom

        if (currentDisc.rad != None):

            while True:
                pick_colors(currentDisc.color)
                draw_disc(quadricObj, currentDisc.rad, stnagebreite)
                glTranslatef(0.0, breite, 0.0)
                tower_height[i] += breite
                currentDisc = currentDisc.next

                if (currentDisc.rad == None):
                    break

        glPopMatrix()
        glTranslatef(config.gap, 0.0, 0.0)     
    glPopMatrix()
    
    if((curMove.fromTower != None or curMove.toTower != None) and curMove.fromTower != -1 and currDisc.rad != None):
        if (pos <= 1.0):

            movY = pos * (config.tower_height - (tower_height[int(curMove.fromTower)]))

            glTranslatef((config.gap * curMove.fromTower), tower_height[int(curMove.fromTower)] + movY, 0.0)
        
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
                    movY = config.tower_height - (pos - 2.0 + speed) * (config.tower_height - tower_height[int(curMove.toTower)])
                    glTranslatef((config.gap * curMove.toTower), movY, 0.0)
                
        pick_colors(currDisc.color)
        draw_disc(quadricObj, currDisc.rad, stnagebreite)
        
    glutSwapBuffers()

def move_disk(param):

    global curMove, pos, tower, speed, fsem, move_count, fem, currDisc

    if(param == 1):
        reset()
    
    if (curMove.fromTower != None and curMove.toTower != None):
        if (pos == 0 or (pos >= (3 - speed))):
            pos = 0
            move_count += 1
            add_to_tower(tower[int(curMove.toTower)], currDisc)
            curMove = curMove.next

            if (curMove.fromTower != None and curMove.toTower != None):
                currDisc = rem_from_tower(tower[int(curMove.fromTower)])
        
        pos += speed

        if (pos > 3.0 - fsem):
            pos = 3.0 - fsem
        
        glutTimerFunc(int(fem), move_disk, 0)
    
    else:
        currDisc.rad = None
        glutTimerFunc(5000, move_disk, 1)
    
    glutPostRedisplay

def timer(param):

    global curMove, seconds, duration

    if(curMove != None):
        duration += 1
        print("Time: %ss" %{str(duration)})
    
    glutTimerFunc(1000, timer, 0)

def main():

    hanoi_init()

    glutInit(sys.argv)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(800, 600)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE)
    glutCreateWindow("Tower of Hanoi Puzzle Simulation")

    init()
    glutDisplayFunc(display)
    glutTimerFunc(int(fem), move_disk, 0)
    glutTimerFunc(1000, timer, 0)
    glutMainLoop()

main()
