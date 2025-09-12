import Table
import Players
import Inputs
import pickle
import pprint
import os
import time
import copy
from GLOBALS import *


# chart.write("Total,Red,Black, Diff\n")

TotalRuns = 1
Traincycles = 10
Testcycles = 100
TotalLoops = 100
current_cycle = 0
feedback_algo = 1
#1 = feedback on loss, 2 = feedback on win, 3 = feedback on both

# TotalRuns = 2
# Traincycles = 10
# Testcycles = 100
# TotalLoops = 100
# current_cycle = 0

Human = Players.DummyAI()
AI = Players.AI()
# if os.path.exists("./AIs/CurrentAI.txt"):
# 	with open("./AIs/CurrentAI.txt", "rb") as file:
# 		AI.State_Table = pickle.load(file)
Game = None

def new_game():
	global Game, AI, Human
	Game = Table.Board([Human,AI], (3,3), False)
	AI.setup(Game)
	Human.setup(Game)

new_game()

start_time = time.time()



for algo in range(3):
	default_stateTable = {}
	if os.path.exists(f"./AIs/3x3_algo{algo+1}.txt"):
		with open(f"./AIs/3x3_algo{algo+1}.txt", "rb") as file:
			default_stateTable = pickle.load(file)
			print('loaded default state table')
	print(f"Testing algo {algo+1}")
	feedback_algo = algo+1
	Data = []
	for run in range(TotalRuns):	##AMOUNT OF GAMES TO RUN
		Data.append([])
		AI = Players.AI()
		AI.State_Table = copy.deepcopy(default_stateTable)
		for loop in range(TotalLoops):	##CYCLES OF TRAIN-TEST TO RUN
			print(f"Algo: {algo+1} - Run: {run}.{loop}")
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
	with open(f"./AIs/3x3_algo{algo+1}.txt", "wb") as file:
		pickle.dump(AI.State_Table, file)
	with open(f"Charts/Algo_{feedback_algo}/chart_data{algo+1}.txt", "w") as chart:
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

