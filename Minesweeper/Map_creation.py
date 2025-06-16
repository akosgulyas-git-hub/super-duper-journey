from random import *

def ketjegyu(a):
    if a<10 and a>=0:
        return str("0" + str(a))
    else:
        return str(a)

width = 10
height = 20
mines = 30

def printWorld(width, height, mines):
    print("    ", end="")
    for u in range(width):
        print(ketjegyu(u+1), end=", ")
    print()
    for i in range(height):
        print(ketjegyu(i+1), end=" [")
        for elem in [i]:
            print(ketjegyu(elem), end=", ")
        print("]")

def worldCreation(heigh, widt, mine):
    world = []

    for i in range(heigh):
        world.append([])
        for j in range(widt):
            world[i].append(0)

    for i in range(mine):
        x = randint(0, widt-1)
        y = randint(0, heigh-1)
        while world[y][x] != 0:
            x = randint(0, widt-1)
            y = randint(0, heigh-1)
        world[y][x] = -1

    L = [(-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1)]

    for i in range(heigh):
        for j in range(widt):
            around = 0
            if world[i][j] != -1:
                try: 
                    for u in L:
                        if i + u[0] > -1 and j + u[1] > -1 and i + u[0] < heigh and j + u[1] < widt:
                            if world[i + u[0]][j + u[1]] == -1:
                                around += 1
                except:
                    pass
                world[i][j] = around
    
    return world