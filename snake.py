#This is where we define our snake class

from block import Block

class Snake:
    def __init__(self,start_posx, start_posy):
        self.size = 4 # we start with 2 block
        self.directionx = 1 # if we are moving in direction x
        self.directiony = 0 # if we are moving in direction y

        self.body = []
        for x in range(self.size):
            block = Block(start_posx - x, start_posy, "SNAKE")
            self.body.insert(x, block)
    
    def draw(self, win):
        for x in range(len(self.body)):
            self.body[x].draw(win)
    
    def move(self,):
        previousBlock = self.body[0]
        newBlock = Block(previousBlock.x + self.directionx, previousBlock.y + self.directiony, "SNAKE")
        self.body.pop()
        self.body.insert(0,newBlock)

    def changeDirection(self,x,y):
        #if we're moving vertically we can't change direction vertically
        #same for horizontal movement
        if((self.directionx == 1 or self.directionx == -1) and (x == 1 or x == -1 ) ):
            return
        if((self.directiony == 1 or self.directiony == -1) and (y == 1 or y == -1 ) ):
            return
        
        self.directionx = x
        self.directiony = y
    
    def collideSelf(self):
        pass

    def collideWall(self, block):
        pass