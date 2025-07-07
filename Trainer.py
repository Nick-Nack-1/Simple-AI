import Table
import Players
import Inputs
import pickle
import pprint
import os
import time
from GLOBALS import *

# 14 141 lines

# ~ 1700 per min
max_cycle = int(input("Max cycles? "))
print(f"time: {max_cycle/18999} minutes")
input("Press enter to start.")
print("Please wait...")
os.remove("chart.txt")
current_cycle = 0

chart = open("chart.txt", "a")
# chart.write("Total,Red,Black, Diff\n")
chart.write("Games,AI Score\n")

# Human = Players.DummyAI()
Human = Players.DummyAI()
# AI = Players.Human(Input, Mouse)
AI = Players.AI()
if os.path.exists("./AIs/CurrentAI.txt"):
	with open("./AIs/CurrentAI.txt", "rb") as file:
		AI.State_Table = pickle.load(file)
Game = None

def new_game():
	global Game, AI, Human
	Game = Table.Board([Human,AI], (3,3), False)
	AI.setup(Game)
	AI.Feedback_algo = 3
	Human.setup(Game)

new_game()

start_time = time.time()

while current_cycle < max_cycle:
	if Game.NewGame():
		chart.write(f"{current_cycle},{AI.score}\n")
		current_cycle += 1
		new_game()

	else:
		Game.Update()

print(f"Completion time: {(time.time()-start_time)/60} minutes")
print(f"Games per minute: {max_cycle/((time.time()-start_time)/60)}")

with open("./AIs/CurrentAI.txt", "wb") as file:
	pickle.dump(AI.State_Table, file)
# with open("./AIs/CurrentAIv2.txt", "wb") as file:
# 	pickle.dump(Human.Moves, file)
with open("PrintOut.txt", "w") as file:
	pprint.pprint(AI.State_Table, file)

print(f"Punish: {AI.punish_num}")
print(f"Revard: {AI.reward_num}")

print("Done")
chart.close()

