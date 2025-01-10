import pygame
import Table
import Players
import Inputs
import pickle
import pprint
from GLOBALS import *

pygame.init()

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

# Initialize font
font = pygame.font.SysFont("Arial", 20, bold=True)

def draw_text(text, font, color, surface, pos):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = pos
    surface.blit(textobj, textrect)


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
        with open("./AIs/CurrentAI.txt", "wb") as file:
            pickle.dump(plr2.Moves, file)
    if Input.keys["F2"]:
        with open("./AIs/CurrentAI.txt", "rb") as file:
            plr2.Moves = pickle.load(file)
    if Input.keys["F3"]:
        with open("PrintOut.txt", "w") as file:
            pprint.pprint(plr2.Moves, file)

    screen.fill((255,255,255))
    plr1.Draw()
    
    draw_text(f"Red: {plr2.score}", font, (150,150,150), screen, (0,0))
    draw_text(f"Black: {plr1.score}", font, (150,150,150), screen, (0,20))

    pygame.display.update()
