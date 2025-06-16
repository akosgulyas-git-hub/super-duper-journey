import pygame
from Map_creation import worldCreation, ketjegyu, printWorld

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60
clock = pygame.time.Clock()

height = 10
width = 10
mines = 22

blocksize = 40

SCREEN_HEIGHT = blocksize*(height+1)
SCREEN_WIDTH = blocksize*width

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

texture = 1
coveredImage = {1 : pygame.image.load("Minesweeper/assets/Texture1/WhoKnowsTile.png").convert_alpha(),
                2 : ""
                }

flagImage = {1 : pygame.image.load("Minesweeper/assets/Texture1/Flag.png").convert_alpha(),
             2 : ""
             }

bombImage = {1 : pygame.image.load("Minesweeper/assets/Texture1/Bomb.png").convert_alpha(),
             2 : ""
             }

images = {1 : [pygame.image.load("Minesweeper/assets/Texture1/Tile0.png").convert_alpha(), 
            pygame.image.load("Minesweeper/assets/Texture1/Tile1.png").convert_alpha(), 
            pygame.image.load("Minesweeper/assets/Texture1/Tile2.png").convert_alpha(),
            pygame.image.load("Minesweeper/assets/Texture1/Tile3.png").convert_alpha(),
            pygame.image.load("Minesweeper/assets/Texture1/Tile4.png").convert_alpha(),
            pygame.image.load("Minesweeper/assets/Texture1/Tile5.png").convert_alpha(),
            pygame.image.load("Minesweeper/assets/Texture1/Tile6.png").convert_alpha(),
            pygame.image.load("Minesweeper/assets/Texture1/Tile7.png").convert_alpha(),
            pygame.image.load("Minesweeper/assets/Texture1/Tile8.png").convert_alpha()],
        2 : []
}



Tiles = pygame.sprite.Group()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

def printWorld():
    print("    ", end="")
    for u in range(len(map[0])):
        print(ketjegyu(u+1), end=", ")
    print()
    for i in range(len(map)):
        print(ketjegyu(i+1), end=" [")
        for elem in map[i]:
            print(ketjegyu(elem), end=", ")
        print("]")

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (blocksize, blocksize))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y+blocksize)
        self.type = num
        self.flipped = False
        self.flagged = False
        self.flaggedThisRound = False
        self.exploded = False
        self.correctMines = 0

    def update(self):
        global lose
        global minesleft
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.flaggedThisRound = False
            if clickedLeft and not self.flagged and not self.flipped:
                self.flipped = True
                if self.type == 0:
                    explode(self.rect.center)
                if self.type >= 0:
                    self.image = pygame.transform.scale(images[texture][self.type], (blocksize, blocksize))
                else:
                    global lose
                    self.image = pygame.transform.scale(bombImage[texture], (blocksize, blocksize))
                    lose = True

            if clickedRight and not self.flipped and self.flagged and not self.flaggedThisRound:
                self.flagged = False
                self.image = pygame.transform.scale(coveredImage[texture], (blocksize, blocksize))
                self.flaggedThisRound = True
                flippedMap[getMapPos(self.rect.center)[0]][getMapPos(self.rect.center)[1]] = 0
                minesleft += 1

            if clickedRight and not self.flipped and not self.flagged and not self.flaggedThisRound and minesleft > 0:
                self.flagged = True
                self.image = pygame.transform.scale(flagImage[texture], (blocksize, blocksize))
                self.flaggedThisRound = True
                flippedMap[getMapPos(self.rect.center)[0]][getMapPos(self.rect.center)[1]] = 2
                minesleft -= 1

        if self.flipped:
            if self.type >= 0:
                    self.image = pygame.transform.scale(images[texture][self.type], (blocksize, blocksize))
            else:
                    self.image = pygame.transform.scale(bombImage[texture], (blocksize, blocksize))
                    lose = True
            flippedMap[getMapPos(self.rect.center)[0]][getMapPos(self.rect.center)[1]] = 1
        
        if self.exploded and self.type == 0:
            explode(self.rect.center)
            self.exploded = False

        if self.flipped and clickedLeft and self.rect.collidepoint(pos):
            self.correctMines = 0
            L = [(-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1)]
            try:
                for u in L:
                    point = (pos[0] + u[0]*blocksize, pos[1] + u[1]*blocksize)
                    for sprite in Tiles:
                        if sprite.rect.collidepoint(point):
                            if sprite.flagged:
                                self.correctMines += 1
                print(self.correctMines)
                    
            except:
                pass
            if self.correctMines == self.type:
                explode(self.rect.center)

