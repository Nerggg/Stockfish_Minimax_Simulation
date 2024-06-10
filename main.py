from stockfish import Stockfish
from collections import deque
import copy

filename = 1

class Node:
    def __init__(self, sf):
        self.child = []
        self.sf = sf
        if (fen.split()[1] == 'w'):
            self.turn = 'w'
        else:
            self.turn = 'b'

    def add_child(self, n):
        self.child.append(n)

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

    def make_tree(self, depth, child_count):
        if (depth == 0):
            return
        
        moves = self.sf.get_top_moves(child_count)
        fen = self.sf.get_fen_position()
        for move in moves:
            new_sf = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe")
            new_sf.set_fen_position(self.sf.get_fen_position())
            new_sf.make_moves_from_current_position([move['Move']])
            print(new_sf.get_fen_position())
            child = Node(new_sf)
            self.add_child(child)
            child.make_tree(depth-1, child_count)

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

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1"
# fen = "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

stockfish = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe", depth=15) # defaultnya emg 15
stockfish.set_fen_position(fen)

root = Node(stockfish)
root.make_tree(2, 2)
print("make tree kelar")
print(root.sf.get_fen_position())
print("ngeprint broh")
bfs_print(root)