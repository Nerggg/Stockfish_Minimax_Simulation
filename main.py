from stockfish import Stockfish
from collections import deque

filename = 1

class Node:
    def __init__(self, sf, move):
        self.child = []
        self.sf = sf
        self.move = move
        self.eval = sf.get_evaluation()

    def add_child(self, n):
        self.child.append(n)

    def write_to_file(self):
        global filename
        fen_to_ascii = {
        'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
        'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
        }
        
        if (filename < 10):
            with open ('0' + str(filename) + ".txt", 'w') as file:
                board = self.sf.get_board_visual()
                ascii_board = ""
                for i in range (len(board)):
                    if i + 31 >= len(board):
                        ascii_board += board[i]
                    else:
                        ascii_board += fen_to_ascii.get(board[i], board[i])
                file.write(ascii_board)
                for move in self.move:
                    file.write(move + ' ')
                file.write('\n')
                file.write(self.eval['type'])
                file.write('\n')
                file.write(str(self.eval['value']))
                file.write('\n')
            filename += 1
        else:
            with open (str(filename) + ".txt", 'w') as file:
                board = self.sf.get_board_visual()
                ascii_board = ""
                for i in range (len(board)):
                    if i + 31 >= len(board):
                        ascii_board += board[i]
                    else:
                        ascii_board += fen_to_ascii.get(board[i], board[i])
                file.write(ascii_board)
                for move in self.move:
                    file.write(move + ' ')
                file.write('\n')
                file.write(self.eval['type'])
                file.write('\n')
                file.write(str(self.eval['value']))
                file.write('\n')
            filename += 1

    def make_tree(self, depth, child_count):
        if (depth == 0):
            return
        
        moves = self.sf.get_top_moves(child_count)
        for move in moves:
            new_sf = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe")
            new_sf.set_fen_position(self.sf.get_fen_position())
            new_sf.make_moves_from_current_position([move['Move']])
            # print(new_sf.get_fen_position())
            move_temp = self.move.copy()
            move_temp.append(move['Move'])
            child = Node(new_sf, move_temp)
            self.add_child(child)
            # print(child.move)
            child.make_tree(depth-1, child_count)
            del move_temp

def minimax(node, depth, maximizing):
    if depth == 0 or len(node.child) == 0:
        return node
    
    if maximizing: # white turn
        if node.eval['type'] == 'cp' or (node.eval['type'] == 'mate' and node.eval['value'] < 0):
            extreme_node = minimax(node.child[0], depth-1, False)
            for i in range (1, len(node.child)):
                minimax_node = minimax(node.child[i], depth-1, False)
                if (minimax_node.eval['value'] > extreme_node.eval['value']):
                    extreme_node = minimax_node
        else:
            extreme_node = minimax(node.child[0], depth-1, True)
            for i in range (1, len(node.child)):
                minimax_node = minimax(node.child[i], depth-1, True)
                if (minimax_node.eval['value'] < extreme_node.eval['value']):
                    extreme_node = minimax_node
    else: # black turn
        if node.eval['type'] == 'cp' or (node.eval['type'] == 'mate' and node.eval['value'] > 0):
            extreme_node = minimax(node.child[0], depth-1, False)
            for i in range (1, len(node.child)):
                minimax_node = minimax(node.child[i], depth-1, False)
                if (minimax_node.eval['value'] < extreme_node.eval['value']):
                    extreme_node = minimax_node
        else:
            extreme_node = minimax(node.child[0], depth-1, True)
            for i in range (1, len(node.child)):
                minimax_node = minimax(node.child[i], depth-1, True)
                if (minimax_node.eval['value'] > extreme_node.eval['value']):
                    extreme_node = minimax_node
    # print("yg di return itu " + str(extreme_node.move) + " dengan value " + str(extreme_node.eval['value']))
    return extreme_node

def delete_tree(root):
    for child in root.child:
        del child
    del root

def bfs_print(root):
    queue = deque([root])

    while queue:
        print(filename)
        node = queue.popleft()
        node.write_to_file()
        print(node.sf.get_fen_position())

        for child in node.child:
            queue.append(child)

def is_game_over(sf):
    info = sf.get_evaluation()
    return (info['type'] == 'mate' and info['value'] == 0)

def make_move(move):
    if stockfish.is_move_correct(move):
        stockfish.make_moves_from_current_position([move])
        return True
    return False

def print_board(sf):
    fen_to_ascii = {
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
    }
    board = sf.get_board_visual()
    ascii_board = ""
    for i in range (len(board)):
        if i + 31 >= len(board):
            ascii_board += board[i]
        else:
            ascii_board += fen_to_ascii.get(board[i], board[i])
    return ascii_board

# fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen = "4K3/4P1k1/8/8/8/8/7R/5r2 b - - 0 1"

# SINGLE PRINTING
# root = Node(stockfish, [])
# root.make_tree(3, 2) # depth, child_count
# bfs_print(root)
# print(minimax(root, 3, False).move)

# MAIN GAME
white = False
while True:
    stockfish = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe") # depth defaultnya 15
    stockfish.set_fen_position(fen)
    root = Node(stockfish, [])
    root.make_tree(3, 2)
    stockfish.make_moves_from_current_position([minimax(root, 3, white).move[0]])
    print(print_board(stockfish))
    fen = stockfish.get_fen_position()
    print(fen)

    if white:
        white = False
    else:
        white = True

    if (is_game_over(stockfish)):
        print("game over :D")
        break