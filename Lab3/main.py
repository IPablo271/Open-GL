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

gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1


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