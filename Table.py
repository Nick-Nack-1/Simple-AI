import copy


class Board():
    def __init__(self, Plrs:list, Board_size):
        self.Players = {}
        self.Players[1] = [Plrs[0],0]
        self.Players[-1] = [Plrs[1],0]
        
        self.Turn = 1
        self.moved = False
        self.turn_pause = None
        self.win = False

        self.Size = Board_size

        self.Board = []
        self.Board = [[3,3,3,3,3],
                      [3,-1,-1,-1,3],
                      [3,0,0,0,3],
                      [3,1,1,1,3],
                      [3,3,3,3,3]]
    

    def Update(self):
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
                self.turn_pause = Pause(15)
        elif self.moved and self.turn_pause.Update():
            self.moved = False
            win = self.Win()
            if win:
                self.win = True
                self.Players[self.Turn][0].End(True)
                self.Players[self.Turn*-1][0].End(False)
            self.Turn = self.Turn*-1
            self.Rotate()
    

    def ValidateMove(self, move:tuple) -> bool:
        if move[1] == "M":
            if self.Board[move[0][1]-1 +1][move[0][0] +1] == 0:
                return True
        elif move[1] == "R":
            if self.Board[move[0][1]-1 +1][move[0][0]+1 +1] == self.Turn*-1:
                return True
        elif move[1] == "L":
            if self.Board[move[0][1]-1 +1][move[0][0]-1 +1] == self.Turn*-1:
                return True
        return False
    
    def Win(self) -> bool:
        #1
        if self.Turn in self.Board[1]:
            return True
        surviver = True
        for layer in self.Board:
            if self.Turn*-1 in layer:
                surviver = False
                break
        #2
        if surviver:
            return True
        #3
        Stalemate = True
        for y in range(len(self.Board)-2):
            for x in range(len(self.Board[0])-2):
                if self.Board[y+1][x+1] == self.Turn:
                    for m in ("L","M","R"):
                        if self.ValidateMove(((x,y),m)):
                            Stalemate = False
        return Stalemate



    def Rotate(self):
        temp_board = copy.deepcopy(self.Board)
        for y in range(len(self.Board)):
            for x in range(len(self.Board[0])):
                rev_x = abs(x-(len(self.Board[0])-1))
                rev_y = abs(y-(len(self.Board)-1))
                temp_board[rev_y][rev_x] = self.Board[y][x]
        self.Board = temp_board
    

    def NewGame(self):
        return self.win


class Pause():
    def __init__(self, T_tick:int):
        self.Total_ticks = T_tick
        self.ticks = 0
    
    def Update(self):
        self.ticks += 1
        if self.ticks >= self.Total_ticks:
            return True
        return False