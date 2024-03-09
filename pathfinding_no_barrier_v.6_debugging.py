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
    app.openSet = set()
    app.closedSet = set()
    app.cameFrom = {}
    app.gScore = {}
    app.fScore = {}
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
    
def initStart(app):
    if app.start == None:
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        app.start = (row, col)
        
def initTarget(app):
    placeTarget(app)

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

#calculating h(n) using Manhattan Distance
def h(app, row, col):
    (trow, tcol) = app.target
    return (abs(trow - row) + abs(tcol - col))*app.cellWidth

def drawFGH(app, canvas, row, col):
    g = app.gScore[(row, col)]
    #h = h(app, row, col)
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

def drawNeighbours(app, canvas):
    for node in app.openSet:
        (row, col) = node
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
        drawFGH(app, canvas, row, col)


def dNS(app, row, col): #cheapest path from start to current node
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


def pathFinding(app):
    app.openSet.add(app.start)
    app.gScore[app.start] = 0
    app.fScore[app.start] = h(app, app.start[0], app.start[1])
    minF = None
    currentNode = None

    while len(app.openSet) != 0:
        #print(f'open Set1 = {app.openSet}')
        for node in app.openSet:
            print(f'node = {node}')
            (row, col) = node
            # app.gScore[node] = dNS(app, row, col)
            # app.fScore[node] = app.gScore[node] + h(app, row, col)
            print(f'gscore = {app.gScore[node]}')
            print(f'hscore = {h(app, row, col)}')
            print(f'fscore = {app.fScore[node]}')
            if ((minF == None or 
                minF ==  app.fScore[app.start] or
                app.fScore[node] <= minF) and currentNode != app.target):
                minF = app.fScore[node]
                currentNode = node 
        if currentNode == app.target:
            app.gameOver = True
            return
        print(f'minF = {minF}')
        print(f'current Node = {currentNode}')
        app.openSet.remove(currentNode)
        app.closedSet.add(currentNode)
        listOfNeighbours = initNeighbour(app, currentNode)
        print(f'list of Neighbours = {listOfNeighbours}')
        for neighbour in listOfNeighbours:
            # print(f'neighbour = {neighbour}')
            (row, col) = neighbour
            
            if neighbour not in app.openSet:
                app.openSet.add(neighbour)
                print(f'openSet2 = {app.openSet}')
            app.gScore[neighbour] = int(dNS(app, row, col))
            # print(f'gScore = {app.gScore[neighbour]}')
            tentative_gScore = int(app.gScore[currentNode] + d(app, currentNode, neighbour))
            # print(f'tentative gScore = {tentative_gScore}')
            if tentative_gScore < app.gScore[neighbour]:
                app.cameFrom[neighbour] = currentNode
                app.gScore[neighbour] = tentative_gScore
            app.fScore[neighbour] = app.gScore[neighbour] + h(app, row, col)
            print (f'neighbour = {neighbour}, gScore = {app.gScore[neighbour]}, fScore = {app.fScore[neighbour]} ')  
        print(f'cameFrom = {app.cameFrom}')        
    return 1

def d(app, currentNode, neighbour):
    (crow, ccol) = currentNode
    (nrow, ncol) = neighbour
    if (crow == nrow) or (ccol == ncol):
        return app.cellWidth
    else:
        return app.cellDiagnol
    """ (crow, ccol) = currentNode
    (nrow, ncol) = neighbour
    if crow == nrow or ccol ==ncol:
        return app.cellWidth
    else:
        return app.cellDiagnol """







""" def newStart(app):
    listOfF = []
    listOfH = []
    listOfIndexMinF = []
    listOfCurrH = []
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
                    listOfCurrH.append(currH)
                    print(f'listOfCurrH = {listOfCurrH}')
                    if minH == None or currH < minH:
                        minH = currH
                        indexMinH = num
                newStart = app.neighbours[indexMinH]
                app.newStart.append(newStart)
        else:
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
            listOfCurrH.append(currH)
            print(f'listOfCurrH = {listOfCurrH}')
            if minH == None or currH < minH:
                minH = currH
                indexMinH = num
        newStart = app.neighbours[indexMinH]
        #app.newStart.append(newStart)
    
        #print(f'indexMinH = {indexMinH}')
        #newStart = app.neighbours[indexMinH]
        if newStart in app.newStart:
            sortedListOfCurrH = sorted(listOfCurrH)
            minH = sortedListOfCurrH[listOfCurrH.count(minH)]
            #print(f'sortedListOfCurrH = {sortedListOfCurrH}')
            #print(f'minH = {minH}')
            # sortedListOfF = sorted(listOfF)
            # minF = sortedListOfF[listOfF.count(minF)]
            indexMinH = listOfH.index(minH)
            newStart = app.neighbours[indexMinH]
            app.newStart.append(newStart)
        else:
            app.newStart.append(newStart)
    #print(newStart)
    return app.newStart """

def drawNewStart(app, canvas):
    for node in app.closedSet:
        if node != app.start:
            (row, col) = node
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
            drawFGH(app, canvas, row, col)
    



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
    if app.gameOver or app.waitingForFirstKeyPress: return
    takeStep(app) """

def takeStep(app):
    pathFinding(app)
    print(f'openSet = {app.openSet}')
    print(f'closeSet = {app.closedSet}')
    # if app.target in app.newStart:
        # app.gameOver = True

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