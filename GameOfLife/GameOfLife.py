#Game of Life program
#by Jerik David Hincapie Bedoya
import pygame
import numpy as np
import time

pygame.init()
# Set the width and height of the screen [width, height]
width, height = 750, 750
# Create the screen
screen = pygame.display.set_mode((height, width))
# screen color
bg = 25, 25, 25
# set screen color
screen.fill(bg)

# num of cells
nxC, nyC = 25, 25

# cell size
dimCW = width / nxC
dimCH = height / nyC

# state of cells. 0 = dead, 1 = alive
gameState = np.zeros((nxC, nyC))

# set initial state	
# Autómata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Autómata móvil
gameState[10, 10] = 1
gameState[11, 11] = 1
gameState[11, 12] = 1
gameState[10, 12] = 1
gameState[9, 12] = 1

# Execution game control
pauseExect = False

# execution loop
while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)
    # Register events of the keyboard
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nyC):
        for x in range(0, nxC):
            if not pauseExect:
                # get neighboring coordinates
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x) % nxC, (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC, (y) % nyC] + \
                        gameState[(x + 1) % nxC, (y) % nyC] + \
                        gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                        gameState[(x) % nxC, (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y + 1) % nyC]
                # apply rules
                # rule 1: Any die cell with exactly three live neighbours becomes a live cell.
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # rule 2: Any live cell with less than two or more than three live neighbours, "die".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # create a polygon for each cell
            poly = [((x) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ((x) * dimCW, (y + 1) * dimCH)]
            # draw the polygon
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    # update the game state
    gameState = np.copy(newGameState)
    # update the screen
    pygame.display.flip()