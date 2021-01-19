#This is where we define our grid for the game

from block import Block

class Grid:
    def __init__(self,x,y):
        #the grid has dimensions x * y
        self.x = x
        self.y = y

        self.generateStructure()

    def generateStructure(self):
        structure = []

        for x in range(self.x):
            #print("x: ", x)
            structure.insert(x,[])
            for y in range(self.y):
                #print("generating grid ", x, " ", y)
                block = Block(x,y, "NORMAL")
                structure[x].insert(y, block)
        
        self.structure = structure

    def draw(self,win):
        for x in range(self.x):
            for y in range(self.y):
                self.structure[x][y].draw(win)
