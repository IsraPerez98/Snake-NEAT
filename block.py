# This is where we define the block class for each block in the grid
import pygame

class Block:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
    
    def __str__(self):
        return "Block: color: %s, x: %s, y: %s" % (self.color, self.x, self.y)

    def draw(self, win):
        
        #20 pixels per block, 2px border at each side (24)
        pygame.draw.rect(win,self.color,(self.x*24 + 2 , self.y*24 + 2,20,20))
