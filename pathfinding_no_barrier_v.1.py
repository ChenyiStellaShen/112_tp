from cmu_112_graphics import *
import random

def appStarted(app):
    app.waitingForFirstKeyPress = True
    reset(app)

def reset(app):
    initApp(app)
    initStart(app)
    initTarget(app)

def initApp(app):
    app.start = None
    app.newStart = []
    app.rows = 10
    app.cols = 10
    app.margin = 0
    app.timerDelay = 250
    app.neighbours = []
    app.gridWidth = app.width - 2*app.margin
    app.gridHeight = app.height - 2*app.margin
    app.cellWidth = (app.width - 2*app.margin) / app.cols
    app.cellHeight = (app.height - 2*app.margin) / app.rows
    app.cellDiagnol = (app.cellWidth**2 + app.cellHeight**2)**0.5
    app.gameOver = False
    
    #app.neighbour = None

def initStart(app):
    if app.start == None:
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        app.start = (row, col)
    initNeighbours(app)
    #newStart(app)
        
def initTarget(app):
    placeTarget(app)


def initNeighbours(app):
    (row, col) = app.start
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if ((drow != 0  or dcol != 0) and
                (0 <= (row+drow) <= app.rows - 1) and
                (0 <= (col+dcol) <= app.cols - 1)):
                neighbour = (row+drow, col+dcol)
                if (neighbour not in app.neighbours) :
                    app.neighbours.append(neighbour)
    return app.neighbours

def initNewNeighbours(app):
    for newStart in app.newStart:
        (row, col) = newStart
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if ((drow != 0  or dcol != 0) and
                    (0 <= (row+drow) <= app.rows - 1) and
                    (0 <= (col+dcol) <= app.cols - 1) and
                    ((row+drow, col+dcol) != app.start)):
                    neighbour = (row+drow, col+dcol)
                    if (neighbour not in app.neighbours):
                        app.neighbours.append(neighbour)
    return app.neighbours
        

def getCellBounds(app, row, col):
    x0 = app.margin + app.gridWidth*col / app.cols
    x1 = app.margin + app.gridWidth*(col + 1) / app.cols
    y0 = app.margin + app.gridHeight * row / app.rows
    y1 = app.margin + app.gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

def drawNeighbours(app, canvas):
    for neighbour in app.neighbours:
        (row, col) = neighbour
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
        drawGAndH(app, canvas, row, col)


def drawGAndH(app, canvas, row, col):
    g = int(dNS(app, row, col))
    h = int(dNT(app, row, col))
    f = g + h
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_text(x0+app.cellWidth/5, y0+app.cellHeight/5, 
                           text = f'{g}', 
                           font = 'Arial 10')
    canvas.create_text(x0+app.cellWidth*4/5, y0+app.cellHeight/5, 
                           text = f'{h}', 
                           font = 'Arial 10')
    canvas.create_text(x0+app.cellWidth/2, y0+app.cellHeight/2, 
                           text = f'{f}', 
                           font = 'Arial 20')



def dNS(app, row, col): #distance between neighbour and target
    (nrow, ncol) = (row, col)
    (srow, scol) = app.start
    #cellDiagnol = (app.cellWidth**2 + app.cellHeight**2)**0.5  #diagnol distance within cell
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

def dNT(app, row, col): #distance between neighbour and target
    (nrow, ncol) = (row, col)
    (trow, tcol) = app.target
    #cellDiagnol = (app.cellWidth**2 + app.cellHeight**2)**0.5  #diagnol distance within cell
    if nrow == trow:
        dNT = app.cellWidth * abs(tcol - ncol)
    elif ncol == tcol:
        dNT = app.cellHeight * abs(trow - nrow)
    elif abs(nrow - trow) == abs(ncol - tcol):
        dNT = app.cellDiagnol * abs(nrow - trow)
    else:
        diagnolStep = min(abs(nrow - trow), abs(ncol - tcol))
        orthoStep = max(abs(nrow - trow), abs(ncol - tcol)) - diagnolStep
        dNT = app.cellDiagnol * diagnolStep + app.cellWidth * orthoStep 
        #this needs to be changed if cellWidth != cellHeight
    return dNT

