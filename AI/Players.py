import Table
import pygame
from random import randint
from GLOBALS import *

class Human():
    def __init__(self, scrn):
        self.screen = scrn
        self.board = None

    def setup(self, board_obj:Table.Board):
        self.game = board_obj

    def Play(self, board):
        self.board = board

    def Draw(self):
        if self.board != None:
            size = self.game.Size
            grid_space = (int(SCREEN_WIDTH/size[0]),int(SCREEN_HEIGHT/size[1]))
            ##Grid
            for y in range(size[1]-1):
                y_pos = grid_space[1]*(y+1)
                pygame.draw.line(self.screen, (255,255,0),(0,y_pos), (SCREEN_WIDTH,y_pos))
            for x in range(size[0]-1):
                x_pos = grid_space[0]*(x+1)
                pygame.draw.line(self.screen, (255,255,0),(x_pos,0), (x_pos, SCREEN_WIDTH))

            ##Dots
            for y in range(size[1]):
                for x in range(size[0]):
                    dot = self.board[y][x]
                    pos = (x*grid_space[0]+grid_space[0]//2, y*grid_space[1]+grid_space[1]//2)
                    if dot == 1:
                        pygame.draw.circle(self.screen, (0,0,255), center=pos, radius=grid_space[1]//2 -4)
                    elif dot == -1:
                        pygame.draw.circle(self.screen, (255,0,0), center=pos, radius=grid_space[1]//2 -4)

class AI():
    def __init__(self):
        self.Moves = {}
        #In totaal moet daar 48 wees↓
        #2
        self.Moves[(1,0,1,0,1,0,-1,-1,-1)] = [[(0,2),"M", 1], [(0,2),"R",1], [(2,2),"M",1], [(2,2),"L",1]]
        self.Moves[(1,1,0,0,0,1,-1,-1,-1)] = [[(0,2),"M", 1], [(1,2),"M",1], [(1,2),"R",1]]
        self.Moves[(0,1,1,1,0,0,-1,-1,-1)] = [[(1,2),"M", 1], [(1,2),"L",1], [(2,2),"M",1]]
        #4
        self.Moves[(1,0,0,0,1,0,0,-1,-1)] = [[(2,2),"M",1], [(2,2),"L",1]]
        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] = [[(2,2),"L",1], [(1,2),"R",1]]
        self.Moves[(1,0,0,0,-1,1,0,-1,-1)] = [[(1,2),"R",1], [(1,1),"L",1], [(1,1),"M",1]]
        self.Moves[(0,0,1,1,0,1,-1,-1,0)] = [[(1,2),"M",1], [(1,2),"R",1], [(1,2),"L",1]]
        self.Moves[(0,0,1,1,0,0,-1,0,-1)] = [[(2,2),"M",1]]
#        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] =
#        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] =
#        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] =
#        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] =
#        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] =
#        self.Moves[(1,0,0,-1,1,1,0,-1,-1)] =




#                   0,0 | 1,0 | 2,0
#                   ----|-----|----
#                   0,1 | 1,1 | 2,1
#                   ----|-----|----
#                   0,2 | 1,2 | 2,2 







    def setup(self, board_obj):
        self.game = board_obj
    
    def Play(self, board):
        board_state = ()
        for y in board:
            board_state = board_state + tuple(y)
        move = self.Moves[board_state]
        bowl = []
        for m in move:
            for count in range(m[2]):
                bowl.append(m)
        return bowl[randint(0,len(bowl)-1)]
