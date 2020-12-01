from cmu_112_graphics import *
import random
# framework cited from CMU 15112 coure website

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        titleFont = 'Arial 36 bold'
        instructionFont = 'Arial 15'
        canvas.create_text(mode.width/2, mode.height/3, text='Doodle Fantasy', 
                           font='Arial 36 bold')
        canvas.create_text(mode.width/2, mode.height*1/2, text='Welcome!', 
                           font='Arial 26 bold')
        
        canvas.create_text(mode.width/2, mode.height*2/3, 
                           text='Press any key to continue!', 
                           font=instructionFont)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.drawMode)

class DrawMode(Mode):
    def appStarted(mode):
        mode.waitingForFirstKeyPress = True
        mode.lastx = None
        mode.lasty = None
        mode.lines = []
        mode.lines.append([])    #create a 3D list so that multiple strokes 
                                 #can be made while drawing doodles


    def mouseDragged(mode, event):
        if not (mode.waitingForFirstKeyPress):
            mode.lastx = event.x
            mode.lasty = event.y
            mode.lines[-1].append([mode.lastx, mode.lasty])
            #print(mode.lines)
    
    def mouseReleased(mode, event):
        if not (mode.waitingForFirstKeyPress):
            mode.lines.append([])

    
    def drawLines(mode, canvas):
        for i in range(len(mode.lines)):
            for j in range(len(mode.lines[i])-1):
                canvas.create_line(mode.lines[i][j], 
                                   mode.lines[i][j+1], width = 3)
    
    def keyPressed(mode, event):
        if (mode.waitingForFirstKeyPress):
            mode.waitingForFirstKeyPress = False
        if (event.key == "g"):
            mode.app.setActiveMode(mode.app.gameMode)


    def redrawAll(mode, canvas):
        if (mode.waitingForFirstKeyPress):
            canvas.create_text(mode.width/2, mode.height/3, 
                            text = 'Draw some DOODLES!', 
                            font = 'Arial 26 bold')
            canvas.create_text(mode.width/2, mode.height*7/18, 
                            text = 'Simply using your mouse!', 
                            font = 'Arial 15 ')
            canvas.create_text(mode.width/2, mode.height*2/3, 
                            text = 'Press any key to continue!', 
                            font = 'Arial 15')
            canvas.create_text(mode.width/2, mode.height*3/4, 
                               text='Press "g" to drop your doodle into the fantasy world.', 
                               font='Arial 15')
            canvas.create_text(mode.width/2, mode.height*4/5, 
                               text='Press "r" to reset the world.', 
                               font='Arial 15')
        else:
            mode.drawLines(canvas)

