class AI():
    def __init__(self):
        self.Moves = {}
        self.generate_moves()

    def generate_moves(self):
        for board_state in self.Moves.keys():
            self.Moves[board_state] = self.find_moves(board_state)

    def find_moves(self, board_state):
        moves = []
        board = [list(board_state[i:i+3]) for i in range(0, len(board_state), 3)]
        for y in range(3):
            for x in range(3):
                if board[y][x] == -1:
                    # Move forward
                    if y > 0 and board[y-1][x] == 0:
                        moves.append([(x,y),"M",1])
                    # Capture diagonally left
                    if y > 0 and x > 0 and board[y-1][x-1] == 1:
                        moves.append([(x,y),"L",1])
                    # Capture diagonally right
                    if y > 0 and x < 2 and board[y-1][x+1] == 1:
                        moves.append([(x,y),"R",1])
        return moves

ai = AI()
while True:
    board_state = input("Enter board state in this format: (0,0,0,0,0,0,0,0,0) or type 'q' to exit\n")
    if board_state.lower() == 'q':
        break
    try:
        board_state = tuple(map(int, board_state.strip('()').split(',')))
        print("\n-----------------------------------------------------------------------------------------------")
        print(f"self.Moves[{str(board_state).replace(' ', '')}] = {str(ai.find_moves(board_state)).replace(', ', ',')}")
        print("-----------------------------------------------------------------------------------------------\n")
    except ValueError:
        print("Invalid input format. Please try again.")

