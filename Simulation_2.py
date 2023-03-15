import pygame
import random
import time
import numpy as np
import pandas as pd

#Returns colours of alive, surrounded, and seed.
def generate_colours(): #Here generate colours for our unique classes.
    col_alive = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
    col_surrounded = (col_alive[0] - 50, col_alive[1] - 50, col_alive[2] - 50)

    col_seed = (col_alive[0] + 50, col_alive[1] + 50, col_alive[2] + 50)

    return {"col_alive": col_alive,"col_surrounded": col_surrounded,"col_seed": col_seed}


#In my laziness, create a function to create a string for a particular species.
def generate_types(number):
    return {"alive":number,"seed":number+1}

def generate_species(requested_species):
    species_list = []
    count = 1
    for i in requested_species:
        type = generate_types(count)
        colours = generate_colours()
        species_list.append({i: type|colours})
        count += 2
    return species_list #Creates a list of species. Each species has a dictionary of their colours and states (alive / seed)


def update(surface,cells,cell_size,display):
    new_cells = pd.DataFrame(pd.DataFrame(np.zeros(display)))

    for index, row in cells.iterrows():
        for i in row.index:
            #print(f"At position {index,i} : {row[i]}")
            if row[i] == 0:
                continue
            elif row[i] %  2 == 0:
                adjust = -1
            else:
                adjust = 1
            #Here dealing with bugs finding surrounding values of a dataframe near edges.
            if index == 0:
                if i == 0:
                    surround = cells.iloc[index:index+2,i:i+2]
                    new_surround = new_cells.iloc[index: index + 2, i: i+2]
                else:
                    surround = cells.iloc[index:index+2,i-1:i+2]
                    new_surround = new_surround.iloc[index: index + 2, i: i+2]
            elif i == 0:
                surround = cells.iloc[index-1:index+2,i:i+2]
                new_surround = new_surround.iloc[index: index + 2, i: i+2]
            else:
                surround = cells.iloc[index-1:index+2,i-1:i+2]
                new_surround = new_surround.iloc[index: index + 2, i: i+2]
            print(surround,"\n\n")
            #print(row[i])

            #Okay, so for entry at position (row, column) = (type)
            # (index, i) = (row[i])
            #Types are x = alive, seed : a = 1, 2 b = 3, 4, c = 5, 6

            #Count occurances in surrounding area in current area
            values,num_occurances = (np.unique(surround.values,return_counts=True))

            #Number of other, same, and dead tiles.
            num_else = 0
            num_self = 0
            num_dead = 0
            for i in len(values):
                if values[i] == 0:
                    num_dead = num_occurances[i]
                elif values[i] == row[i] or values[i] == row[i]+adjust:
                    num_self += num_occurances[i]
                else:
                    num_else += num_occurances[i]

            values, num_occurances = (np.unique(new_surround.values, return_counts=True))

            # Number of other, same, and dead tiles.
            new_num_else = 0
            new_num_self = 0
            new_num_dead = 0
            for i in len(values):
                if values[i] == 0:
                    new_num_dead = num_occurances[i]
                elif values[i] == row[i] or values[i] == row[i]+adjust:
                    new_num_self += num_occurances[i]
                else:
                    new_num_else += num_occurances[i]

            if row[i] % 2 != 0: #This is when the value is odd, therefore a planter / alive.
                if num_else == 0 and num_dead > 0: #If not surrounded by any else, and open spot
                    #plant
                    pass
                #Want planting to be seperate from death / staying alive.
                if num_else >= 3 or num_self <= 1: #If too many else, too few friends, or both, die
                    new_cells.iloc[index,i] == 0
                else: #If not able to die, stay alive.
                    new_cells.iloc[index, i] == row[i]

            if row[i] % 2 == 0: #So if a value is even, that means it is a






    """
    for i, row in cells.iterrows():
        count=0
        for j in row:
            #At position (row = i, col = count) in the dataframe, has value of j.
            if j == 0:
                continue
            print(i,count,":",j)
            surrounding = cells.iloc[i-1:i+2,count-1:count+2]
            print(surrounding)
            count+=1
        if count > 200:
            return cells
    print(cells)
    """
    return cells
def main():
    pygame.init()
    display = (120,120)
    cell_size = 8
    surface = pygame.display.set_mode(size=(display[0]*cell_size,display[1]*cell_size))
    cells = pd.DataFrame(np.zeros(display))

    #Ok so I want to implement multiple species one day but for right now that was too complicated in the Update
    #So, it is half implemented here, and thrown out in Update function.
    species = ["a","b","c"]
    species_list = generate_species(species)
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            if random.randint(0,100) > 80:
                choice = random.choice(species_list)
                for n in species:
                    try:
                        cells.iloc[[i],[j]] = choice[n]["alive"]
                    except: pass

    running,pause = 0,1
    state = running

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
            # Creates background
            surface.fill((30, 30, 60))

            # Updates the cells to be alive or dead
            cells = update(surface, cells,cell_size,display)
            pygame.display.update()
            return
        elif state == pause:
            continue


main()
