import pygame
import neat

from grid import Grid

#GLOBAL VARIABLES
WIN = None
GRID = None

GRID_SIZE = [25,25]

#window size = 20 px + 2px border at each side for each block (24)

WINDOW_SIZE = [GRID_SIZE[0] * 24 , GRID_SIZE[0] * 24 ]

print("WINDOW_SIZE: ", WINDOW_SIZE)


def drawWindow():
    """
    function to draw the window and all the game elements
    """
    global WIN
    global GRID
    global WINDOW_SIZE

    #we draw the background
    backgroundColor = (0,0,0)
    pygame.draw.rect(WIN,backgroundColor,(0,0,WINDOW_SIZE[0], WINDOW_SIZE[1]))

    GRID.draw(WIN)

def GenerateGame():
    """
    function to prepare a game to be played
    """
    
    global WIN
    global GRID_SIZE
    
    WIN = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
    
    global GRID
    GRID = Grid(GRID_SIZE[0],GRID_SIZE[1])


def PlayGame():
    """
    function to play a game
    """
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        
        drawWindow()
        pygame.display.update()

GenerateGame()
PlayGame()