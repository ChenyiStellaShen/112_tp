from tkinter import *
#import random

def init(data):
    data.scrollX = 0
    data.scrollMargin = 50
    data.playerX = data.scrollMargin
    data.playerY = 0
    data.playerWidth = 10
    data.playerHeight = 20
    data.doodles = 5
    data.doodlePoints = [0] * data.doodles
    data.doodleWidth = 20
    data.doodleHeight = 40
    data.doodleSpacing = 90
    data.currentDoddleCollect = -1


def getPlayerBounds(data):
    (x0, y1) = (data.playerX, data.heigh/2 - data.playerY)
    (x1, y0) = (x0 + data.playerWidth, y1 - data.palyerHeight)
    return (x0, y0, x1, y1)

def getDoodleBounds(doodle, data):
    (x0, y1) = ((1 + doodle) * data.doodleSpacing, data.height/2)
    (x1, y0) = (x0 + data.doodleWidth, y1 - data.doodleHeight)
    return (x0, y0, x1, y1)

def getDoodleCollect(data):
    playerBounds = getPlayerBounds(data)
    for doodle in range(data.doodles):
        doodleBounds = getDoodleBounds(doodle, data)
        if (boundsIntersect(playerBounds, doodleBounds) == True):
            return doodle
    return -1


def boundsIntersect(boundsA, boundsB):
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def movePlayer(dx, dy, data):
    data.playerX += dx
    data.playerY += dy
    if (data.playerX < data.scrollX + data.scrollMargin):
        data.scrollX = data.playerX - data.scrollMargin
    if (data.playerX > data.scrollX + data.width - data.scrollMargin):
        data.scrollX = data.playerX - data.width + data.scrollMargin

    doodle = getDoodleCollect(data)
    if (doodle != data.curentDoodleCollect):
        data.currentDoodleCollect = doodle
        if (doodle >= 0):
            data.doodlePoints[doodle] += 1

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if (event.keysym == "Left"): movePlayer(-5, 0, data)
    elif (event.keysym == "Right"): movePlayer(+5, 0, data)
    elif (event.keysym == "Up"): movePlayer(0, +5, data)
    elif (event.keysym == "Down"): movePlayer(0, -5, data)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    lineY = data.height/2
    lineHeight = 5
    canvas.create_rectangle(0, lineY, data.width, 
                            lineY + lineHeight, fill = "black")

    sx = data.scrollX
    for doodle in range(data.doodles):
        (x0, y0, x1, y1) = getDoodleBounds(doodle, data)
        fill = "orange" if (doodle == data.currentDoodleCollect) else "pink"
        canvas.create_rectangle(x0 - sx, y0, x1 - sx, y1, fill = fill)
        (cx, cy) = ((x0+x1)/2 - sx, (y0+y1)/2)
        canvas.create_text(cs, cy, text = str(data.doodlePoints[doodle]))
        cy = lineY + 5
        canvas.create_text(cx, cy, text = str(doodle), anchor = N)
    
    (x0, y0, x1, y1) = getPlayerBounds(data)
    canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill = "grey")

    msg = "Use arrows to move, collect doodls to score"
    canvas.create_text(data.width/2, 20, text = msg)

####################################
# use the run function as-is
####################################

def run(width = 400, height = 400):
    def redrawAllWrapper(canvs, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill = 'tan', width = 0)
        redrawAll(canvas, data)
        canvas.update()

        def mousePressedWrapper(event, canvas, data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)

        def keyPressedWrapper(event, canvas, data):
            keyPressed(event, data)
            redrawAllWrapper(canvs, data)

        def timerFiredWrapper(event, canvas, data):
            timerFiredWrapper(event, data)
            redrawAllWrapper(canvs, data)

            canvas.after(data,timerDelay, timerFiredWrapper, canvas, data)
        
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 100
        init(data)

        root = Tk()
        canvas = Canvas(root, width = data.width, height = data.height)
        canvas.pack()

        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)

        root.mainloop()
        print("bye!")

run(400, 400)
        


