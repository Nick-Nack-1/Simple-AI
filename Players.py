import Table
import pygame
import Inputs
import random
from GLOBALS import *

class Human():
	def __init__(self, inp:Inputs.Input_events, mouse:Inputs.Mouse):
		self.board = None
		self.Inputs = inp
		self.Mouse = mouse
		self.select_pos = None

		self.score = 0
		

	def setup(self, board_obj):
		self.game = board_obj

	def GetBoard(self, board):
		self.board = board

	def Play(self, board, plr_key:int) -> tuple|None:
		self.board = board
		if self.Mouse.press_triggered("Left"):
			size = (len(self.game.Board[0]),len(self.game.Board))
			grid_space = (int(SCREEN_WIDTH/(size[0]-2)),int(SCREEN_HEIGHT/(size[1]-2)))
			pos = self.Mouse.peek_pos()
			new_select = pos[0]//grid_space[0], pos[1]//grid_space[1]
			if self.select_pos == None:
				self.select_pos = new_select
				if self.board[self.select_pos[1]+1][self.select_pos[0]+1] != plr_key:
					self.select_pos = None
			
			elif self.board[new_select[1]+1][new_select[0]+1] == plr_key:
				self.select_pos = new_select

			else:
				move = (pos[0]//grid_space[0], pos[1]//grid_space[1])
				if move[0] == self.select_pos[0] and move[1] == self.select_pos[1]-1:
					move = (self.select_pos,"M")
				elif move[0] == self.select_pos[0]+1 and move[1] == self.select_pos[1]-1:
					move = (self.select_pos,"R")
				elif move[0] == self.select_pos[0]-1 and move[1] == self.select_pos[1]-1:
					move = (self.select_pos,"L")
				else:
					self.select_pos = None
					return None
				if self.game.ValidateMove(move, self.board):
					self.select_pos = None
					return move
		return None

	def Draw(self, screen):
		if self.board != None:
			size = (len(self.game.Board[0]),len(self.game.Board))
			grid_space = (int(SCREEN_WIDTH/(size[0]-2)),int(SCREEN_HEIGHT/(size[1]-2)))
			##Grid
			for y in range(size[1]-3):
				y_pos = grid_space[1]*(y+1)
				pygame.draw.line(screen, ((128,128,128)),(0,y_pos), (SCREEN_WIDTH,y_pos),width=3)
			for x in range(size[0]-3):
				x_pos = grid_space[0]*(x+1)
				pygame.draw.line(screen, ((128,128,128)),(x_pos,0), (x_pos, SCREEN_WIDTH),width=3)

			##Dots
			for y in range(size[1]-2):
				for x in range(size[0]-2):
					dot = self.board[y+1][x+1]
					pos = (x*grid_space[0]+grid_space[0]//2, y*grid_space[1]+grid_space[1]//2)
					if dot == 1:
						pygame.draw.circle(screen, (0,0,0), center=pos, radius=grid_space[1]//2 -4)
					elif dot == -1:
						pygame.draw.circle(screen, (255,0,0), center=pos, radius=grid_space[1]//2 -4)
	def End(self, win:bool):
		if win:
			self.score += 1

class AI():
	def __init__(self):
		self.last_move = [(0,0),"M",0]
		self.score = 0
		self.State_Table = {}
		self.board = None
		self.Feedback_algo = 0
		self.base_weight_score = 2
		self.reward_num = 0
		self.punish_num = 0
		#0 = no feedback, 1 = feedback on loss, 2 = feedback on win, 3 = feedback on both
		
	def setup(self, board_obj):
		self.game = board_obj
	
	def GetBoard(self, board):
		self.board = board
	
	def Play(self, board, plr_key:int) -> list|None:
		board_state = ()
		for y in range(len(board)-2):
			board_state = board_state + tuple(board[y+1][1:-1])

		if board_state not in self.State_Table:
			self.State_Table[board_state] = []
			for y in range(len(board)-2):
				for x in range(len(board[0])-2):
					if board[y+1][x+1] == plr_key:
						for m in ["M","L","R"]:
							if self.game.ValidateMove(((x,y),m), board):
								self.State_Table[board_state].append([(x,y),m, self.base_weight_score])

		possible_moves = self.State_Table[board_state]
		weights = []
		weight_sum = 0
		for m in possible_moves:
			weight_sum += m[2]
			weights.append(m[2])

		if weight_sum == 0:
			if self.Feedback_algo != 0:
				self.last_move[2] = 0
				self.punish_num += 1
			self.last_move = possible_moves[random.randint(0,len(possible_moves)-1)]
			return self.last_move[0:2]
		else:
			self.current_move = random.choices(possible_moves, weights=weights, k=1)[0]
			if self.current_move[2] > self.base_weight_score*2:
				if self.Feedback_algo != 0:
					self.last_move[2] += 1
					self.reward_num += 1
			self.last_move = self.current_move
			return self.last_move[0:2]
	
	def End(self, win:bool):
		if win:
			self.score += 1
			if self.Feedback_algo == 2 or self.Feedback_algo == 3:
				self.last_move[2] += 1  #haal die lyn uit vir ai om vinniger te leer
				self.reward_num += 1
		else:
			if self.Feedback_algo == 1 or self.Feedback_algo == 3:
				if self.last_move[2] > 0:
					self.last_move[2] -= 1
					self.punish_num += 1
		self.last_move = [(0,0),"M",0]

	def Draw(self, screen):
		if self.board != None:
			size = (len(self.game.Board[0]),len(self.game.Board))
			grid_space = (int(SCREEN_WIDTH/(size[0]-2)),int(SCREEN_HEIGHT/(size[1]-2)))
			##Grid
			for y in range(size[1]-3):
				y_pos = grid_space[1]*(y+1)
				pygame.draw.line(screen, ((128,128,128)),(0,y_pos), (SCREEN_WIDTH,y_pos),width=3)
			for x in range(size[0]-3):
				x_pos = grid_space[0]*(x+1)
				pygame.draw.line(screen, ((128,128,128)),(x_pos,0), (x_pos, SCREEN_WIDTH),width=3)

			##Dots
			for y in range(size[1]-2):
				for x in range(size[0]-2):
					dot = self.board[y+1][x+1]
					pos = (x*grid_space[0]+grid_space[0]//2, y*grid_space[1]+grid_space[1]//2)
					if dot == 1:
						pygame.draw.circle(screen, (0,0,0), center=pos, radius=grid_space[1]//2 -4)
					elif dot == -1:
						pygame.draw.circle(screen, (255,0,0), center=pos, radius=grid_space[1]//2 -4)
			

class DummyAI():
	def __init__(self):
		self.last_move = [(0,0),"M",0]
		self.score = 0
		self.board = None
		self.State_Table = None	#place holder
		
	def setup(self, board_obj):
		self.game = board_obj
	
	def GetBoard(self, board):
		self.board = board
	
	def Play(self, board, plr_key:int) -> list|None:
		board_state = ()
		for y in range(len(board)-2):
			board_state = board_state + tuple(board[y+1][1:-1])

		Moves = []
		for y in range(len(board)-2):
			for x in range(len(board[0])-2):
				if board[y+1][x+1] == plr_key:
					for m in ["M","L","R"]:
						if self.game.ValidateMove(((x,y),m), board):
							Moves.append([(x,y),m,1])
		

		if len(Moves) != 0:
			self.last_move = Moves[random.randint(0,len(Moves)-1)]
			return self.last_move[0:2]
	
	def End(self, win:bool):
		if win:
			self.score += 1

	def Draw(self, screen):
		if self.board != None:
			size = (len(self.game.Board[0]),len(self.game.Board))
			grid_space = (int(SCREEN_WIDTH/(size[0]-2)),int(SCREEN_HEIGHT/(size[1]-2)))
			##Grid
			for y in range(size[1]-3):
				y_pos = grid_space[1]*(y+1)
				pygame.draw.line(screen, ((128,128,128)),(0,y_pos), (SCREEN_WIDTH,y_pos),width=3)
			for x in range(size[0]-3):
				x_pos = grid_space[0]*(x+1)
				pygame.draw.line(screen, ((128,128,128)),(x_pos,0), (x_pos, SCREEN_WIDTH),width=3)

			##Dots
			for y in range(size[1]-2):
				for x in range(size[0]-2):
					dot = self.board[y+1][x+1]
					pos = (x*grid_space[0]+grid_space[0]//2, y*grid_space[1]+grid_space[1]//2)
					if dot == 1:
						pygame.draw.circle(screen, (0,0,0), center=pos, radius=grid_space[1]//2 -4)
					elif dot == -1:
						pygame.draw.circle(screen, (255,0,0), center=pos, radius=grid_space[1]//2 -4)