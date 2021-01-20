#This is where we define our snake class

from block import Block

class Snake:
    def __init__(self,start_posx, start_posy):
        self.size = 2 # we start with 2 block
        self.directionx = 1 # if we are moving in direction x
        self.directiony = 0 # if we are moving in direction y
        self.futuredirectionx = 1
        self.futuredirectiony = 0

        self.body = []
        for x in range(self.size):
            block = Block(start_posx - x, start_posy, "SNAKE")
            self.body.insert(x, block)
    
    def draw(self, win):
        for x in range(len(self.body)):
            self.body[x].draw(win)
    
    def move(self,):
        previousBlock = self.body[0]
        newBlock = Block(previousBlock.x + self.futuredirectionx, previousBlock.y + self.futuredirectiony, "SNAKE")
        self.body.pop()
        self.body.insert(0,newBlock)

        self.directionx = self.futuredirectionx
        self.directiony = self.futuredirectiony

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
        for block_a_index in range(len(self.body)):
            block_a = self.body[block_a_index]

            for block_b_index in range(block_a_index + 1,len(self.body)):
                block_b = self.body[block_b_index]
                if (block_a.x == block_b.x) and (block_a.y == block_b.y):
                    #print(block_a)
                    #print(block_b)
                    return True
        
        return False


    def collideWall(self, block):
        pass