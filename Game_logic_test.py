import Table
import pprint

Game = Table.Board([None, None], (3, 3), False)
Game.Turn = -1  # Set the turn to Red
state = [[3,3,3,3,3],
		 [3,0,0,0,3],
		 [3,-1,-1,1,3],
		 [3,0,0,-1,3],
		 [3,3,3,3,3]]
Game.Board = state

pprint.pprint(state)
pprint.pprint(f"win: {Game.Win()}")
pprint.pprint(f"stalemate: {Game.StalemateCheck()}")