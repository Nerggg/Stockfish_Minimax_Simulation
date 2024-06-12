# Stockfish Minimax Simulation

A simple Minimax simulation using Depth First Search made with Python in the purpose of fulfilling the **IF2211 Strategi Algoritma** paper assignment.

## How to Use
Please note that you need Python to be able to run this program

1. Clone the repository and navigate to the repository folder
    ```
    git clone https://github.com/Nerggg/Stockfish_Minimax_Simulation
    cd Stockfish_Minimax_Simulation
    ```
2. Install the Stockfish library for Python
    ```
    pip install stockfish
    ```
2. Download Stockfish binary file from [their offical website](https://stockfishchess.org/download/) then extract it into `Stockfish_Minimax_Simulation/`
3. If your Stockfish version is newer than 16.1, You may need to adjust the version of Stockfish used in the source code
3. Change the `fen` variable into the FEN Notation of a position you want to calculate 
4. Run the program using this command
    ```
    python3 main.py
    ```
5. OR if you want to calculate the minimax tree of a certain position, uncomment this part of code
    ``` py
    # stockfish = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe")
    # stockfish.set_fen_position(fen)
    # root = Node(stockfish, [])
    # root.make_tree(3, 2) # depth, child_count
    # bfs_print(root)
    # move = minimax(root, 3, True).move
    # print(move)
    # stockfish.make_moves_from_current_position([move[0]])
    # print(stockfish.get_fen_position())
    ```
    and comment this part
    ``` py
    white = False # use True if white is to play the turn
    while True:
        stockfish = Stockfish(path="./stockfish/stockfish-windows-x86-64-avx2.exe")
        stockfish.set_fen_position(fen)
        root = Node(stockfish, [])
        root.make_tree(3, 2) # depth, child count
        move = minimax(root, 3, white).move
        stockfish.make_moves_from_current_position([move[0]])
        print(print_board(stockfish))
        print(move)
        fen = stockfish.get_fen_position()
        print(fen)

        if white:
            white = False
        else:
            white = True

        if (is_game_over(stockfish)):
            print("game over :D")
            break
    ```
    then run like usual.  
    You can check the calculation for each node in the generated txt files. The numbering will follow the usual BFS node traversing.

## Demo
https://github.com/Nerggg/Stockfish_Minimax_Simulation/assets/118040364/4db6e4dd-889f-4018-9aef-55dea068caf3
