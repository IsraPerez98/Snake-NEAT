# This is where we define the block class for each block in the grid
import pygame

class Block:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
    
    def __str__(self):
        return "Block: type: %s, x: %s, y: %s" % (self.type, self.x, self.y)

    def draw(self, win):
        color = (255,255,255)
        
        if self.type == "NORMAL":
            color = (158,158,158)
        elif self.type == "SNAKE":
            color = (27, 94, 32)
        
        #print("drawing block ", self.type, " ", color, "on pos ", self.x, ",", self.y)
        
        #20 pixels per block, 2px border at each side (24)
        pygame.draw.rect(win,color,(self.x*24 + 2 , self.y*24 + 2,20,20))
