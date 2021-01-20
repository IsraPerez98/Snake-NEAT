#the food that the snake eats

from block import Block

class Food:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.block = Block(x,y, "FOOD")
    
    def draw(self,win):
        self.block.draw(win)
    
    def checkCollision(self,snake):
        """
        returns True if a snake ate the food
        """
        #we only have to check the mouth of the snake
        snake_mouth = snake.body[0]

        if(snake_mouth.x == self.x and snake_mouth.y == self.y):
            return True
        
        return False