import Table
import Players
import Inputs
import pickle
import pprint
import os
from GLOBALS import *

# 14 141 lines

# ~ 100 000 per min
max_cycle = int(input("Max cycles? "))
print(f"time: {max_cycle/1700} minutes")
input("Press enter")
os.remove("chart.txt")
current_cycle = 0

chart = open("chart.txt", "a")
chart.write("Total,Red,Black, Diff\n")

# Human = Players.DummyAI()
Human = Players.DummyAI()
# AI = Players.Human(Input, Mouse)
AI = Players.AI()
if os.path.exists("./AIs/CurrentAI.txt"):
	with open("./AIs/CurrentAI.txt", "rb") as file:
		AI.Moves = pickle.load(file)
Game = None

def new_game():
	global Game, AI, Human
	Game = Table.Board([AI,Human], (3,3), False)
	AI.setup(Game)
	Human.setup(Game)

new_game()


while current_cycle < max_cycle:
	if Game.NewGame():
		chart.write(f"{Human.score+AI.score},{Human.score},{AI.score},{Human.score-AI.score}\n")
		current_cycle += 1
		new_game()

	else:
		Game.Update()
	
	#print(f"Cycle {current_cycle}: {Human.score},{AI.score}, DIFF: {Human.score-AI.score}")


with open("./AIs/CurrentAI.txt", "wb") as file:
	pickle.dump(AI.Moves, file)
with open("./AIs/CurrentAIv2.txt", "wb") as file:
	pickle.dump(Human.Moves, file)
with open("PrintOut.txt", "w") as file:
	pprint.pprint(AI.Moves, file)

print("Done")
chart.close()

