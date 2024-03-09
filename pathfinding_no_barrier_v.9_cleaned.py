from cmu_112_graphics import *
import random

def appStarted(app):
    app.waitingForFirstKeyPress = True
    reset(app)

def reset(app):
    initApp(app)
    initStart(app)
    initTarget(app)


#########################
# Group 1 - Initializing
#########################
# initializing variables/values
def initApp(app):
    app.start = None
    app.openSet = set()
    app.closedSet = set()
    app.cameFrom = {}
    app.gScore = {}
    app.fScore = {}
    app.rows = 10
    app.cols = 10
    app.margin = 0
    app.timerDelay = 250
    app.gridWidth = app.width - 2*app.margin
    app.gridHeight = app.height - 2*app.margin
    app.cellWidth = (app.width - 2*app.margin) / app.cols
    app.cellHeight = (app.height - 2*app.margin) / app.rows
    app.cellDiagnol = (app.cellWidth**2 + app.cellHeight**2)**0.5
    app.gameOver = False

# place a starting point    
def initStart(app):
    if app.start == None:
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        app.start = (row, col)

# place a target point        
def initTarget(app):
    placeTarget(app)

# find out neighbouring cells of a certain node
def initNeighbour(app, node):
    listOfNeighbours = []
    (row, col) = node
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if ((drow != 0  or dcol != 0) and
                (0 <= (row+drow) <= app.rows - 1) and
                (0 <= (col+dcol) <= app.cols - 1) and
                ((row+drow, col+dcol) != app.start)):
                neighbour = (row+drow, col+dcol)
                if neighbour not in app.closedSet:
                    listOfNeighbours.append(neighbour)
    return listOfNeighbours


#########################
# Group 2 - Pathfinding
#########################
#finding the shortest path from start to target
def pathFinding(app):
    app.openSet.add(app.start)
    app.gScore[app.start] = 0
    app.fScore[app.start] = h(app, app.start[0], app.start[1])
    minF = None
    currentNode = None

    while len(app.openSet) != 0:
        for node in app.openSet:
            (row, col) = node
            if minF == None:
                minF = app.fScore[node]
                currentNode = node 
            elif app.fScore[node] <= minF and node != app.start:
                minF = app.fScore[node]
                currentNode = node
            if currentNode == app.target:
                app.gameOver = True
                return
        app.openSet.remove(currentNode)
        app.closedSet.add(currentNode)
        listOfNeighbours = initNeighbour(app, currentNode)
        for neighbour in listOfNeighbours:
            (row, col) = neighbour
            
            if neighbour not in app.openSet:
                app.openSet.add(neighbour)
            app.gScore[neighbour] = int(dNS(app, row, col))
            tentative_gScore = int(app.gScore[currentNode] + d(app, currentNode, neighbour))
            if tentative_gScore < app.gScore[neighbour]:
                app.cameFrom[neighbour] = currentNode
                app.gScore[neighbour] = tentative_gScore
            app.fScore[neighbour] = app.gScore[neighbour] + h(app, row, col)
    return None

# finding the cheapest path from start to current node
def dNS(app, row, col): 
    (nrow, ncol) = (row, col)
    (srow, scol) = app.start
    if nrow == srow:
        dNS = app.cellWidth * abs(scol - ncol)
    elif ncol == scol:
        dNS = app.cellHeight * abs(srow - nrow)
    elif abs(nrow - srow) == abs(ncol - scol):
        dNS = app.cellDiagnol * abs(nrow - srow)
    else:
        diagnolStep = min(abs(nrow - srow), abs(ncol - scol))
        orthoStep = max(abs(nrow - srow), abs(ncol - scol)) - diagnolStep
        dNS = app.cellDiagnol * diagnolStep + app.cellWidth * orthoStep 
        #this needs to be changed if cellWidth != cellHeight
    return dNS

#calculating h(n) using Manhattan Distance
def h(app, row, col):
    (trow, tcol) = app.target
    return (abs(trow - row) + abs(tcol - col))*app.cellWidth

# d is the weight of edge from current node to its neighbour
def d(app, currentNode, neighbour):
    (crow, ccol) = currentNode
    (nrow, ncol) = neighbour
    if (crow == nrow) or (ccol == ncol):
        return app.cellWidth
    else:
        return app.cellDiagnol


#############################
# Group 3 - Helper Functions
#############################
# helper function to place the target
def placeTarget(app):
    while True:
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        if (row, col) != app.start:
            app.target = (row, col)
            return

#cited from CMU 15112 course website
def getCellBounds(app, row, col):
    x0 = app.margin + app.gridWidth*col / app.cols
    x1 = app.margin + app.gridWidth*(col + 1) / app.cols
    y0 = app.margin + app.gridHeight * row / app.rows
    y1 = app.margin + app.gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

# helper function for finding the shortest path
def takeStep(app):
    pathFinding(app)            


#########################
# Group 4 - Controller
#########################
def keyPressed(app, event):
    if (app.waitingForFirstKeyPress):
        app.waitingForFirstKeyPress = False
    elif event.key == "r":
        reset(app)
    elif app.gameOver:
        return
    elif event.key == "Up":
        takeStep(app)

def timerFired(app):
    if app.gameOver or app.waitingForFirstKeyPress: return
    takeStep(app)


#########################
# Group 5 - Drawing
#########################
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = "white")

def drawStart(app, canvas):
    (row, col) = app.start
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'pink')

def drawTarget(app, canvas):
    if (app.target != None):
        (row, col) = app.target
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'cyan')

def drawOpenSet(app, canvas):
    for node in app.openSet:
        (row, col) = node
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
        drawFGH(app, canvas, row, col)          

def drawClosedSet(app, canvas):
    for node in app.closedSet:
        if node != app.start:
            (row, col) = node
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
            drawFGH(app, canvas, row, col)    

def drawFGH(app, canvas, row, col):
    g = app.gScore[(row, col)]
    f = g + h(app, row, col)
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_text(x0+app.cellWidth/5, y0+app.cellHeight/5, 
                           text = f'{g}', 
                           font = 'Arial 10')
    canvas.create_text(x0+app.cellWidth*4/5, y0+app.cellHeight/5, 
                           text = f'{h(app, row, col)}', 
                           font = 'Arial 10')
    canvas.create_text(x0+app.cellWidth/2, y0+app.cellHeight/2, 
                           text = f'{f}', 
                           font = 'Arial 20')

def drawGameOver(app, canvas):
    pass

def redrawAll(app, canvas):
    if (app.waitingForFirstKeyPress):
        canvas.create_text(app.width/2, app.height/2, 
                           text = 'Press any key to start!', 
                           font = 'Arial 26 bold')

    else:
        drawBoard(app, canvas)
        drawOpenSet(app, canvas)
        drawStart(app, canvas)
        drawClosedSet(app, canvas)
        drawTarget(app, canvas)
        

runApp(width = 1000, height = 1000)