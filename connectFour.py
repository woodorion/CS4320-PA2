# Alan Robles ID: 80647127
# Orion Wood ID: 80537518
# Jesus Ortega ID: 80421772 
import sys
import random
import math

def gameSetup(gameBoard):
    if len(gameBoard) != 6:
        raise ValueError("You need 6 rows for the board")
    # Check the top row for empty spaces.
    allowedMoves = [col for col in range(7) if gameBoard[0][col] == 'O']
    # Simply return the list, even if it is empty.
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
            if verbosity == "Verbose":
                print("Game Over: No Winner")
            if simYN and verbosity == "Verbose":
                print("TERMINAL NODE VALUE: 0")
            return 0    #Game is over, no winner
        
        chosen_move = random.choice(allowedMoves) #Chooses random valid move 

        #find row of the piece that was placed, will be none if invalid
        row = dropPiece(gameBoard, chosen_move, current_player)  # Drop the piece in the chosen column

        if row is not None:  # If the piece was placed successfully
            if winLogic(gameBoard, row, chosen_move, current_player):     #checks if there is a 4 in a row for the current player
                if verbosity != "None" and not simYN:
                    print(f"FINAL Move Selected: {chosen_move + 1}")
                    print(f"Player {current_player} wins!")
                    printBoard(gameBoard)
                if simYN and verbosity == "Verbose":
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
    best_move = max(moveStats, key=lambda col: (moveStats[col]["wi"] / moveStats[col]["ni"]) if moveStats[col]["ni"] > 0 else -float('inf'))
    if verbosity != "None":
        for col in range(7):
            if moveStats[col]["ni"] > 0:
                value = moveStats[col]["wi"] / moveStats[col]["ni"]
                print(f"Column {col+1}: {value:.2f}")
            else:
                print(f"Column {col+1}: Null")
        print(f"FINAL Move selected: {best_move + 1}")
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
    best_move = max(moveStats, key=lambda col: (moveStats[col]["wi"] / moveStats[col]["ni"]) if moveStats[col]["ni"] > 0 else -float('inf'))

    if verbosity != "None":
        for col in range(7):
            if moveStats[col]["ni"] > 0:
                value = moveStats[col]["wi"] / moveStats[col]["ni"]
                print(f"Column {col+1}: {value:.2f}")
            else:
                print(f"Column {col+1}: Null")
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
    # Now returns row of the placed piece, to be used in winLogic()

    # Start checking from the bottom row to the top
    for row in reversed(range(6)):
        if board[row][col] == 'O':  # Check for an empty spot
            board[row][col] = symbol  # Place the piece in the lowest empty spot, simulating a "drop"
            return row
    return None  # Column is full
 
def winLogic(board, row, col, symbol):
    #checks around the piece placed to see if there is a 4 in a row
    #check horizontal lines
    count = 0
    for c in range(max(col -3, 0), min(col + 4, 7)):    #c for column
        count = count + 1 if board[row][c] == symbol else 0
        if count == 4:
            return True
    #check vertical lines
    count = 0 #resest count after each check
    for r in range(max(row-3, 0), min(row + 4, 6)):   #r for row
        count = count + 1 if board[r][col] == symbol else 0
        if count == 4:
            return True
    #check diagonal lines (\)
    count = 0
    for d in range(-3,4):   #d for diagonal
        r, c = row + d, col + d
        if 0 <= r < 6 and 0 <= c < 7:
            count = count + 1 if board[r][c] == symbol else 0
            if count == 4:
                return True
        else:
            count = 0
    #check diagonal lines (/)
    count = 0
    for b in range(-3,4):   #b for anti-diagonal (b => d backwards)
        r, c = row -b, col + b
        if 0 <= r < 6 and 0 <= c < 7:
            count = count + 1 if board[r][c] == symbol else 0
            if count == 4:
                return True
        else:
            count = 0
    return False  #if none found, return false

def selectMoveUR(gameBoard, current_player):
    
    allowedMoves = gameSetup(gameBoard)
    return random.choice(allowedMoves)

