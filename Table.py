import copy
from GLOBALS import *
import pygame

class Board():
	def __init__(self, Plrs:list, Board_size, pause = True):
		self.Should_pause = pause
		self.Players = {}
		self.Players[1] = [Plrs[0],0]
		self.Players[-1] = [Plrs[1],0]
		
		self.Turn = 1
		self.Turn_count = 7
		self.moved = False
		self.turn_pause = None
		self.win = False

		self.Size = Board_size
		
		possible_boards = {(3,3):[[3,3,3,3,3],[3,-1,-1,-1,3],[3,0,0,0,3],[3,1,1,1,3],[3,3,3,3,3]],
						   (4,4):[[3,3,3,3,3,3],[3,-1,-1,-1,-1,3],[3,0,0,0,0,3],[3,0,0,0,0,3],[3,1,1,1,1,3],[3,3,3,3,3,3]]}
		self.Board = possible_boards[Board_size]
	

	def Update(self):
		self.Players[self.Turn*-1][0].GetBoard(self.Reflect(x=True, y=True))
		if self.moved == False:
			Current_plr = self.Players[self.Turn][0]
			move = Current_plr.Play(self.Board, self.Turn)
			if move != None:
				self.moved = True
				if move[1] == "M":
					self.Board[move[0][1]+1][move[0][0]+1] = 0
					self.Board[move[0][1]-1+1][move[0][0]+1] = self.Turn
				elif move[1] == "R":
					self.Board[move[0][1]+1][move[0][0]+1] = 0
					self.Board[move[0][1]-1+1][move[0][0]+1+1] = self.Turn
				elif move[1] == "L":
					self.Board[move[0][1]+1][move[0][0]+1] = 0
					self.Board[move[0][1]-1+1][move[0][0]-1+1] = self.Turn
				if self.Should_pause:
					self.turn_pause = Pause(15)
				else:
					self.turn_pause = Pause(0)
		elif self.moved and self.turn_pause.Update():
			self.moved = False
			if self.Win():
				self.win = True
				self.Players[self.Turn][0].End(True)
				self.Players[self.Turn*-1][0].End(False)
			elif self.StalemateCheck():
				##CHANGED IN RULE CHANGE
				self.win = True
				self.Players[self.Turn][0].End(True)	#True for normal win
				self.Players[self.Turn*-1][0].End(False)
			self.Board = self.Reflect(x=True, y=True)
			self.Turn = self.Turn*-1
			self.Turn_count -= 1
	

	def ValidateMove(self, move:tuple, board) -> bool:
		pawn_type = board[move[0][1]+1][move[0][0]+1]
		if move[1] == "M":
			if board[move[0][1]-1 +1][move[0][0] +1] == 0:
				return True
		elif move[1] == "R":
			if board[move[0][1]-1 +1][move[0][0]+1 +1] == pawn_type*-1:
				return True
		elif move[1] == "L":
			if board[move[0][1]-1 +1][move[0][0]-1 +1] == pawn_type*-1:
				return True
		return False
	
	def Win(self) -> bool:
		#1
		if self.Turn in self.Board[1]:
			# print(f"Border win by {'Red' if self.Turn == -1 else 'Black'}")
			return True
		#2
		surviver = True
		for layer in self.Board:
			if self.Turn*-1 in layer:
				surviver = False
				break
		if surviver:
			return True

	def StalemateCheck(self):
		board = self.Reflect(x=True, y=True)
		Stalemate = True
		for y in range(len(board)-2):
			for x in range(len(board[0])-2):
				if board[y+1][x+1] == self.Turn*-1:
					for m in ("L","M","R"):
						if self.ValidateMove(((x,y),m), board):
							Stalemate = False
							break
		# if Stalemate:
		# 	print(f"Stalemate win for {'Red' if self.Turn == -1 else 'Black'}")
		return Stalemate
	
	def Resign(self):
		self.win = True
		self.Players[self.Turn][0].End(False)
		self.Players[self.Turn*-1][0].End(True)

	def Reflect(self, x=False, y=False):
		ref_board = copy.deepcopy(self.Board)
		temp_board = copy.deepcopy(self.Board)
		#X-axsis reflection
		if x and y:
			for y in range(len(self.Board)):
				for x in range(len(self.Board[0])):
					rev_x = abs(x-(len(self.Board[0])-1))
					rev_y = abs(y-(len(self.Board)-1))
					ref_board[rev_y][rev_x] = self.Board[y][x]
		elif x:
			for y in range(len(self.Board)):
				for x in range(len(self.Board[0])):
					rev_y = abs(y-(len(self.Board)-1))
					ref_board[rev_y][x] = self.Board[y][x]
		#Y-axsis reflection
		elif y:
			for y in range(len(self.Board)):
				for x in range(len(self.Board[0])):
					rev_x = abs(x-(len(self.Board[0])-1))
					ref_board[y][rev_x] = self.Board[y][x]
		return ref_board
		
		# return temp_board

	def NewGame(self):
		return self.win
	
	def ShowWinner(self, screen, font):
		if self.win:
			screen.fill((255,255,255))
			if self.Turn == 1:
				text = "Red wins!"
				text_obj = font.render(text, True, (255,0,0))
			else:
				text = "Black wins!"
				text_obj = font.render(text, True, (0,0,0))
			screen.blit(text_obj, ((SCREEN_WIDTH-text_obj.get_width())//2,(SCREEN_HEIGHT-text_obj.get_height())//2))

#            if self.Should_pause:
#                self.turn_pause = Pause(1)
#            else:
#                self.turn_pause = Pause(1)

class Pause():
	def __init__(self, T_tick:int):
		self.Total_ticks = T_tick
		self.ticks = 0
	
	def Update(self):
		self.ticks += 1
		if self.ticks >= self.Total_ticks:
			return True
		return False