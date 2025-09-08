import Table
import Players
import Inputs
import pickle
import pprint
import os
import sys
import time
import copy
from GLOBALS import *


# chart.write("Total,Red,Black, Diff\n")

#TotalRuns = 100
#Traincycles = 10
#Testcycles = 1000
#TotalLoops = 100
#current_cycle = 0
if len(sys.argv) > 1:
	feedback_algo = int(sys.argv[1])
else:
	feedback_algo = int(input('Enter feedback algorithm (neg|1|, pos|2|, both|3|): '))
#1 = feedback on loss, 2 = feedback on win, 3 = feedback on both

TotalRuns = 1
Traincycles = 10
Testcycles = 10
TotalLoops = 10
current_cycle = 0

Human = Players.DummyAI()
AI = Players.AI()
Game = None

def new_game():
	global Game, AI, Human
	Game = Table.Board([Human,AI], (3,3), False)
	AI.setup(Game)
	Human.setup(Game)

new_game()

start_time = time.time()


default_stateTable = {}
if os.path.exists(f"./AIs/3x3_algo{feedback_algo}.txt"):
	with open(f"./AIs/3x3_algo{feedback_algo}.txt", "rb") as file:
		default_stateTable = pickle.load(file)
		print('loaded default state table')
print(f"Testing algo {feedback_algo}")
Data = []
for run in range(TotalRuns):	##AMOUNT OF GAMES TO RUN
	Data.append([])
	AI = Players.AI()
	AI.State_Table = copy.deepcopy(default_stateTable)
	for loop in range(TotalLoops):	##CYCLES OF TRAIN-TEST TO RUN
		print(f"Algo: {feedback_algo} - Run: {run}.{loop}")
		for state in range(2):
			AI.score = 0
			if state == 0:
				AI.Feedback_algo = 0
				cycles = Testcycles
				with open(f"./StateTable_printouts/Type{feedback_algo}_Table_pretest{loop}.txt", "w") as file:
					pprint.pprint(AI.State_Table, file)
			elif state == 1:
				AI.Feedback_algo = feedback_algo
				cycles = Traincycles
			##RUN GAME START
			for cycle in range(cycles):
				while True:
					if Game.NewGame():
						new_game()
						break
					else:
						Game.Update()
			##RUN GAME END
			if state == 0:
				with open(f"./StateTable_printouts/Type{feedback_algo}_Table_post_test{loop}.txt", "w") as file:
					pprint.pprint(AI.State_Table, file)
				Data[run].append(AI.score)
	#Last test
	AI.score = 0
	AI.Feedback_algo = 0
	for cycle in range(Testcycles):
		while True:
			if Game.NewGame():
				new_game()
				break
			else:
				Game.Update()
	Data[run].append(AI.score)

with open(f"./StateTable_printouts/Type{feedback_algo}_Table{loop}.txt", "w") as file:
	pprint.pprint(AI.State_Table, file)
with open(f"./AIs/3x3_algo{feedback_algo}.txt", "wb") as file:
	pickle.dump(AI.State_Table, file)
with open(f"Charts/Algo_{feedback_algo}/chart_data{feedback_algo}.txt", "w") as chart:
	chart.write("Test,AI Score\n")
	print(Data)
	for loop in range(TotalLoops+1):
		avrg = 0
		for run in range(TotalRuns):
			avrg += Data[run][loop]
		avrg /= TotalRuns
		chart.write(f"{loop},{avrg}\n")


print(f"Completion time: {(time.time()-start_time)/60} minutes")
max_cycle = (Testcycles+Traincycles)*TotalLoops*TotalRuns
print(f"Games per minute: {max_cycle/((time.time()-start_time)/60)}")

