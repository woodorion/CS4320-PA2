# Alan Robles ID: 80647127
# Orion Wood ID: 80537518
# Jesus Ortega ID: 80421772 
import sys
import random

def gameSetup(gameBoard):
    #Checks if game is set up correctly, returns initial allowed moves if valid
    if len(gameBoard) != 6:
        raise ValueError("You need 6 rows for the board")
    allowedMoves = []
    try:
        # Travel through the columns to check for allowed moves
        allowedMoves = [col for col in range(7) if gameBoard[0][col] == 'O']    #If top row is full, column cannot be added to
        if not allowedMoves:
            raise ValueError("No valid moves at onset, board is already full")     #Check for errors if no allowed moves
    except Exception as e:
        print(f"Not able to travel through array: {e}")
        sys.exit(1)
    # Check for errors if there is an index issue
    if not allowedMoves:
        print("Index issue moves not allowed.")
        sys.exit(1)
    return allowedMoves

def UR_Algorithm(current_player, gameBoard, verbosity, simYN):
    #Uniform Random Method - takes in the current player, game board, and verbosity level
    #runs through board, till game is over (either win or draw)
    #functionality for if running by itself, as as part of simulation (mainly print statement differences)
    initialPlayer = current_player #Keep track of the starting player, for PMCGS
    allowedMoves = gameSetup(gameBoard)    #Check if game is set up correctly
    
    # Use the UR algorithm 
    while True:
        if not allowedMoves:
            if verbosity != "None":
                print("Game Over: No Winner")
            if simYN and verbosity != "None":
                print("TERMINAL NODE VALUE: 0")
            return 0    #Game is over, no winner
        
        chosen_move = random.choice(allowedMoves) #Chooses random valid move 

        #if selected column is not full (aka piece is dropped down correctly)
        if dropPiece(gameBoard, chosen_move, current_player):
            if winLogic(gameBoard, current_player):     #checks if there is a 4 in a row for the current player
                if verbosity != "None" and not simYN:
                    print(f"FINAL Move Selected: {chosen_move + 1}")
                    print(f"Player {current_player} wins!")
                    printBoard(gameBoard)
                if simYN and verbosity != "None":
                    print(f"TERMINAL NODE VALUE: {1 if current_player == initialPlayer else -1}")
                return 1 if current_player == initialPlayer else -1    #return 1 if original player wins, -1 if other player wins
            if verbosity == "Testing":
                print(f"Player {current_player} chooses column {chosen_move + 1}")
                printBoard(gameBoard)  #only used for testing purposes
            #Update allowed moves for next player, if game is not over
            allowedMoves = [col for col in range(7) if gameBoard[0][col] == 'O']
        else:
            print(f"Error Could not place piece in column {chosen_move + 1}")
        #alternates players (always assumed R if current_player somehow isn't R or Y)
        current_player = 'Y' if current_player == 'R' else 'R'

        if verbosity == "Verbose" and simYN:
            print(f"Move selected: {chosen_move + 1}")

def PMCGS_Algorithm(current_player, gameBoard, verbosity, simulations):
    allowedMoves = gameSetup(gameBoard)    #Check if game is set up correctly
    # Track win and simulation counts for each move
    moveStats = {col: {"wi":0, "ni": 0} for col in range(7)}

    for sim in range (simulations):
        #Select a random valid move to start the simulation
        allowedMoves = [col for col in range(7) if gameBoard[0][col] == 'O']
        if not allowedMoves:
            print("Game Over: No Winner")
            return
        chosen_move = random.choice(allowedMoves)
        if moveStats[chosen_move]["ni"] == 0 and verbosity == "Verbose":
            print("NODE ADDED")

        # Copy the board to simulate the game
        sim_board = [row[:] for row in gameBoard]

        # Drop the initial piece for the current player
        dropPiece(sim_board, chosen_move, current_player)
        # Simulate a game from the chosen move
        result = UR_Algorithm(current_player, sim_board, verbosity, True)  # Run the simulation, randomly

        # Update move statistics
        moveStats[chosen_move]["wi"] += (1 if result == 1 else 0)
        moveStats[chosen_move]["ni"] += 1

        #Verbose output for each simulation
        if verbosity == "Verbose":
            print(f"wi: {moveStats[chosen_move]['wi']}")
            print(f"ni: {moveStats[chosen_move]['ni']}")
            print(f"Move selected: {chosen_move + 1}")
    # Select the move with the highest win rate wi/ni
    best_move = max(moveStats, key=lambda x: (moveStats[x]["wi"] / moveStats[x]["ni"]) if moveStats[x]["ni"] > 0 else -1)

    print(f"Best Move: {best_move + 1}")
    return best_move