class GameMode(Mode):
    def appStarted(mode):
        mode.waitingForFirstKeyPress = False
        mode.reset()

    def reset(mode):
        mode.initApp()
        mode.initStart()
        mode.initTarget()   

    def initApp(mode):
        mode.start = None
        mode.openSet = set()
        mode.closedSet = set()
        mode.cameFrom = {}
        mode.gScore = {}
        mode.fScore = {}
        mode.rows = 10
        mode.cols = 10
        mode.margin = 0
        mode.timerDelay = 250
        mode.gridWidth = mode.width - 2*mode.margin
        mode.gridHeight = mode.height - 2*mode.margin
        mode.cellWidth = (mode.width - 2*mode.margin) / mode.cols
        mode.cellHeight = (mode.height - 2*mode.margin) / mode.rows
        mode.cellDiagnol = (mode.cellWidth**2 + mode.cellHeight**2)**0.5
        mode.gameOver = False 

    def initStart(mode):
        if mode.start == None:
            row = random.randint(0, mode.rows - 1)
            col = random.randint(0, mode.cols - 1)
            mode.start = (row, col)

    def initTarget(mode):
        mode.placeTarget()

    def initNeighbour(mode, node):
        listOfNeighbours = []
        (row, col) = node
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if ((drow != 0  or dcol != 0) and
                    (0 <= (row+drow) <= mode.rows - 1) and
                    (0 <= (col+dcol) <= mode.cols - 1) and
                    ((row+drow, col+dcol) != mode.start)):
                    neighbour = (row+drow, col+dcol)
                    if neighbour not in mode.closedSet:
                        listOfNeighbours.append(neighbour)
        return listOfNeighbours

    def pathFinding(mode):
        mode.openSet.add(mode.start)
        mode.gScore[mode.start] = 0
        mode.fScore[mode.start] = mode.h(mode.start[0], mode.start[1])
        minF = None
        currentNode = None

        while len(mode.openSet) != 0:
            for node in mode.openSet:
                (row, col) = node
                if minF == None:
                    minF = mode.fScore[node]
                    currentNode = node 
                elif mode.fScore[node] <= minF and node != mode.start:
                    minF = mode.fScore[node]
                    currentNode = node
                if currentNode == mode.target:
                    mode.gameOver = True
                    return
            mode.openSet.remove(currentNode)
            mode.closedSet.add(currentNode)
            listOfNeighbours = mode.initNeighbour(currentNode)
            for neighbour in listOfNeighbours:
                (row, col) = neighbour
                
                if neighbour not in mode.openSet:
                    mode.openSet.add(neighbour)
                mode.gScore[neighbour] = int(mode.dNS(row, col))
                tentative_gScore = int(mode.gScore[currentNode] + mode.d(currentNode, neighbour))
                if tentative_gScore < mode.gScore[neighbour]:
                    mode.cameFrom[neighbour] = currentNode
                    mode.gScore[neighbour] = tentative_gScore
                mode.fScore[neighbour] = mode.gScore[neighbour] + mode.h(row, col)
        return None


    def dNS(mode, row, col): 
        (nrow, ncol) = (row, col)
        (srow, scol) = mode.start
        if nrow == srow:
            dNS = mode.cellWidth * abs(scol - ncol)
        elif ncol == scol:
            dNS = mode.cellHeight * abs(srow - nrow)
        elif abs(nrow - srow) == abs(ncol - scol):
            dNS = mode.cellDiagnol * abs(nrow - srow)
        else:
            diagnolStep = min(abs(nrow - srow), abs(ncol - scol))
            orthoStep = max(abs(nrow - srow), abs(ncol - scol)) - diagnolStep
            dNS = mode.cellDiagnol * diagnolStep + mode.cellWidth * orthoStep 
            #this needs to be changed if cellWidth != cellHeight
        return dNS

    def h(mode, row, col):
        (trow, tcol) = mode.target
        return (abs(trow - row) + abs(tcol - col))*mode.cellWidth

    def d(mode, currentNode, neighbour):
        (crow, ccol) = currentNode
        (nrow, ncol) = neighbour
        if (crow == nrow) or (ccol == ncol):
            return mode.cellWidth
        else:
            return mode.cellDiagnol

    def placeTarget(mode):
        while True:
            row = random.randint(0, mode.rows - 1)
            col = random.randint(0, mode.cols - 1)
            if (row, col) != mode.start:
                mode.target = (row, col)
                return

    def getCellBounds(mode, row, col):
        x0 = mode.margin + mode.gridWidth*col / mode.cols
        x1 = mode.margin + mode.gridWidth*(col + 1) / mode.cols
        y0 = mode.margin + mode.gridHeight * row / mode.rows
        y1 = mode.margin + mode.gridHeight * (row + 1) / mode.rows
        return (x0, y0, x1, y1)

    def takeStep(mode):
        mode.pathFinding()   

    def keyPressed(mode, event):
        if (mode.waitingForFirstKeyPress):
            mode.waitingForFirstKeyPress = False
        elif event.key == "r":
            mode.reset()
        elif event.key == "h":
            mode.app.setActiveMode(mode.app.helpMode)
        elif mode.gameOver:
            return
        elif event.key == "Up":
            mode.takeStep()


    def timerFired(mode):
        if mode.gameOver or mode.waitingForFirstKeyPress: return
        mode.takeStep()

    def drawBoard(mode, canvas):
        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = "white")

    def drawStart(mode, canvas):
        (row, col) = mode.start
        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'pink')

    def drawTarget(mode, canvas):
        if (mode.target != None):
            (row, col) = mode.target
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'cyan')

    def drawOpenSet(mode, canvas):
        for node in mode.openSet:
            (row, col) = node
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
            mode.drawFGH(canvas, row, col) 

    def drawClosedSet(mode, canvas):
        for node in mode.closedSet:
            if node != mode.start:
                (row, col) = node
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
                mode.drawFGH(canvas, row, col) 

    def drawFGH(mode, canvas, row, col):
        g = mode.gScore[(row, col)]
        f = g + mode.h(row, col)
        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
        canvas.create_text(x0+mode.cellWidth/5, y0+mode.cellHeight/5, 
                            text = f'{g}', 
                            font = 'Arial 10')
        canvas.create_text(x0+mode.cellWidth*4/5, y0+mode.cellHeight/5, 
                            text = f'{mode.h(row, col)}', 
                            font = 'Arial 10')
        canvas.create_text(x0+mode.cellWidth/2, y0+mode.cellHeight/2, 
                            text = f'{f}', 
                            font = 'Arial 20')

    def redrawAll(mode, canvas):
        if (mode.waitingForFirstKeyPress):
            canvas.create_text(mode.width/2, mode.height/2, 
                            text = 'Press any key to start!', 
                            font = 'Arial 26 bold')

        else:
            mode.drawBoard(canvas)
            mode.drawOpenSet(canvas)
            mode.drawStart(canvas)
            mode.drawClosedSet(canvas)
            mode.drawTarget(canvas)


class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(mode.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.drawMode = DrawMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=1000, height=1000)