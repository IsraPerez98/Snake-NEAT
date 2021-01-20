import pygame
import neat
from random import randrange

from grid import Grid
from snake import Snake
from food import Food


#GLOBAL VARIABLES
WIN = None
GRID = None
SNAKE = None
FOOD = None

GRID_SIZE = [25,25]

#window size = 20 px + 2px border at each side for each block (24)

WINDOW_SIZE = [GRID_SIZE[0] * 24 , GRID_SIZE[0] * 24 ]

#print("WINDOW_SIZE: ", WINDOW_SIZE)

def drawWindow():
    """
    function to draw the window and all the game elements
    """
    global WIN
    global GRID
    global WINDOW_SIZE
    global SNAKE
    global FOOD

    #we draw the background
    backgroundColor = (0,0,0)
    pygame.draw.rect(WIN,backgroundColor,(0,0,WINDOW_SIZE[0], WINDOW_SIZE[1]))

    GRID.draw(WIN)
    SNAKE.draw(WIN)
    FOOD.draw(WIN)

def generateFood():
    """
    function to generate a food unit (if there is none on screen)
    """
    global FOOD
    if FOOD != None:
        return
    food_x = randrange(GRID_SIZE[0])
    food_y = randrange(GRID_SIZE[1])

    global SNAKE
    colliding_with_snake = False
    for snake_block in SNAKE.body:
        if snake_block.x == food_x and snake_block.y == food_y:
            colliding_with_snake = True
            break
    
    if not colliding_with_snake:
        FOOD = Food(food_x,food_y)
    else:
        return generateFood()

def processKeys(keys):
    #movement
    if keys[pygame.K_w]:
        SNAKE.changeDirection(0,-1)
    if keys[pygame.K_a]:
        SNAKE.changeDirection(-1,0)
    if keys[pygame.K_s]:
        SNAKE.changeDirection(0, 1)
    if keys[pygame.K_d]:
        SNAKE.changeDirection(1, 0)
    ###

def GenerateGame():
    """
    function to prepare a game to be played
    """
    pygame.init()
    
    global WIN
    global GRID_SIZE
    
    WIN = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
    
    global GRID
    GRID = Grid(GRID_SIZE[0],GRID_SIZE[1])

    global SNAKE
    snake_pos_x = int(round(GRID_SIZE[0] / 2))
    snake_pos_y = int(round(GRID_SIZE[1] / 2))
    SNAKE = Snake(snake_pos_x, snake_pos_y)

    generateFood()


def PlayGame():
    """
    function to play a game
    """
    global FOOD
    clock = pygame.time.Clock()
    running = True

    MOVESNAKEEVNT = pygame.USEREVENT

    pygame.time.set_timer(MOVESNAKEEVNT, 250)

    while running:
        clock.tick(60)

        keys = pygame.key.get_pressed()
        processKeys(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == MOVESNAKEEVNT:
                SNAKE.move()

                if(SNAKE.collideSelf()):
                    print("SNAKE COLLIDED WITH ITSELF")
                    running = False
                    break
                
                if(SNAKE.collideWall(GRID)):
                    print("SNAKE COLLIDED WITH WALL")
                    running = False
                    break
                
                if(FOOD.checkCollision(SNAKE)):
                    print("SNAKE ATE THE FOOD")
                    SNAKE.grow = True
                    FOOD = None
                    generateFood()
                    break

        
        #SNAKE.move(clock)

        drawWindow()
        pygame.display.update()

GenerateGame()
PlayGame()