def UCT_Algorithm(current_player, gameBoard, verbosity, simulations):
    allowedMoves = gameSetup(gameBoard)
    moveStats = {col: {"wi": 0, "ni": 0} for col in range(7)}
    initial_player = current_player  # store root player
    C = 1.41  # Exploration constant for the algorithm since you use square root of 2

    for sim in range(simulations):
        allowedMoves = [col for col in range(7) if gameBoard[0][col] == 'O']
        if not allowedMoves:
            print("Game Over: No Winner")
            return
        
        # Check if node is not a leaf: all allowed moves have been visited at least once.
        if all(moveStats[col]["ni"] > 0 for col in allowedMoves):
            total_simulations = sum(moveStats[col]["ni"] for col in allowedMoves)
            ucb_values = {}
            for col in allowedMoves:
                ni = moveStats[col]["ni"]
                wi = moveStats[col]["wi"]
                avg_value = wi / ni
                exploration_term = C * math.sqrt(math.log(total_simulations) / ni)
                # Assume that the root player is maximizing.
                ucb = avg_value + exploration_term
                ucb_values[col] = ucb
            if verbosity == "Verbose":
                for col in range(7):
                    if col in ucb_values:
                        print(f"V{col+1}: {ucb_values[col]:.2f}")
                    else:
                        print(f"V{col+1}: Null")
            chosen_move = max(ucb_values, key=ucb_values.get)
            if verbosity == "Verbose":
                print(f"Move selected: {chosen_move + 1}")
        else:
            # If some allowed moves are unvisited, select one at random and indicate a new node.
            chosen_move = random.choice(allowedMoves)
            if moveStats[chosen_move]["ni"] == 0 and verbosity == "Verbose":
                print("NODE ADDED")
        
        # Copy board and simulate from the chosen move.
        sim_board = [row[:] for row in gameBoard]
        dropPiece(sim_board, chosen_move, current_player)
        result = UR_Algorithm(current_player, sim_board, verbosity, True)
        moveStats[chosen_move]["wi"] += (1 if result == 1 else 0)
        moveStats[chosen_move]["ni"] += 1

        if verbosity == "Verbose":
            print("Updated values:")
            print(f"wi: {moveStats[chosen_move]['wi']}")
            print(f"ni: {moveStats[chosen_move]['ni']}")
    
    # After all simulations, select the best move based on the direct estimate (wi/ni)
    for col in range(7):
        if moveStats[col]["ni"] > 0:
            value = moveStats[col]["wi"] / moveStats[col]["ni"]
            print(f"Column {col+1}: {value:.2f}")
        else:
            print(f"Column {col+1}: Null")
    best_move = max(moveStats, key=lambda col: (moveStats[col]["wi"] / moveStats[col]["ni"]) if moveStats[col]["ni"] > 0 else -float('inf'))
    print(f"FINAL Move selected: {best_move + 1}")
    return best_move

def printBoard(board):
    #Method to print board, for testing/reporting purposes
    for row in board:
        print(' '.join(row))
    print('-' * 15)  # Divider between states

def dropPiece(board, col, symbol):
    #if valid, drops down piece to proper spot (based on board)
    #if not valid, just returns false
    #if placed in an if statement, doubles as both dropping down piece to proper place, and verifying placement validity

    # Start checking from the bottom row to the top
    for row in reversed(range(6)):
        if board[row][col] == 'O':  # Check for an empty spot
            board[row][col] = symbol  # Place the piece in the lowest empty spot, simulating a "drop"
            return True
    return False  # Column is full
 
def winLogic(board, symbol):
    #checks the entire board every time for possible wins for the current player
    #inefficient, but easier to implement than a local search, will likely optimize later
    for row in range(6):    #check horizontal lines (L to R)
        for col in range(4):
            if all(board[row][col+i] == symbol for i in range(4)):
                return True
    for col in range(7):    #check vertical lines (T to B)
        for row in range(3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    for row in range(3,6):  #check diagonals (BL to TR)
        for col in range (4):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    for row in range(3,6):  #check other diagonals (BR to TL)
        for col in range(3,7):
            if all(board[row - i][col - i] == symbol for i in range(4)):
                return True
    return False    #if none found, return false

def main():
    # Checking the command line arguments using the argv functions
    # to make sure there is a total of 4, nothing less and nothing more (might be worth having it have default arguements otherwise, but that's extra)
    if len(sys.argv) != 4:
        print("Number of arguments does not match")
        sys.exit(1) # Exit the program 
    
    # For the first argument we need to get the text file
    input_file = sys.argv[1]
    verbosity = sys.argv[2]     
    # Algorithm specific parameter
    algorithm_param = int(sys.argv[3]) 

    # Read the file and handle errors
    try:
        with open(input_file, 'r') as file:
            # Get everything that is not empty from each line
            lines = [line.strip() for line in file if line.strip()]
    except Exception as e:
        # Error if there is not a file or not able to read it
        print(f"Error with this file'{input_file}': {e}")
        sys.exit(1)
    
    try:
        # Get the type of algorithm using the first line from the command line
        algorithm = lines[0]

        # Choose the Algorithm
        if algorithm == "UR":
            UR_Algorithm(lines[1], [list(line) for line in lines[2:8]], verbosity, False)
        elif algorithm == "PMCGS":
            PMCGS_Algorithm(lines[1], [list(line) for line in lines[2:8]], verbosity, algorithm_param)
        elif algorithm == "UCT":
            UCT_Algorithm(lines[1], [list(line) for line in lines[2:8]], verbosity, algorithm_param)   
        else:
            raise ValueError(f"Wrong Algorithm: {algorithm}")
    except Exception as e:
        print(f"Not reading file: {e}")
        sys.exit(1)
    
    
    
if __name__ == "__main__":
    main()
