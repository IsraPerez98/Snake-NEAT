import pygame
import neat
from random import randrange
import os
from math import sqrt

from grid import Grid
from snake import Snake
from food import Food


#GLOBAL VARIABLES
GRID_SIZE = [25,25]
SHOW_AFTER_GENERATIONS = 5 #after how many generations should we show the single best snake alone


WIN = None
GRID = None
SNAKES = []
FOOD = None

NETS = []
GENOMES = []

POPULATION = None

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
    global FOOD

    #we draw the background
    backgroundColor = (0,0,0)
    pygame.draw.rect(WIN,backgroundColor,(0,0,WINDOW_SIZE[0], WINDOW_SIZE[1]))

    GRID.draw(WIN)
    FOOD.draw(WIN)

def drawSnakes(snakes):
    global WIN

    for snakes in snakes:
        snakes.draw(WIN)

def generateFood():
    """
    function to generate a food unit (if there is none on screen)
    """
    global FOOD
    #if FOOD != None:
    #    return
    food_x = randrange(GRID_SIZE[0])
    food_y = randrange(GRID_SIZE[1])

    global SNAKES
    colliding_with_snake = False
    for snake in SNAKES:
        snake_mouth = snake.body[0]
        if (snake_mouth.x == food_x) and (snake_mouth.y == food_y):
            colliding_with_snake = True
            break
        #for snake_block in snake.body:
        #    if snake_block.x == food_x and snake_block.y == food_y:
        #        colliding_with_snake = True
        #        break
        #if colliding_with_snake:
        #    break

    
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

def deleteSnake(index, snakes, networks, genomes):
    snakes.pop(index)
    networks.pop(index)
    genomes.pop(index)


