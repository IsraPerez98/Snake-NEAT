# This is where we define the block class for each block in the grid
import pygame

class Block:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type

    def draw(self, win):
        color = (158,158,158)
        #20 pixels per block, 2px border at each side (24)
        pygame.draw.rect(win,color,(self.x*24 + 2 , self.y*24 + 2,20,20))