from graphics import *
from random import randint
from Queue import *
import time

width = 400
height = 400
cols = 25
rows = 25
w = width/cols
h = height/rows
window = GraphWin("Pathfinding Example", width, height)

grid = []
openSet = []
closedSet = []

start = None
end = None
path = []

class Spot(object):
	
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.colour = 'white'
		self.f = 0
		self.g = 0
		self.h = 0
		self.neighbours = []
		self.previous = None
		self.wall = False
		
		wallChance = randint(1,10)
		if wallChance <= 2:
			self.wall = True
		
	def show(self):
		p1 = Point(self.i * w, self.j * h)
		p2 = Point(self.i * w + w - 1, self.j * h + h - 1)
		rect = Rectangle(p1,p2)
		if self.wall == False:
			rect.setFill(self.colour)
		else:
			rect.setFill('black')
		rect.draw(window)

	def addNeighbours(self):
		i = self.i
		j = self.j
		if i < cols - 1:
			self.neighbours.append(grid[i + 1][j])
		if i > 0:
			self.neighbours.append(grid[i - 1][j])
		if j < rows - 1:
			self.neighbours.append(grid[i][j + 1])
		if j > 0:
			self.neighbours.append(grid[i][j - 1])
		
		
def setup():

	global end

	# make a 2D array of Spot objects
	for i in range(0, cols):
		row = []
		for j in range(0, rows):
			new_spot = Spot(i, j)
			row.append(new_spot)
		grid.append(row)
		
	# add neighbours for each Spot object
	for i in range(0, cols):
		for j in range(0, rows):
			grid[i][j].addNeighbours()
		
	# start from the top left, end in the bottom right
	start = grid[0][0]
	end = grid[cols - 1][rows - 1]
	
	start.wall = False
	end.wall = False
		
	openSet.append(start)
	
	# openSet is green, closedSet is red, neither is white
	for i in range(0, cols):
		for j in range(0, rows):
			if grid[i][j] in openSet:
				grid[i][j].colour = 'green'
			elif grid[i][j] in closedSet:
				grid[i][j].colour = 'red'
			else:
				if grid[i][j].wall == True:
					grid[i][j].colour = 'black'
				else:
					grid[i][j].colour = 'white'
		
	# show all cells
	for i in range(0, cols):
		for j in range(0, rows):
			grid[i][j].show()
			
	
def removeFromArray(arr, element):
	# USE ARR.REMOVE(VALUE) INSTEAD
	for i in range(len(arr) - 1, 0, -1):
		if arr[i] == elt:
			arr.pop(i)
			
			
def heuristic(a, b):
	d = abs(a.i - b.i) + abs(a.j - b.j)
	return d
	
	
def draw():
	# KEEP SEARCHING FOR END ----------------------
	if len(openSet) > 0:
		winner = 0
		for i in range(1, len(openSet)):
			if openSet[i].f < openSet[winner].f:
				winner = i
		
		current = openSet[winner]
		
		if current == end:
			end.colour = 'red'
			end.show()
			
			temp = current
			path.append(temp)
			while temp.previous:
				path.append(temp.previous)
				temp = temp.previous
			
		else:
			openSet.remove(current)
			closedSet.append(current)
			current.colour = 'red'
			current.show()
			
			neighbours = current.neighbours
			for neighbour in neighbours:
			
				if neighbour not in closedSet and not neighbour.wall:
					tempG = current.g + 1
					if neighbour in openSet:
						if tempG < neighbour.g:
							neighbour.g = tempG
					else:
						neighbour.g = tempG
						openSet.append(neighbour)
						neighbour.colour = 'green'
						neighbour.show()
						
					neighbour.h = heuristic(neighbour, end)
					neighbour.f = neighbour.g + neighbour.h
					neighbour.previous = current
					
		for i in range(0, len(path)):
			path[i].colour = 'grey'
			path[i].show()
					
			
	# END NOT FOUND -------------------------------
	else:
		pass
		
		
	"""
	OLD METHOD OF UPDATING THE SCREEN
	FAR TOO SLOW
	# DISPLAY SPOTS -------------------------------
	# openSet is green, closedSet is red, neither is white
	for i in range(0, cols):
		for j in range(0, rows):
			if grid[i][j] in openSet:
				grid[i][j].colour = 'green'
			elif grid[i][j] in closedSet:
				grid[i][j].colour = 'red'
			else:
				grid[i][j].colour = 'white'
		
	# show all cells
	for i in range(0, cols):
		for j in range(0, rows):
			grid[i][j].show()
	"""
	
	for i in range(0, len(path)):
		path[i].colour = 'grey'
		path[i].show()
	
	
# initialize Spot objects and graphics window
setup()
time.sleep(7)

# main loop
while True:
	draw()
	
# clean up graphics window
window.getMouse()
window.close()
