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

# Initialize font
font = pygame.font.SysFont("Arial", 20, bold=True)
font2 = pygame.font.SysFont("Arial", 40, bold=True)

def draw_text(text, font, color, surface, pos):
	textobj = font.render(text, True, color)
	textrect = textobj.get_rect()
	textrect.topleft = pos
	surface.blit(textobj, textrect)

running = True

Input = Inputs.Input_events()
Mouse = Inputs.Mouse()

Human = Players.Human(Input, Mouse)
AI = Players.AI()
AI.Feedback_algo = 3
AI_Difficulty = 'Untrained'
Game = None
def new_game():
	global Game, AI, Human
	Game = Table.Board([Human,AI], (3,3), True)
	AI.setup(Game)
	Human.setup(Game)

Game_end_delay = Table.Pause(30)

Game_count = 0

new_game()

while running:
	clock.tick(fps)
	Input.reset_events()
	Mouse.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		Input.update(event)

	if Game.NewGame():
		Game_count +=1
		if Game_end_delay.Update():
			new_game()
			if Game.Should_pause:
				Game_end_delay = Table.Pause(30)
			else:
				Game_end_delay = Table.Pause(0)
	else:
		Game.Update()
	
	
	if Input.keys["F1"]:
		AI.Feedback_algo = 1
	elif Input.keys["F2"]:
		AI.Feedback_algo = 2
	elif Input.keys["F3"]:
		AI.Feedback_algo = 3
	if Input.keys["U"]:
		AI.State_Table = {}
		AI_Difficulty = 'Untrained'
		AI.score = 0
		Human.score = 0
	elif Input.keys["T"]:
		with open("./AIs/PerfectModel.txt", "rb") as file:
			AI.State_Table = pickle.load(file)
		AI_Difficulty = 'Trained'
		AI.score = 0
		Human.score = 0
	if Input.keys["Return"]:
		with open("PrintOut.txt", "w") as file:
			pprint.pprint(AI.State_Table, file)


	screen.fill((255,255,255))
	Human.Draw(screen=screen)
	draw_text(f"algo: {['P','R','R&P'][AI.Feedback_algo-1]}", font, (0,0,0), screen, (0,0))
	draw_text(f"agent: {AI_Difficulty}", font, (0,0,0), screen, (0,20))
	Game.ShowWinner(screen, font2)
	pygame.display.set_caption(f"Red: {AI.score} | Black: {Human.score} | Game no.: {AI.score+Human.score}")

	pygame.display.update()
