import Table
import pygame
import Inputs
from random import randint
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
        self.Moves = {}
        self.board = None
        
    def setup(self, board_obj):
        self.game = board_obj
    
    def GetBoard(self, board):
        self.board = board
    
    def Play(self, board, plr_key:int) -> list|None:
        board_state = ()
        for y in range(len(board)-2):
            board_state = board_state + tuple(board[y+1][1:-1])

        if board_state not in self.Moves:
            self.Moves[board_state] = []
            for y in range(len(board)-2):
                for x in range(len(board[0])-2):
                    if board[y+1][x+1] == plr_key:
                        for m in ["M","L","R"]:
                            if self.game.ValidateMove(((x,y),m), board):
                                self.Moves[board_state].append([(x,y),m,1])

        move = self.Moves[board_state]
        bowl = []
        for m in move:
            for count in range(m[2]):
                bowl.append(m)
        if len(bowl) == 0:
            self.last_move[2] = 1
            print("Resigning")
            self.last_move = move[randint(0,len(move)-1)]
            return self.last_move[0:2]
    
        else:
            self.last_move = bowl[randint(0,len(bowl)-1)]
            return self.last_move[0:2]
    
    def End(self, win:bool):
        if win:
            self.score += 1
            #self.last_move[2] += 1  #haal die lyn uit vir ai om vinniger te leer
        else:
            if self.last_move[2] > 0:
                self.last_move[2] -= 1

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
            self.last_move = Moves[randint(0,len(Moves)-1)]
            return self.last_move[0:2]
    
    def End(self, win:bool):
        pass

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