from cmu_112_graphics import *
import random
import math

def appStarted(app):
    app.waitingForFirstKeyPress = True
    reset(app)

def reset(app):
    initApp(app)
    initStart(app)
    initTarget(app)
    initBarriers(app)
    initMap(app)
    # castRay(app)


#########################
# Group 1 - Initializing
#########################
# initializing variables/values
def initApp(app):
    app.start = None
    app.target = None
    app.openSet = set()
    app.closedSet = set()
    # app.cameFrom = {}
    app.gScore = {}
    app.fScore = {}
    app.rows = 10
    app.cols = 10
    app.barriers = []
    app.total_path = []
    app.margin = 5
    app.timerDelay = 250
    app.gridWidth = app.width - 2*app.margin
    app.gridHeight = app.height - 2*app.margin
    app.cellWidth = (app.width - 2*app.margin) / app.cols
    app.cellHeight = (app.height - 2*app.margin) / app.rows
    app.cellDiagnol = (app.cellWidth**2 + app.cellHeight**2)**0.5
    app.maxNeighbour = None
    app.gameOver = False
    app.map = None
    app.dirX = -1
    app.dirY = 0
    app.pX = None
    app.pY = None
    app.pA = 2*math.pi
    app.rA = 0
    app.pdX = math.cos(app.pA) * 5
    app.pdY = math.sin(app.pA) * 5
    app.rY = None
    app.rX = None
    app.xO = None
    app.yO = None
    

def initStart(app):
    if app.start == None:
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        app.start = (row, col)
        # app.map[row][col] = 1
        # print(app.map)

def initTarget(app):
    placeTarget(app)
    (x0, y0, x1, y1) = getCellBounds(app, app.target[0], app.target[1])
    app.pX = (x0 + x1)/2
    app.pY = (y0 + y1)/2
    # castRay(app)


def initBarriers(app):
    while True:
        listOfRows = list(range(app.rows))
        listOfCols = list(range(app.cols))
        rows = random.sample(listOfRows, 3)
        cols = random.sample(listOfCols, 3)
        for i in range(len(rows)):
            (row, col) = (rows[i], cols[i])
            barrier1 = (row, col)
            barrierList = [barrier1]
            if (row+1) < (app.rows-1):
                barrier2 = (row+1, col)
                barrierList = [barrier1, barrier2]
                if (col+1) < (app.cols-1):
                    barrier3 = (row+1, col+1)
                    barrierList = [barrier1, barrier2, barrier3]
            # barrierList = [barrier1, barrier2, barrier3]
            if ((app.start not in barrierList) and 
               (app.target not in barrierList)):
                app.barriers += barrierList
        return

def initMap(app):
    app.map = [[0]*app.cols for row in range(app.rows)]
    (row, col) = app.start
    # print(row, col)
    for barrier in app.barriers:
        
        (row, col) = barrier
        # print(row, col)
        app.map[row][col] = 1
    # print(app.barriers)
    # print(app.map)

def keyPressed(app, event):
    if event.key == "a":
        rotatePlayerLeft(app)
    if event.key == "d":
        rotatePlayerRight(app)
    if event.key == "w":
        movePlayerForward(app)
    if event.key == "s":
        movePlayerBackward(app)


def castRay(app):
    # app.rY = None
    # app.rX = None
    print("1")
    trial = 0
    if app.pA == 2*math.pi:
        app.rA = 0
    else:
    
        app.rA = app.pA
        print(f'{app.rA}')
        #Looking Up
        if app.rA < math.pi:
            closestRow = int(app.pY/app.cellWidth) - 1
            app.rY = getCellBounds(app, closestRow, 0)[3]
            app.rX = (app.pY-app.rY)/math.tan(app.rA) + app.pX
            print(f'1tanA = {math.tan(app.rA)}, rA = {app.rA}, pY-rY = {app.pY-app.rY}')
            print(f'1app.rx , app.rY = {app.rX} {app.rY}')
            app.yO = -app.cellWidth
            app.xO = -app.yO/math.tan(app.rA)
            return
        #Looking Down
        elif app.rA > math.pi:
            closestRow = int(app.pY/app.cellWidth)
            app.rY = getCellBounds(app, closestRow, 0)[3]
            app.rX = (app.pY-app.rY)/math.tan(app.rA) + app.pX
            print(f'2tanA = {math.tan(app.rA)}, rA = {app.rA}, pY-rY = {app.pY-app.rY}')
            print(f'2app.rx , app.rY = {app.rX} {app.rY}')
            app.yO = app.cellWidth
            app.xO = -app.yO/math.tan(app.rA)
            return
        elif app.rA == 0 or app.rA == math.pi:
            app.rX, app.rY = app.pX, app.pY
            print(f'3tanA = {math.tan(app.rA)}, rA = {app.rA}, pY-rY = {app.pY-app.rY}')
            print(f'3app.rx , app.rY = {app.rX} {app.rY}')
            return
        
           

