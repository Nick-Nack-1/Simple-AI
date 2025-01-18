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

Pause =True

# plr1 = Players.Human(Input, Mouse)
plr1 = Players.AI()
plr2 = Players.AI()
Game = None
def new_game():
    global Game, plr1, plr2, Pause
    Game = Table.Board([plr1,plr2], (3,3), Pause)
    plr1.setup(Game)
    plr2.setup(Game)

Game_end_delay = Table.Pause(30)

new_game()

# Initialize font
font = pygame.font.SysFont("Arial", 20, bold=True)
font2 = pygame.font.SysFont("Arial", 40, bold=True)

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

    if Game.NewGame():
        if Game_end_delay.Update():
            new_game()
            if Game.Should_pause:
                Game_end_delay = Table.Pause(30)
            else:
                Game_end_delay = Table.Pause(0)
    else:
        Game.Update()
    
    if Input.keys["F1"]:
        with open("./AIs/CurrentAI.txt", "wb") as file:
            print("saving")
            pickle.dump(plr2.Moves, file)
    if Input.keys["F2"]:
        with open("./AIs/CurrentAIv2.txt", "wb") as file:
            print("saving")
            pickle.dump(plr1.Moves, file)
    if Input.keys["F3"]:
        with open("./AIs/CurrentAI.txt", "rb") as file:
            print("loading")
            plr2.Moves = pickle.load(file)
    if Input.keys["Return"]:
        with open("PrintOut.txt", "w") as file:
            print("printout")
            pprint.pprint(plr2.Moves, file)
    if Mouse.press_triggered("Right"):
        Game.Should_pause = not Game.Should_pause
        Pause = not Pause

    screen.fill((255,255,255))
    plr1.Draw(screen=screen)
    Game.ShowWinner(screen, font2)


    pygame.display.set_caption(f"Red: {plr2.score} | Black: {plr1.score} | Game no.: {plr1.score+plr2.score}")
    #draw_text(f"Game no.: {plr1.score+plr2.score}", font, (50,50,50), screen, (0,0))
    #draw_text(f"Red(AI): {plr2.score}", font, (50,50,50), screen, (0,20))
    #draw_text(f"Black: {plr1.score}", font, (50,50,50), screen, (0,40))
    
    pygame.display.update()
