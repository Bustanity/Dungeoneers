#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, random

class lore:
	@classmethod
	def generateText(cls):
		i = random.randint(0, 5)
		text = "UNDEFINED"
		
		if i == 0:
			text = """
				As you enter to the dungeon room a small breeze passes you,
				whispering to your ear that death is close.
				Your sanity is being tested in these dark caves, be strong.
			"""
			
		elif i == 1:
			text = """
				Door after door, you have been doing this for a while but
				nothing seems to be there after all, you wonder if there
				ever was.
			"""
		
		elif i == 2:
			text = """
				You see a shadow lurking beside you and you start running,
				door is closed but luckily, there is another one next to you.
				Door is big, it has writing on it that you can't make sense of
				but the shadow is getting closer so you open the door and go inside.
			"""
		
		else:
			text = """
				Prepare.
			"""
			
		print text

class game:
	gameText = []
	
	class grid:
		grid_table = None
		
		def __init__(self, width, height):
			self.grid_table = [[0 for col in range (width)] for row in range(height)]
					
		def updateGrid(self, x, y, char):
			self.grid_table[x][y] = char
			
		def printGrid(self):
			for row in self.grid_table:
				print row
				
			print "\r\n"
				
	class event:
		@classmethod
		def checkEvent(cls, grid, x, y):
			table = grid.grid_table
			if table[x][y] == 0:
				pass
			elif table[x][y] == 4:
				main()	
			elif table[x][y] == 5:
				item = game.gobjects.getObject(x, y)
				if game.gplayer.items.count(item) < 1:
					game.gplayer.items.append(item)
					game.addText("New item aquired: " + item + "\r\n")
				else:
					game.addText("Found nothing usefull :(\r\n")
			else:
				game.addText("Unhandled event for mark: " + str(table[x][y]) + "\r\n)
	
	class gplayer:
		items = []
		x = 0
		y = 0
		
		@classmethod
		def createPlayer(cls, grid, x, y):
			cls.x = x
			cls.y = y
			grid.updateGrid(x, y, 1)
			
		@classmethod
		def movePlayer(cls, grid, x, y):
			game.event.checkEvent(grid, x, y)
			grid.updateGrid(cls.x, cls.y, 0)
			cls.createPlayer(grid, x, y)
			
		@classmethod
		def position(cls):
			return cls.x, cls.y
						
	class gobjects:
		objects = []
		
		@classmethod
		def createObject(cls, grid, name, x, y, mark):
			cls.objects.append(cls.gobject(grid, name, x, y))
			grid.updateGrid(x, y, mark)
			# print "New object spawned at: [" + str(x) + ", " + str(y) + "] - " + name
			
		@classmethod
		def generateObjects(cls, grid, GRID_WIDTH, GRID_HEIGHT):
			fortuneObjects = ["Soap", "Kite", "Emerald Shield", "Bronze Sword", "Silver Sword", "Hat", "Ration", "Pokeball", "Stick", "Flute", "Guitar", "Spoon"]
			cls.createObject(grid, "Door", 0, random.randint(0, (GRID_WIDTH - 1)), 4)
			
			usedObjects = []
			for i in range(random.randint(0, 3)):
				while True:
					item = fortuneObjects[random.randint(0, (len(fortuneObjects) - 1))]
					
					if item not in usedObjects:
						usedObjects.append(item)
						cls.createObject(grid, item, random.randint(0, (GRID_HEIGHT - 1)), random.randint(0, (GRID_WIDTH - 1)), 5)
						break
					else:
						pass
		@classmethod
		def getObject(cls, x, y):
			for obj in cls.objects:
				if obj.x == x and obj.y == y:
					return obj.name
				
		class gobject:
			grid = None
			name = "UNDEFINED"
			x = 0
			y = 0
			
			def __init__(self, grid, name, x, y):
				self.grid = grid
				self.name = name
				self.x = x
				self.y = y
	
	@classmethod
	def addText(cls, text):
		cls.gameText.append(text)
		print text
		
	@classmethod
	def getText(cls):
		for text in cls.gameText:
			print text

	@classmethod
	def clearText(cls):
		for i in range(0, len(cls.gameText)):
			cls.gameText.pop()
			
	@classmethod		
	def clearScreen(cls):
		os.system("clear")
		cls.getText()
		
	@classmethod
	def waitInput(cls):
		raw_input("Press enter key to continue!")
		
	@classmethod
	def quit(cls):
		print "Rake -> Exiting! Goodbye."
		exit(0)
		
def newGame():
	game.clearText()
	playing = True
	
	game.clearScreen();
	
	GRID_WIDTH = random.randint(15, 30)
	GRID_HEIGHT = random.randint(15, 30)
	# print "\r\nGenerating a new grid - " + str(GRID_WIDTH) + " by " + str(GRID_HEIGHT) + " squares..\r\n"
		
	grid = game.grid(GRID_WIDTH, GRID_HEIGHT)

	game.gobjects.generateObjects(grid, GRID_WIDTH, GRID_HEIGHT)
	
	# print "Positioning the player to the grid\r\n"
	game.gplayer.createPlayer(grid, (GRID_HEIGHT - 1), random.randint(0, (GRID_WIDTH - 1)))
	
	grid.printGrid()
	
	while playing:
		game.clearText()
	
		if (len(game.gplayer.items) > 0):
			game.addText("Items:")
			for item in game.gplayer.items:
				game.addText(item)
			game.addText("\r\n")
			
		nextMove = raw_input("Next move: ")
		game.clearText()
		
		x, y = game.gplayer.position()
		
		if nextMove == "w":
			game.gplayer.movePlayer(grid, (x - 1), y)
		elif nextMove == "a":
			game.gplayer.movePlayer(grid, x, (y - 1))
		elif nextMove == "s":
			game.gplayer.movePlayer(grid, (x + 1), y)
		elif nextMove == "d":
			game.gplayer.movePlayer(grid, x, (y + 1))
		else:
			playing = False
	
		game.clearScreen()
		grid.printGrid()
		
	game.quit()
	
def main():
	game.clearScreen()
	game.clearText()
	
	lore.generateText()
	
	game.waitInput()
	newGame()
	return 0

if __name__ == '__main__':
	main()