def getMapPos(pos):
    pos = list(pos)
    pos[1] -= blocksize
    x = int(pos[0]//blocksize)
    y = int(pos[1]//blocksize)
    return [y, x]

def explode(pos):
    L = [(-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1)]
    try:
        for u in L:
            point = (pos[0] + u[0]*blocksize, pos[1] + u[1]*blocksize)
            for sprite in Tiles:
                if sprite.rect.collidepoint(point):
                    if not sprite.flagged:
                        sprite.exploded = True
                        sprite.flipped = True
    except:
        pass

flippedMap = []

run = True
minesleft = mines
# 0 --> plain, not flipped
# 1 --> flipped
# 2 --> flagged

for i in range(height):
    flippedMap.append([])
    for j in range(width):
        flippedMap[i].append(0)

map = worldCreation(height, width, mines)

for i in range(height):
    for j in range(width):
        tile = Tile(j*blocksize, i*blocksize, coveredImage[texture], map[i][j])
        Tiles.add(tile)

while not pygame.mouse.get_pressed()[0] and run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    Tiles.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pos = pygame.mouse.get_pos()
while map[getMapPos(pos)[0]][getMapPos(pos)[1]] != 0:
    map = worldCreation(height, width, mines)

Tiles = pygame.sprite.Group()
for i in range(height):
    for j in range(width):
        tile = Tile(j*blocksize, i*blocksize, coveredImage[texture], map[i][j])
        Tiles.add(tile)

realFlippedMap = []

for sor in map:
    unit = []
    for elem in sor:
        if elem == -1:
            unit.append(2)
        else:
            unit.append(1)
    realFlippedMap.append(unit)

clickedLeft = True
clickedRight = False
Tiles.update()

printWorld()
lose = False
win = False
while run:
    screen.fill("white")
    draw_text(f"{minesleft}", pygame.font.SysFont(None, int(blocksize*9/10)), "black", SCREEN_WIDTH//3, blocksize//2)
    clickedRight = False
    clickedLeft = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not lose and not win:
                if event.button == 3:
                    clickedRight = True
                if event.button == 1:
                    clickedLeft = True
        if event.type == pygame.QUIT:
            run = False
    if clickedRight and clickedLeft:
        clickedRight = False
    Tiles.update()
    Tiles.draw(screen)
    clock.tick(FPS)
    if minesleft == 0:
        pass
    if flippedMap == realFlippedMap:
        win = True
    if lose:
        draw_text("Lost", pygame.font.SysFont(None, SCREEN_WIDTH//3, True), "black", SCREEN_WIDTH//2, (SCREEN_HEIGHT-blocksize)//2+blocksize)
        draw_text("Lost", pygame.font.SysFont(None, SCREEN_WIDTH//3, False), "white", SCREEN_WIDTH//2, (SCREEN_HEIGHT-blocksize)//2+blocksize)
    if win:
        draw_text("Victory", pygame.font.SysFont(None, SCREEN_WIDTH//3, True), "black", SCREEN_WIDTH//2, (SCREEN_HEIGHT-blocksize)//2+blocksize)
        draw_text("Victory", pygame.font.SysFont(None, SCREEN_WIDTH//3, False), "white", SCREEN_WIDTH//2, (SCREEN_HEIGHT-blocksize)//2+blocksize)
    pygame.display.flip()

pygame.quit()