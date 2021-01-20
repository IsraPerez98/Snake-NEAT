#This is where we define our snake class

from block import Block

class Snake:
    def __init__(self,start_posx, start_posy):
        self.size = 2 # we start with 2 blocks

        self.body = []
        for x in range(self.size):
            block = Block(start_posx - x, start_posy, "SNAKE")
            self.body.insert(x, block)
    
    def draw(self, win):
        for x in range(len(self.body)):
            self.body[x].draw(win)
    
    def move(self):
        pass

    def changeDirection(self):
        pass
    
    def collideSelf(self):
        pass

    def collideWall(self, block):
        pass