def get_move(algo, board, current_player, param, verbosity):
    if algo == "UR":
        return selectMoveUR(board, current_player)
    elif algo == "PMCGS":
        return PMCGS_Algorithm(current_player, board, verbosity, param)
    elif algo == "UCT":
        return UCT_Algorithm(current_player, board, verbosity, param)
    else:
        raise ValueError("Unknown algorithm specified.")

def simulate_game(algo_row, param_row, algo_col, param_col, starting_first):
    # Initialize an empty Connect Four board (6 rows x 7 columns)
    board = [['O'] * 7 for _ in range(6)]
    
    # Assign symbols based on who starts first.
    if starting_first == "row":
        symbol_for_row = 'R'
        symbol_for_col = 'Y'
    else:
        symbol_for_row = 'Y'
        symbol_for_col = 'R'
    
    current_player = 'R'  # 'R' always moves first in our simulation
    while True:
        # Check for draw: if no allowed moves (i.e., board full)
        if not gameSetup(board):
            return "draw"
        
        if current_player == 'R':
            # Determine which algorithm is playing as 'R'
            if symbol_for_row == 'R':
                move = get_move(algo_row, board, current_player, param_row, "None")
            else:
                move = get_move(algo_col, board, current_player, param_col, "None")
        else:  # current_player == 'Y'
            if symbol_for_row == 'Y':
                move = get_move(algo_row, board, current_player, param_row, "None")
            else:
                move = get_move(algo_col, board, current_player, param_col, "None")
        
        # Place the piece and check for a win.
        row_index = dropPiece(board, move, current_player)
        if row_index is None:
            # This should not happen if moves are legal.
            return "draw"
        if winLogic(board, row_index, move, current_player):
            # Return who won based on the symbol.
            if current_player == symbol_for_row:
                return "row"
            else:
                return "col"
        # Alternate player
        current_player = 'Y' if current_player == 'R' else 'R'

def tournament():
    # Each algorithm with the number of simulation for the tournament
    variants = [
        ("UR", None, "UR"),
        ("PMCGS", 500, "PMCGS(500)"),
        ("PMCGS", 1000, "PMCGS(10000)"),
        ("UCT", 500, "UCT(500)"),
        ("UCT", 1000, "UCT(10000)")
    ]
    num_games = 100
    results = [[0 for _ in range(len(variants))] for _ in range(len(variants))]
    
    # Run the tournament games.
    for i, (algo_row, param_row, label_row) in enumerate(variants):
        for j, (algo_col, param_col, label_col) in enumerate(variants):
            row_wins = 0
            for game in range(num_games):
                # Alternate starting order for fairness.
                starting_first = "row" if game % 2 == 0 else "col"
                outcome = simulate_game(algo_row, param_row, algo_col, param_col, starting_first)
                if outcome == "row":
                    row_wins += 1
            win_percentage = (row_wins / num_games) * 100
            results[i][j] = win_percentage

    # Create headers.
    header = ["Row\\Col"] + [variant[2] for variant in variants]
    # Determine a fixed column width based on the longest header.
    col_width = max(len(cell) for cell in header) + 4  # add extra space for padding

    # Print the header row with fixed-width columns.
    header_line = "".join(cell.ljust(col_width) for cell in header)
    print(header_line)

    # Print each result row with the row label and aligned percentages.
    for i, row in enumerate(results):
        row_label = variants[i][2]
        row_str = row_label.ljust(col_width)
        for win_pct in row:
            row_str += f"{win_pct:.1f}%".ljust(col_width)
        print(row_str)

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
        # The first line specifies the mode/algorithm.
        algorithm = lines[0]
        # If Tournament mode is specified, run the tournament.
        if algorithm == "Tournament":
            tournament()
        # Otherwise, run a single move/game as before.
        elif algorithm == "UR":
            UR_Algorithm(lines[1], [list(line) for line in lines[2:8]], verbosity, False)
        elif algorithm == "PMCGS":
            PMCGS_Algorithm(lines[1], [list(line) for line in lines[2:8]], verbosity, int(algorithm_param))
        elif algorithm == "UCT":
            UCT_Algorithm(lines[1], [list(line) for line in lines[2:8]], verbosity, int(algorithm_param))
        else:
            raise ValueError(f"Wrong Algorithm: {algorithm}")
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
    
    
    
if __name__ == "__main__":
    main()
