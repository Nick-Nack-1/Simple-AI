import pygame
import Table
import Players
from GLOBALS import *

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fps = 60
clock = pygame.time.Clock()

running = True

plr1 = Players.Human(screen)
plr2 = Players.AI()
Game = Table.Board([plr1,plr2], (3,3))
plr1.setup(Game)
plr2.setup(Game)

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Game.Update()

    screen.fill((0,0,0))
    plr1.Draw()
    pygame.display.update()
