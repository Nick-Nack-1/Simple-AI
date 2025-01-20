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

Train_mode =	False

chart = open("chart.txt", "w")
chart.write("Total,Red,Black\n")

Human = Players.Human(Input, Mouse)
# Human = Players.DummyAI()
# Human = Players.AI()
# AI = Players.Human(Input, Mouse)
AI = Players.AI()
Game = None
def new_game():
	global Game, AI, Human, Train_mode
	Game = Table.Board([AI,Human], (3,3), not Train_mode)
	AI.setup(Game)
	Human.setup(Game)

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
	if not Train_mode:
		clock.tick(fps)
	Input.reset_events()
	Mouse.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		Input.update(event)

	if Game.NewGame():
		if Game_end_delay.Update():
			chart.write(f"{Human.score+AI.score},{Human.score},{AI.score}\n")
			new_game()
			if Game.Should_pause:
				Game_end_delay = Table.Pause(30)
			else:
				Game_end_delay = Table.Pause(0)
	else:
		Game.Update()
	
	if Input.keys["F1"]:
		with open("./AIs/DummyAI.txt", "wb") as file:
			print("saving")
			pickle.dump(Human.Moves, file)
	if Input.keys["F2"]:
		with open("./AIs/CurrentAI.txt", "wb") as file:
			print("saving")
			pickle.dump(AI.Moves, file)
	if Input.keys["F3"]:
		with open("./AIs/CurrentAI.txt", "rb") as file:
			print("loading")
			AI.Moves = pickle.load(file)
	if Input.keys["Return"]:
		with open("PrintOut.txt", "w") as file:
			print("printout")
			pprint.pprint(AI.Moves, file)
	if Mouse.press_triggered("Right"):
		Game.Should_pause = not Game.Should_pause
		Train_mode = not Train_mode
	
	if not Train_mode:
		screen.fill((255,255,255))
		Human.Draw(screen=screen)
		Game.ShowWinner(screen, font2)


	pygame.display.set_caption(f"Red: {AI.score} | Black: {Human.score} | Game no.: {Human.score+AI.score}")
	#draw_text(f"Game no.: {plr1.score+plr2.score}", font, (50,50,50), screen, (0,0))
	#draw_text(f"Red(AI): {plr2.score}", font, (50,50,50), screen, (0,20))
	#draw_text(f"Black: {plr1.score}", font, (50,50,50), screen, (0,40))
	
	if not Train_mode:
		pygame.display.update()

chart.close()
