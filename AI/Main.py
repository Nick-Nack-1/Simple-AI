import pygame
import Table
import Players
import Inputs
import pickle
from GLOBALS import *

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fps = 60
clock = pygame.time.Clock()

running = True

Input = Inputs.Input_events()
Mouse = Inputs.Mouse()

plr1 = Players.Human(screen, Input, Mouse)
plr2 = Players.AI()
Game = None
def new_game():
    global Game, plr1, plr2
    Game = Table.Board([plr1,plr2], (3,3))
    plr1.setup(Game)
    plr2.setup(Game)


new_game()

while running:
    clock.tick(fps)
    Input.reset_events()
    Mouse.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Input.update(event)

    Game.Update()
    if Game.NewGame():
        new_game()
    
    if Input.keys["F1"]:
        with open("CurrentAI.pkl", "ws") as file:
            pickle.dump(plr2.Moves, file)
    elif Input.keys["F2"]:
        with open("CurrentAI.pkl", "rs") as file:
            plr2.Moves = pickle.load(file)

    screen.fill((255,255,255))
    plr1.Draw()
    pygame.display.update()
