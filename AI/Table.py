import copy

class Board():
    def __init__(self, Plrs:list, Board_size):
        self.Players = {}
        self.Players[1] = Plrs[0]
        self.Players[-1] = Plrs[1]
        
        self.Turn = 1

        self.Size = Board_size

        self.Board = []
        for y in range(Board_size[1]):
            self.Board.append([])
            for x in range(Board_size[0]):
                self.Board[y].append(0)
        self.Board = [[3,3,3,3,3],
                      [3,-1,-1,-1,3],
                      [3,0,0,0,3],
                      [3,1,1,1,3],
                      [3,3,3,3,3]]
    

    def Update(self):
        Current_plr = self.Players[self.Turn]
        move = Current_plr.Play(self.Board, self.Turn)
        if move != None:
            if move[1] == "M":
                self.Board[move[0][1]+1][move[0][0]+1] = 0
                self.Board[move[0][1]-1+1][move[0][0]+1] = self.Turn
            elif move[1] == "R":
                self.Board[move[0][1]+1][move[0][0]+1] = 0
                self.Board[move[0][1]-1+1][move[0][0]+1] = self.Turn
            elif move[1] == "L":
                self.Board[move[0][1]+1][move[0][0]+1] = 0
                self.Board[move[0][1]-1+1][move[0][0]-1+1] = self.Turn
            self.Turn = self.Turn*-1
            self.Rotate()
    

    def ValidateMove(self, move:list) -> bool:
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
    

    def Rotate(self):
        temp_board = copy.deepcopy(self.Board)
        for y in range(len(self.Board)):
            for x in range(len(self.Board[0])):
                rev_x = abs(x-(len(self.Board[0])-1))
                rev_y = abs(y-(len(self.Board)-1))
                self.Board[y][x] = temp_board[rev_y][rev_x]