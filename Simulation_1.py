# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random
import time
import numpy as np
col_dead = (random.randint(0,50),random.randint(0,50),random.randint(0,55))
col_alive = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
col_surrounded = (col_alive[0]-50,col_alive[1]-50,col_alive[2]-50)

def generate_colours():
    col_alive = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
    col_surrounded = (col_alive[0] - 50, col_alive[1] - 50, col_alive[2] - 50)

    col_seed = (col_alive[0] + 50, col_alive[1] + 50, col_alive[2] + 50)

    return col_alive, col_surrounded, col_seed

def update(surface,cells,cellsize=8):
    new_cells = np.zeros((cells.shape[0],cells.shape[1]))
    for row,col in np.ndindex(cells.shape):
        num_alive = np.sum(cells[row-1:row + 2,col-1:col+2])
        is_alive = cells[row, col]

        #This is for debugging
        #print(row,col, " is : ", is_alive , "with this many around it :" ,num_alive)

        if is_alive == 0: #When dead

            if num_alive >= 4: #If surrounded by n alive cells, become alive
                colour = col_alive
                new_cells[row, col] = 1

            else: #Else, if surrounded by less than n, stay dead
                colour = col_dead
                new_cells[row, col] = 0

        elif is_alive == 1: #When alive
            if num_alive <= 1: #If surrounded by n or fewer alive cells die
                colour = col_dead
                new_cells[row, col] = 0

            elif num_alive > 8: #When surrounded by more than n cells, take on surrounded cell colouring for cool fx
                colour = col_surrounded
                new_cells[row, col] = 1
            else: # else live
                colour = col_alive
                new_cells[row, col] = 1
        pygame.draw.rect(surface,colour,rect=(col*8,row*8,8-1,8-1))
    return new_cells


def main():
    pygame.init()
    display_x,display_y = 120,120
    #The display will be composed of 8x8 pixel blocks. So we have a 120x90 grid of 8x8 squares.
    surface = pygame.display.set_mode(size=(display_x*8,display_y * 8))
    cells = np.zeros((display_x,display_y))

    #Keeps track of generation
    count = 0

    #Randomly assigns alive cells to begin
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            if random.randint(0,100) > 80:
                cells[i,j] = 1

    # Allows for checking if the sim is running or not
    running, pause = 0,1
    state = running
    #Sim loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: state = pause
                if event.key == pygame.K_o: state = running


        if state == running:
            #Creates background
            surface.fill((30,30,60))

            #Updates the cells to be alive or dead
            cells = update(surface,cells)
            pygame.display.update()
            count += 1
        elif state == pause:
            continue


main()