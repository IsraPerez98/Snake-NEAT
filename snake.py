#This is where we define our snake class
from random import randrange

from block import Block

class Snake:
    def __init__(self,start_posx, start_posy):    
        self.directionx = 1 # if we are moving in direction x
        self.directiony = 0 # if we are moving in direction y
        self.futuredirectionx = 1
        self.futuredirectiony = 0

        self.grow = True
        self.color = (randrange(255), randrange(255), randrange(255) )

        self.body = []
        for x in range(1): # we start with 1 block
            block = Block(start_posx - x, start_posy, self.color)
            self.body.insert(x, block)
        
        self.recordLastMovements = False
        self.lastMovements = []
    
    def draw(self, win):
        for x in range(len(self.body)):
            self.body[x].draw(win)
    
    def move(self,):
        previousBlock = self.body[0]
        newBlock = Block(previousBlock.x + self.futuredirectionx, previousBlock.y + self.futuredirectiony, self.color)
        self.body.insert(0,newBlock)

        self.directionx = self.futuredirectionx
        self.directiony = self.futuredirectiony

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        if self.recordLastMovements:
            self.lastMovements.insert(0,newBlock)
            if(len(self.lastMovements) > 50):
                self.lastMovements.pop()

    def changeDirection(self,x,y):
        #if we're moving vertically we can't change direction vertically
        #same for horizontal movement
        if((self.directionx == 1 or self.directionx == -1) and (x == 1 or x == -1 ) ):
            return
        if((self.directiony == 1 or self.directiony == -1) and (y == 1 or y == -1 ) ):
            return
        
        self.futuredirectionx = x
        self.futuredirectiony = y
    
    def collideSelf(self):
        """
        returns True when the snake collides with itself
        """
        #for block_a_index in range(len(self.body)):
        #    block_a = self.body[block_a_index]

        #    for block_b_index in range(block_a_index + 1,len(self.body)):
        #        block_b = self.body[block_b_index]
        #        if (block_a.x == block_b.x) and (block_a.y == block_b.y):
                    #print(block_a)
                    #print(block_b)
        #            return True

        snake_mouth = self.body[0]
        for block_index in range(1,len(self.body)):
            block = self.body[block_index]
            if(snake_mouth.x == block.x) and (snake_mouth.y == block.y):
                return True
        
        return False


    def collideWall(self, grid):
        """
        returns True when the snake collides with a wall
        """
        #for snake_block in self.body:
        #    if snake_block.x < 0 or snake_block.y < 0:
        #        return True
        #    if snake_block.x >= grid.x or snake_block.y >= grid.y:
        #        return True
        snake_mouth = self.body[0]
        if snake_mouth.x < 0 or snake_mouth.y < 0:
            return True
        if snake_mouth.x >= grid.x or snake_mouth.y >= grid.y:
            return True
        return False