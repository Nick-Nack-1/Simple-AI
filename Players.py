import Table
import pygame
import Inputs
from random import randint
from GLOBALS import *

class Human():
    def __init__(self, scrn, inp:Inputs.Input_events, mouse:Inputs.Mouse):
        self.screen = scrn
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
                if self.game.ValidateMove(move):
                    self.select_pos = None
                    return move
        return None

    def Draw(self):
        if self.board != None:
            size = (len(self.game.Board[0]),len(self.game.Board))
            grid_space = (int(SCREEN_WIDTH/(size[0]-2)),int(SCREEN_HEIGHT/(size[1]-2)))
            ##Grid
            for y in range(size[1]-3):
                y_pos = grid_space[1]*(y+1)
                pygame.draw.line(self.screen, ((128,128,128)),(0,y_pos), (SCREEN_WIDTH,y_pos),width=3)
            for x in range(size[0]-3):
                x_pos = grid_space[0]*(x+1)
                pygame.draw.line(self.screen, ((128,128,128)),(x_pos,0), (x_pos, SCREEN_WIDTH),width=3)

            ##Dots
            for y in range(size[1]-2):
                for x in range(size[0]-2):
                    dot = self.board[y+1][x+1]
                    pos = (x*grid_space[0]+grid_space[0]//2, y*grid_space[1]+grid_space[1]//2)
                    if dot == 1:
                        pygame.draw.circle(self.screen, (0,0,0), center=pos, radius=grid_space[1]//2 -4)
                    elif dot == -1:
                        pygame.draw.circle(self.screen, (255,0,0), center=pos, radius=grid_space[1]//2 -4)
    def End(self, win:bool):
        if win:
            self.score += 1

class AI():
    def __init__(self):
        self.last_move = None
        self.score = 0
        self.Moves = {}
        #In totaal moet daar 37 wees↓  (nie 48 want daar is twee wat dieselfde is)(-8 vir simmetriese enes by 6)(-2 vir simmetriese enes by 4)
        #2 (3)
        self.Moves[(1,0,1,0,1,0,-1,-1,-1)] = [[(0,2),"M", 1], [(0,2),"R",1], [(2,2),"M",1], [(2,2),"L",1]]#eintlik 2 boksies(hul is simmetries selfs gerotate)
        self.Moves[(1,1,0,0,0,1,-1,-1,-1)] = [[(0,2),"M", 1], [(1,2),"M",1], [(1,2),"R",1]]
        self.Moves[(0,1,1,1,0,0,-1,-1,-1)] = [[(1,2),"M", 1], [(1,2),"L",1], [(2,2),"M",1]]
        #4 (20)
        self.Moves[(1,0,0,0,1,0,0,-1,-1)] = [[(2,2),"M",1], [(2,2),"L",1]]
        self.Moves[(1,0,0,0,-1,1,0,-1,-1)] = [[(1,2),"R",1], [(1,1),"L",1], [(1,1),"M",1]]
        self.Moves[(0,0,1,1,0,1,-1,-1,0)] = [[(1,2),"M",1], [(1,2),"R",1], [(1,2),"L",1]]
        self.Moves[(0,0,1,1,0,0,-1,0,-1)] = [[(2,2),"M",1]]
        self.Moves[(0,1,0,1,1,0,-1,0,-1)] = [[(0,2),"R",1], [(2,2),"M",1], [(2,2),"L",1]]
        self.Moves[(0,0,1,1,-1,0,0,-1,-1)] = [[(1,1),"M",1], [(1,1),"R",1], [(2,2),"M",1], [(1,2),"L",1]]
        self.Moves[(0,0,1,0,1,0,0,-1,-1)] = [[(2,2),"M",1], [(2,2),"L",1]]
        self.Moves[(0,0,1,-1,1,0,-1,0,-1)] = [[(0,1),"M",1], [(0,2),"R",1], [(2,2),"M",1], [(2,2),"L",1]] 
        self.Moves[(0,1,0,-1,0,1,-1,0,-1)] = [[(0,1),"M",1],[(0,1),"R",1]]
        self.Moves[(0,0,1,0,1,0,-1,-1,0)] = [[(0,2),"M",1],[(0,2),"R",1]]  #4.2
        self.Moves[(0,1,0,1,0,-1,-1,0,-1)] = [[(2,1),"M",1],[(2,1),"L",1]]
        self.Moves[(1,0,0,0,1,-1,-1,0,-1)] = [[(2,1),"M",1],[(0,2),"M",1],[(0,2),"R",1],[(2,2),"L",1]]
        self.Moves[(1,0,0,0,1,0,-1,-1,0)] = [[(0,2),"M",1],[(0,2),"R",1]]
        self.Moves[(1,0,0,0,-1,1,-1,-1,0)] = [[(1,1),"M",1],[(1,1),"L",1],[(0,2),"M",1],[(1,2),"R",1]]
        self.Moves[(0,1,0,0,1,1,-1,0,-1)] = [[(0,2),"M",1],[(0,2),"R",1],[(2,2),"L",1]]
        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] = [[(1,2),"R",1],[(2,2),"L",1]]
        self.Moves[(1,0,0,0,0,1,-1,0,-1)] = [[(0,2),"M",1]]
        self.Moves[(1,0,0,1,0,1,0,-1,-1)] = [[(1,2),"M",1],[(1,2),"L",1],[(1,2),"R",1]]
        self.Moves[(0,0,1,1,-1,0,-1,-1,0)] = [[(1,1),"M",1],[(1,1),"R",1],[(1,2),"L",1]]
        self.Moves[(0,0,1,1,1,-1,-1,-1,0)] = [[(0,2),"R",1],[(1,2),"L",1]]
        #6 (14)
        self.Moves[(0,0,0,1,1,1,-1,0,0)] = [[(0,2),"R",1]]
        self.Moves[(0,0,0,-1,1,0,0,0,-1)] = [[(0,1),"M",1],[(2,2),"M",1],[(2,2),"L",1]]
        self.Moves[(0,0,0,-1,-1,1,0,0,-1)] = [[(0,1),"M",1],[(1,1),"M",1]]
        self.Moves[(0,0,0,1,-1,0,0,-1,0)] = [[(1,1),"M",1],[(1,2),"L",1]]
        self.Moves[(0,0,0,1,-1,-1,-1,0,0)] = [[(1,1),"M",1],[(2,1),"M",1]]
        self.Moves[(0,0,0,-1,1,1,0,-1,0)] = [[(0,1),"M",1],[(1,2),"R",1]]
        self.Moves[(0,0,0,-1,1,0,-1,0,0)] = [[(0,1),"M",1],[(0,2),"R",1]]
        self.Moves[(0,0,0,0,1,-1,-1,0,0)] = [[(2,1),"M",1],[(0,2),"M",1],[(0,2),"R",1]]
        self.Moves[(0,0,0,0,-1,1,0,-1,0)] = [[(1,1),"M",1],[(1,2),"R",1]]
        self.Moves[(0,0,0,-1,-1,1,-1,0,0)] = [[(0,1),"M",1],[(1,1),"M",1]]
        self.Moves[(0,0,0,1,1,1,0,0,-1)] = [[(2,2),"L",1]]
        self.Moves[(0,0,0,1,-1,-1,0,0,-1)] = [[(1,1),"M",1],[(2,1),"M",1]]
        self.Moves[(0,0,0,0,1,-1,0,0,-1)] = [[(2,1),"M",1],[(2,2),"L",1]]
        self.Moves[(0,0,0,1,1,-1,0,-1,0)] = [[(2,1),"M",1],[(1,2),"L",1]]
        
    def setup(self, board_obj):
        self.game = board_obj
    
    def GetBoard(self, board):
        self.board = board
    
    def Play(self, board, plr_key:int) -> list|None:
        board_state = ()
        for y in range(len(board)-2):
            board_state = board_state + tuple(board[y+1][1:4])
        move = self.Moves[board_state]
        bowl = []
        for m in move:
            for count in range(m[2]):
                bowl.append(m)
        if bowl == []:
            self.last_move[2] = 0
            self.game.Resign()
            return
        else:
            self.last_move = bowl[randint(0,len(bowl)-1)]
            return self.last_move[0:2]
    
    def End(self, win:bool):
        if win:
            self.score += 1
            self.last_move[2] += 1
        else:
            self.last_move[2] -= 1

            