def PlayGame(mov_speed, snakes, networks, genomes, training=True):
    """
    function to play a game
    """
    pygame.init()
    global FOOD
    global GRID_SIZE

    clock = pygame.time.Clock()
    running = True
    #game_stuck = False

    #MOVESNAKEEVNT = pygame.USEREVENT + 0 
    #CHECKGAMESTUCK = pygame.USEREVENT + 1
    #print("game speed: ", mov_speed)

    #pygame.time.set_timer(CHECKGAMESTUCK, mov_speed * 100)
    #pygame.time.set_timer(MOVESNAKEEVNT, mov_speed)
    time_elapsed_since_moved = 0
    time_elapsed_since_action = 0

    while running:
        dt = clock.tick()

        time_elapsed_since_moved += dt
        time_elapsed_since_action += dt
            
    
        keys = pygame.key.get_pressed()
        #processKeys(keys)
        if keys[pygame.K_SPACE]:
            for snake_id, snake in enumerate(snakes):
                deleteSnake(snake_id,snakes,networks,genomes)
            time_elapsed_since_action = 0
            running = False
            break

        if(len(snakes)) == 0:
            running = False
            break

        if time_elapsed_since_action > (mov_speed * 250):
        #if no significant actions have taken place in the last x seconds, we reset the game
            print("GAME IS STUCK, ENDING ...")
            for snake_id, snake in enumerate(snakes):
                if training:
                    genomes[snake_id].fitness -= 1000
                deleteSnake(snake_id,snakes,networks,genomes)
                running = False
                time_elapsed_since_action = 0
                break

        if time_elapsed_since_moved > mov_speed:
            time_elapsed_since_moved = 0
            for snake_id, snake in enumerate(snakes):
                snake.move()

                if(snake.collideSelf()):
                    print("SNAKE COLLIDED WITH ITSELF")
                    #running = False
                    if training:
                        genomes[snake_id].fitness -= 2000
                    deleteSnake(snake_id,snakes,networks,genomes)
                    time_elapsed_since_action = 0
                    continue
                
                if(snake.collideWall(GRID)):
                    #print("SNAKE COLLIDED WITH WALL")
                    if training:
                        genomes[snake_id].fitness -= 3000
                    deleteSnake(snake_id, snakes, networks, genomes)
                    time_elapsed_since_action = 0
                    continue
                
                if(FOOD.checkCollision(snake)):
                    print("SNAKE ATE THE FOOD")
                    snake.grow = True
                    #FOOD = None
                    generateFood()
                    if training:
                        genomes[snake_id].fitness += 5000
                    time_elapsed_since_action = 0
                        
                snake_mouth = snake.body[0]
                
                if training:
                    # if snake is still alive, give them some fitness based on distance to the food
                    #GENOMES[snake_id].fitness += 1
                    distance_sqrd = (snake_mouth.x - FOOD.x) ** 2 + (snake_mouth.y - FOOD.y) ** 2
                    mid_dist_sqrd = ((GRID_SIZE[0] ** 2) + (GRID_SIZE[1] ** 2))/4

                    fitness_increase = ((mid_dist_sqrd - distance_sqrd)) / 500
                    #print(fitness_increase)
                    #print(fitness_increase)
                    genomes[snake_id].fitness += fitness_increase

                #inputs for neural net
                inputs = []
                #distance to left wall
                inputs.insert(0,snake_mouth.x) # mouth pos x
                #distance to wall right
                inputs.insert(1, GRID_SIZE[0] - 1 - snake_mouth.x)
                #distance to top wall
                inputs.insert(2, snake_mouth.y) # mouth pos y
                #inputs.insert(2, FOOD.x) #food pos x
                #inputs.insert(3, FOOD.y) #food pos y
                #distance to wall bottom
                inputs.insert(3, GRID_SIZE[1] - 1 - snake_mouth.y)
                #distance to body left
                inputs.insert(4, snake_mouth.x)
                for i in range(1,len(snake.body)):
                    block = snake.body[i]
                    if (block.y == snake_mouth.y) and (block.x < snake_mouth.x):
                        inputs[4] = snake_mouth.x - block.x
                #distance to body right
                inputs.insert(5, GRID_SIZE[0] -1 - snake_mouth.x)
                for i in range(1,len(snake.body)):
                    block = snake.body[i]
                    if (block.y == snake_mouth.y) and (block.x > snake_mouth.x):
                        inputs[5] =  block.x - snake_mouth.y
                #distance to body top
                inputs.insert(6, snake_mouth.y)
                for i in range(1,len(snake.body)):
                    block = snake.body[i]
                    if (block.x == snake_mouth.x) and (block.y < snake_mouth.y):
                        inputs[6] =  snake_mouth.y - block.y
                #distance to body bottom
                inputs.insert(7, GRID_SIZE[1] - 1 - snake_mouth.y)
                for i in range(1,len(snake.body)):
                    block = snake.body[i]
                    if (block.x == snake_mouth.x) and (block.y > snake_mouth.y):
                        inputs[7] =  block.y - snake_mouth.y
                #left distance to food
                inputs.insert(8, snake_mouth.x - FOOD.x )
                #right distance to food
                inputs.insert(9, FOOD.x - snake_mouth.x )
                #top distance to food
                inputs.insert(10, snake_mouth.y - FOOD.y )
                #bottom distance to food
                inputs.insert(11, snake_mouth.y - FOOD.y )

                #outputs of net
                #ugly, i know :(
                outputs = networks[snake_id].activate((inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5],inputs[6],inputs[7],inputs[8],inputs[9], inputs[10], inputs[11]))
                #outputs = NETS[snake_id].activate((inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5],inputs[6],inputs[7],inputs[8],inputs[9]))

                if outputs[0] > 0.5: #up
                    snake.changeDirection(0,-1)
                if outputs[1] > 0.5: #left
                    snake.changeDirection(-1,0)
                if outputs[2] > 0.5: #down
                    snake.changeDirection(0, 1)
                if outputs[3] > 0.5: #right
                    snake.changeDirection(1, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        drawWindow()
        drawSnakes(snakes)
        pygame.display.update()

#GenerateGame()
#PlayGame()

games_until_show = SHOW_AFTER_GENERATIONS
def instance(genomes,config):
    global games_until_show
    global SHOW_AFTER_GENERATIONS

    global NETS
    global SNAKES
    global GENOMES

    global POPULATION

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
    
    PlayGame(20, SNAKES, NETS, GENOMES, training=True)

    #print("best_genome ", POPULATION.best_genome)

    games_until_show -= 1
    if(games_until_show < 1 and POPULATION.best_genome):
        print("SHOWING BEST SNAKE ALONE")
        best_genome = POPULATION.best_genome
        best_network = neat.nn.FeedForwardNetwork.create(best_genome, config)
        best_snake = Snake(snake_pos_x, snake_pos_y)
        
        PlayGame(110, [best_snake], [best_network], [best_genome], training=False)

        games_until_show = SHOW_AFTER_GENERATIONS
    



def run(config_file):
    global POPULATION

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #generate population
    POPULATION = neat.Population(config)

    #reporter in terminal
    POPULATION.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    POPULATION.add_reporter(stats)

    #50 generations
    winner = POPULATION.run(instance,500)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)