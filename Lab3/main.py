import pygame
import numpy as np
import time

pygame.init()

#Ancho de la pantalla
width, height = 1000, 1000

screen = pygame.display.set_mode((height,width))

#Color de la pantalla
color = 25,25,25
screen.fill(color)

nxC = 50 #Numero de celdas en x
nyC = 50 #Numero de celdas en y

dimCw = width / nxC
dimCH = height / nyC

# Estadp de las celdas
gameState = np.zeros((nxC,nyC))


gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1

gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1


gameState[41,41] = 1
gameState[42,42] = 1
gameState[42,43] = 1
gameState[41,43] = 1
gameState[40,43] = 1

gameState[20,10] = 1
gameState[20,11] = 1
gameState[20,12] = 1

gameState[10,10] = 1
gameState[11,11] = 1
gameState[12,13] = 1
gameState[11,13] = 1
gameState[10,13] = 1



gameState[10,40] = 1
gameState[11,41] = 1
gameState[12,43] = 1
gameState[11,43] = 1
gameState[10,43] = 1

gameState[30,30] = 1
gameState[32,32] = 1
gameState[32,33] = 1
gameState[31,33] = 1
gameState[30,33] = 1

gameState[34,38] = 1
gameState[34,39] = 1
gameState[34,40] = 1



gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

gameState[47,47] = 1
gameState[48,48] = 1
gameState[48,49] = 1
gameState[47,49] = 1
gameState[47,49] = 1

gameState[43,43] = 1
gameState[44,44] = 1
gameState[44,45] = 1
gameState[43,46] = 1
gameState[44,46] = 1



gameState[43,43] = 1
gameState[28,35] = 1
gameState[17,17] = 1
gameState[17,21] = 1
gameState[48,10] = 1


gameState[29,27] = 1
gameState[29,28] = 1
gameState[29,29] = 1






while True:
    newGameState = np.copy(gameState)
    screen.fill(color)
    time.sleep(0.1)
    for y in range(0,nxC):
        for x in range(0,nyC):

            n_heigh = gameState[(x-1) % nxC,(y-1) % nyC] + \
                      gameState[(x) % nxC,(y-1) % nyC] + \
                      gameState[(x+1) % nxC,(y-1) % nyC] + \
                      gameState[(x-1) % nxC,(y) % nyC] + \
                      gameState[(x+1) % nxC,(y) % nyC] + \
                      gameState[(x-1) % nxC,(y+1) % nyC] + \
                      gameState[(x) % nxC,(y+1) % nyC] + \
                      gameState[(x+1) % nxC,(y+1) % nyC]
                
            if gameState[x,y] == 0 and n_heigh == 3:
                newGameState[x,y] = 1
            
            elif gameState[x,y] == 1 and (n_heigh < 2 or n_heigh > 3):
                newGameState[x,y] = 0
      
            poly = [
                ((x)* dimCw, y * dimCH),
                ((x+1) * dimCw, y * dimCH),
                ((x+1) * dimCw,(y+1) * dimCH),
                ((x) * dimCw,(y+1) * dimCH)
            ]
            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly,1)
            else:
                pygame.draw.polygon(screen, (255,255,255), poly,0)

    gameState = np.copy(newGameState)

    pygame.display.flip()