from cmu_112_graphics import *
import math, random, copy


class MyApp(App):
    x, y, z = 1, 2, 3
    def appStarted(self):
        self.messages = ['appStarted']
        self.lastx = None
        self.lasty = None
        self.lines = []
        self.lines.append([])    #create a 3D list so that multiple strokes can be made while drawing doodles

    def mouseDragged(self, event):
        self.lastx = event.x
        self.lasty = event.y
        self.lines[-1].append([self.lastx, self.lasty])
        #print(self.lines)
    
    def mouseReleased(self, event):
        self.lines.append([])

    
    def drawLines(self, canvas):
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])-1):
                canvas.create_line(self.lines[i][j], self.lines[i][j+1], width = 3)


    def redrawAll(self, canvas):
        self.drawLines(canvas)
    

MyApp(width = 400, height = 400)