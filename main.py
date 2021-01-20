import pygame
import neat
from random import randrange
import os

from grid import Grid
from snake import Snake
from food import Food


#GLOBAL VARIABLES
WIN = None
GRID = None
SNAKES = []
FOOD = None

NETS = []
GENOMES = []

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
    global SNAKES
    global FOOD

    #we draw the background
    backgroundColor = (0,0,0)
    pygame.draw.rect(WIN,backgroundColor,(0,0,WINDOW_SIZE[0], WINDOW_SIZE[1]))

    GRID.draw(WIN)
    for snake in SNAKES:
        snake.draw(WIN)
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

    global SNAKES
    colliding_with_snake = False
    for snake in SNAKES:
        for snake_block in snake.body:
            if snake_block.x == food_x and snake_block.y == food_y:
                colliding_with_snake = True
                break
        if colliding_with_snake:
            break

    
    if not colliding_with_snake:
        FOOD = Food(food_x,food_y)
    else:
        return generateFood()

def processKeys(keys):
    #movement
    if keys[pygame.K_w]:
        SNAKES[0].changeDirection(0,-1)
    if keys[pygame.K_a]:
        SNAKES[0].changeDirection(-1,0)
    if keys[pygame.K_s]:
        SNAKES[0].changeDirection(0, 1)
    if keys[pygame.K_d]:
        SNAKES[0].changeDirection(1, 0)
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

    #global SNAKE
    #snake_pos_x = int(round(GRID_SIZE[0] / 2))
    #snake_pos_y = int(round(GRID_SIZE[1] / 2))
    #SNAKE = Snake(snake_pos_x, snake_pos_y)

    generateFood()

def deleteSnake(index):
    SNAKES.pop(index)
    NETS.pop(index)
    GENOMES.pop(index)


def PlayGame():
    """
    function to play a game
    """
    global FOOD
    global GENOMES
    clock = pygame.time.Clock()
    running = True

    MOVESNAKEEVNT = pygame.USEREVENT

    pygame.time.set_timer(MOVESNAKEEVNT, 250)

    while running:
        clock.tick(60)

        keys = pygame.key.get_pressed()
        processKeys(keys)

        if(len(SNAKES)) == 0:
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == MOVESNAKEEVNT:
                for snake_id, snake in enumerate(SNAKES):
                    snake.move()

                    if(snake.collideSelf()):
                        print("SNAKE COLLIDED WITH ITSELF")
                        #running = False
                        GENOMES[snake_id].fitness -= 10
                        deleteSnake(snake_id)
                        break
                
                    if(snake.collideWall(GRID)):
                        print("SNAKE COLLIDED WITH WALL")
                        GENOMES[snake_id].fitness -= 10
                        deleteSnake(snake_id)
                        break
                
                    if(FOOD.checkCollision(snake)):
                        print("SNAKE ATE THE FOOD")
                        SNAKE.grow = True
                        FOOD = None
                        generateFood()
                        GENOMES[snake_id].fitness += 50
                        break
                    
                    # if snake is still alive, give them some fitness
                    GENOMES[snake_id].fitness += 1
                    
                    snake_mouth = snake.body[0]
                    #inputs for neural net
                    inputs = []
                    inputs.insert(0,snake_mouth.x) # mouth pos x
                    inputs.insert(1, snake_mouth.y) # mouth pos y
                    inputs.insert(2, FOOD.x) #food pos x
                    inputs.insert(3, FOOD.y) #food pos y
                    #distance to wall right
                    inputs.insert(4, GRID_SIZE[0] - snake_mouth.x)
                    #distance to wall bottom
                    inputs.insert(5, GRID_SIZE[1] - snake_mouth.y)
                    #distance to body left
                    inputs.insert(6, snake_mouth.x)
                    for i in range(1,len(snake.body)):
                        block = snake.body[i]
                        if (block.y == snake_mouth.y) and (block.x < snake_mouth.x):
                            inputs[6] = snake_mouth.x - block.x
                    #distance to body right
                    inputs.insert(7, GRID_SIZE[0] - snake_mouth.x)
                    for i in range(1,len(snake.body)):
                        block = snake.body[i]
                        if (block.y == snake_mouth.y) and (block.x > snake_mouth.x):
                            inputs[7] =  block.x - snake_mouth.y
                    #distance to body top
                    inputs.insert(8, snake_mouth.y)
                    for i in range(1,len(snake.body)):
                        block = snake.body[i]
                        if (block.x == snake_mouth.x) and (block.y < snake_mouth.y):
                            inputs[8] =  snake_mouth.y - block.y
                    #distance to body bottom
                    inputs.insert(9, GRID_SIZE[1] - snake_mouth.y)
                    for i in range(1,len(snake.body)):
                        block = snake.body[i]
                        if (block.x == snake_mouth.x) and (block.y > snake_mouth.y):
                            inputs[9] =  block.y - snake_mouth.y

                    #outputs of net
                    #ugly, i know :(
                    outputs = NETS[snake_id].activate((inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5],inputs[6],inputs[7],inputs[8],inputs[9]))

                    if outputs[0] > 0.5: #up
                        snake.changeDirection(0,-1)
                    if outputs[1] > 0.5: #left
                        snake.changeDirection(-1,0)
                    if outputs[2] > 0.5: #down
                        snake.changeDirection(0, 1)
                    if outputs[3] > 0.5: #right
                        snake.changeDirection(1, 0)


        
        #SNAKE.move(clock)

        drawWindow()
        pygame.display.update()

#GenerateGame()
#PlayGame()

def instance(genomes,config):
    global NETS
    global SNAKES
    global GENOMES

    snake_pos_x = int(round(GRID_SIZE[0] / 2))
    snake_pos_y = int(round(GRID_SIZE[1] / 2))

    GenerateGame()

    for genome_id, genome in genomes:
        #generate a net
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        NETS.append(net)
        SNAKES.append(Snake(snake_pos_x, snake_pos_y))
        genome.fitness = 0
        GENOMES.append(genome)
    
    PlayGame()
    



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #generate population
    population = neat.Population(config)

    #reporter in terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    #50 generations
    winner = population.run(instance,50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)