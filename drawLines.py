import math, copy, random
import tkinter as tk
########################################################################
# line drawing tutorial: 
# https://pythonprogramming.altervista.org/draw-in-tkinters-canvas/
######################################################################
lines = []
def xy(event):
	global lastx,lasty
	lastx,lasty=event.x,event.y
	lines.append([])
def addLine(event):
	global lastx,lasty
	canvas.create_line((lastx,lasty,event.x,event.y))
	lastx,lasty=event.x,event.y
	lines[-1].append([lastx,lasty])
root = tk.Tk()
root.geometry("800x600")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
canvas = tk.Canvas(root)
canvas.grid(column=0,row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
canvas.bind("<Button-1>",xy)
canvas.bind("<B1-Motion>",addLine)
root.mainloop()
y0 = 0
x0 = 0
for line in lines:
	for (x,y) in line:
		if y > y0:
			y0 = y
			x0 = x
for i in range(len(lines)):
	for j in range(len(lines[i])):
		lines[i][j][0] -= x0
		lines[i][j][1] -= y0
print(lines)
root2 = tk.Tk()
root2.geometry("800x600")
root2.columnconfigure(0,weight=1)
root2.rowconfigure(0,weight=1)
canvas2 = tk.Canvas(root2)
canvas2.grid(column=0,row=0,sticky=(tk.N,tk.W,tk.E,tk.S))
dx = 0
dy = 0
terrain = []
for i in range(0,10):
	terrain.append((i/9*800,600-random.random()*200))
def drawTerrain():
	for i in range(len(terrain)-1):
		canvas2.create_line((terrain[i][0],terrain[i][1],terrain[i+1][0],terrain[i+1][1]))

def calcY(x):
	for i in range(len(terrain)-2,-1,-1):
		if x > terrain[i][0]:
			j = i+1
			t = (x-terrain[i][0])/(terrain[j][0]-terrain[i][0])
			return terrain[i][1]*(1-t)+terrain[j][1]*t
	return 0
def animation():
	global dx,dy
	dx += 1
	dy = calcY(dx)
	canvas2.delete("all")
	drawTerrain()
	for line in lines:
		for i in range(len(line)-1):
			canvas2.create_line((line[i][0]+dx,line[i][1]+dy,line[i+1][0]+dx,line[i+1][1]+dy))
	drawTerrain()
	for line in lines:
		for i in range(len(line)-2):
			canvas2.create_line((line[i][0]+dx,line[i][1]+dy,line[i+1][0]+dx,line[i+1][1]+dy))
	root2.after(10,animation)
animation()
root2.mainloop()