def temp(app):
    if app.rX != None and app.rY != None:
        trial = 0
        while trial < app.rows:
            rayRow = int(app.rX/app.cellWidth)
            rayCol = int(app.rY/app.cellWidth)
            rayMap = rayCol*app.rows + rayRow
            print(f'rayRow, rayCol = {rayRow},{rayCol}')
            
            if ((0 <= rayRow <= app.rows - 1) and (0 <= rayCol <= app.cols - 1) 
                and app.map[rayRow][rayCol] == 1):
                print(f'{app.map[rayRow][rayCol]}')
                trial = app.rows
            
            else:
                print("18")
      
                app.rX += app.xO
                app.rY += app.yO
                print(f'xO, yO = {app.xO, app.yO}')
                trial += 1
                print(f'trial = {trial}')
    else:
            return
    
   
     






    
def rotatePlayerLeft(app):
    castRay(app)
    temp(app)
    app.pA -= 0.1
    if app.pA < 0:
        app.pA += 2*math.pi
    app.pdX = math.cos(app.pA) * 5
    app.pdY = math.sin(app.pA) * 5
    

def rotatePlayerRight(app):
    castRay(app)
    temp(app)
    app.pA += 0.1
    if app.pA > 2*math.pi:
        app.pA += 2*math.pi
    app.pdX = math.cos(app.pA) * 5
    app.pdY = math.sin(app.pA) * 5
    

def movePlayerForward(app):
    castRay(app)
    app.pX += app.pdX
    app.pY += app.pdY
  
def movePlayerBackward(app):
    castRay(app)
    app.pX -= app.pdX
    app.pY -= app.pdY
    


def drawVisionLine(app, canvas):
    vertex1 = (app.pX, app.pY)
    vertex2 = (app.pX+app.pdX*5, app.pY+app.pdY*5)
    canvas.create_line(vertex1, vertex2, fill = "red")

def drawRay(app, canvas):
    vertex1 = (app.pX, app.pY)
    # print(app.pX, app.pY)
    vertex2 = (app.rX, app.rY)
    # print(app.rX, app.rY)
    canvas.create_line(vertex1, vertex2, fill = "red")
    # print("drawray")


""" def timerFired(app):
    castRay(app) """

def ray(app):
    pass



def getCellBounds(app, row, col):
    x0 = app.margin + app.gridWidth*col / app.cols
    x1 = app.margin + app.gridWidth*(col + 1) / app.cols
    y0 = app.margin + app.gridHeight * row / app.rows
    y1 = app.margin + app.gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.row

def placeTarget(app):
    while True:
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        if (row, col) != app.start:
            app.target = (row, col)
            return


def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = "white")

def drawStart(app, canvas):
    (row, col) = app.start
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'pink')

def drawBarriers(app, canvas):
    for barrier in app.barriers:
        (row, col) = barrier
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'dark grey')

def drawTarget(app, canvas):
    if (app.target != None):
        (row, col) = app.target
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'black')

def drawRayCenter(app, canvas):
    cx, cy = app.pX, app.pY
    r = 5
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = "white")

def redrawAll(app, canvas):
    
    drawBoard(app, canvas)
    drawStart(app, canvas)
    # drawTarget(app, canvas)
    drawBarriers(app, canvas)
    drawRayCenter(app, canvas)
    # drawVisionLine(app, canvas)
    if app.rX != None and app.rY != None:
        drawRay(app, canvas)
    # print(f'app.pX, app.pY = {app.pX}, {app.pY}')
    # print(f'app.cellWidth = {app.cellWidth}')
        
runApp(width = 1000, height = 1000)