def newStart(app):
    listOfF = []
    listOfH = []
    listOfIndexMinF = []
    minH = None
    #print(f'neighbours = {app.neighbours}')
    #print(f'length of neighbours = {len(app.neighbours)}')
    for neighbour in app.neighbours:
        (row, col) = neighbour
        g = int(dNS(app, row, col))
        h = int(dNT(app, row, col))
        f = g + h
        listOfF.append(f)
        listOfH.append(h)
    #print(f'listOfF = {listOfF}')
    #print(f'length of listOfF = {len(listOfF)}')
    #print(f'listOfH = {listOfH}')
    #print(f'length of listOfH = {len(listOfH)}')
    minF = min(listOfF)
    #print(f'minF = {minF}')
    #print(f'minF count = {listOfF.count(minF)}')
    if listOfF.count(minF) == 1:
        indexOfMinF = listOfF.index(minF)
        #print(f'indexOfF = {indexOfMinF}')
        newStart = app.neighbours[indexOfMinF]
        app.newStart.append(newStart)
    elif listOfF.count(minF) > 1:
        for i in range(len(listOfF)):
            if listOfF[i] != minF:
                continue
            elif listOfF[i] == minF:
                indexMinF = i
                listOfIndexMinF.append(indexMinF)
        #print(f'listofIndexMinF = {listOfIndexMinF}')
        for num in listOfIndexMinF:
            currH = listOfH[num]
            if minH == None or currH < minH:
                minH = currH
                indexMinH = num
        newStart = app.neighbours[indexMinH]
        #app.newStart.append(newStart)
    
        #print(f'indexMinH = {indexMinH}')
        #newStart = app.neighbours[indexMinH]
        if newStart in app.newStart:
            sortedListOfF = sorted(listOfF)
            minF = sortedListOfF[listOfF.count(minF)]
            if listOfF.count(minF) == 1:
                indexOfMinF = listOfF.index(minF)
                #print(f'indexOfF = {indexOfMinF}')
                newStart = app.neighbours[indexOfMinF]
                app.newStart.append(newStart)
            elif listOfF.count(minF) > 1:
                for i in range(len(listOfF)):
                    if listOfF[i] != minF:
                        continue
                    elif listOfF[i] == minF:
                        indexMinF = i
                        listOfIndexMinF.append(indexMinF)
                #print(f'listofIndexMinF = {listOfIndexMinF}')
                for num in listOfIndexMinF:
                    currH = listOfH[num]
                    if minH == None or currH < minH:
                        minH = currH
                        indexMinH = num
                newStart = app.neighbours[indexMinH]
                app.newStart.append(newStart)
        else:
            app.newStart.append(newStart)
    #print(newStart)
    return app.newStart

def drawNewStart(app, canvas):
    for newStart in app.newStart:
        (row, col) = newStart
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
        drawGAndH(app, canvas, row, col)
    



def keyPressed(app, event):
    if (app.waitingForFirstKeyPress):
        app.waitingForFirstKeyPress = False
    elif event.key == "r":
        reset(app)
    elif app.gameOver:
        return
    elif event.key == "Up":
        takeStep(app)

""" def timerFired(app):
    if app.waitingForFirstKeyPress: return
    takeStep(app) """

def takeStep(app):
    initNewNeighbours(app)
    newStart(app)
    if app.target in app.newStart:
        app.gameOver = True

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

def drawTarget(app, canvas):
    if (app.target != None):
        (row, col) = app.target
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'cyan')

def drawGameOver(app, canvas):
    pass

def redrawAll(app, canvas):
    if (app.waitingForFirstKeyPress):
        canvas.create_text(app.width/2, app.height/2, 
                           text = 'Press any key to start!', 
                           font = 'Arial 26 bold')

    else:
        drawBoard(app, canvas)
        drawNeighbours(app, canvas)
        drawStart(app, canvas)
        drawNewStart(app, canvas)
        drawTarget(app, canvas)
        

runApp(width = 1000, height = 1000)