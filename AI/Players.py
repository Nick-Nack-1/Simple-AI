
class Human():
    def __init__(self, scrn):
        self.screen = scrn

    def setup(self, board_obj):
        self.game = board_obj

    def Play(self, board):
        pass

class AI():
    def __init__(self):
        self.Moves = {}
        self.Moves[(1,0,1,0,1,0,-1,-1,-1)] = [[(0,2),"M", 1],[(0,2),"R",1]]
    def setup(self, board_obj):
        self.game = board_obj
    
    def Play(self, board):
        board_state = ()
        for y in range(len(board)):
            board_state = board_state + tuple(board)