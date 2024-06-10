from stockfish import Stockfish
from collections import deque

filename = 1

class Node:
    def __init__(self, sf):
        self.child = []
        self.child_count = 0
        self.sf = sf
        if (fen.split()[1] == 'w'):
            self.turn = 'w'
        else:
            self.turn = 'b'

    def add_child(self, n):
        self.child.append(n)
        self.child_count += 1

    def write_to_file(self):
        global filename
        fen_to_ascii = {
        'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
        'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
        }
        
        with open (str(filename) + ".txt", 'w') as file:
            board = self.sf.get_board_visual()
            ascii_board = ""
            for i in range (len(board)):
                if i + 31 >= len(board):
                    ascii_board += board[i]
                else:
                    ascii_board += fen_to_ascii.get(board[i], board[i])
            evaluation = evaluate(self.sf.get_fen_position())
            file.write(ascii_board)
            file.write(evaluation['type'] + '\n')
            file.write(str(evaluation['value']))
            file.write('\n\n')
        filename += 1

    def make_tree(self, depth):
        if (depth == 0):
            return
        
        moves = self.sf.get_top_moves(2)
        fen = self.sf.get_fen_position()
        for move in moves:
            self.sf.set_fen_position(fen)
            self.sf.make_moves_from_current_position([move['Move']])
            child = Node(self.sf)
            self.add_child(child)
            print(self.sf.get_fen_position())
            child.make_tree(depth-1)

def bfs_print(root):
    queue = deque([root])

    while queue:
        print(filename)
        node = queue.popleft()
        node.write_to_file()
        print(node.sf.get_fen_position())

        for child in node.child:
            queue.append(child)

def evaluate(fen):
    calculator = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe")
    calculator.set_fen_position(fen)
    return calculator.get_evaluation()

stockfish = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe", depth=15) # defaultnya emg 15

def is_game_over():
    info = stockfish.get_evaluation()
    return (info['type'] == 'mate' and info['value'] == 0) or (len(stockfish.get_fen_position()) == 33)

def make_move(move):
    if stockfish.is_move_correct(move):
        stockfish.make_moves_from_current_position([move])
        return True
    return False

def print_board():
    fen_to_ascii = {
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
    }
    board = stockfish.get_board_visual()
    ascii_board = ""
    for i in range (len(board)):
        if i + 31 >= len(board):
            ascii_board += board[i]
        else:
            ascii_board += fen_to_ascii.get(board[i], board[i])
    return ascii_board

# def set_board_position(fen):
#     stockfish.set_fen_position(fen)

# def get_best_moves(n=1):
#     return stockfish.get_top_moves(n)

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1"
# fen = "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


# best_moves = stockfish.get_top_moves(3)
# root = Node(stockfish)
# for move in best_moves:
#     stockfish.set_fen_position(fen)
#     make_move(move['Move'])
#     child = Node(stockfish)
#     root.add_child(child)

# root.write_child_to_file()

# print(print_board())

# make_move(best_moves[0]['Move'])

# print(print_board())

# print((stockfish.get_board_visual()[0]))

# while True:
#     make_move(get_best_moves()[0]['Move'])
#     print(print_board())
#     print(stockfish.get_evaluation())
    
#     if is_game_over():
#         break

root = Node(stockfish)
root.make_tree(2)
print("make tree kelar")
print(root.sf.get_fen_position())
print("ngeprint broh")
bfs_print(root)