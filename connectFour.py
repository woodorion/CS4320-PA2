# Alan Robles ID: 80647127
# Orion Wood ID: 80537518
# Jesus Ortega ID: 80421772 
import sys
import random

#Method to print board, for testing purposes
def printBoard(board):
    for row in board:
        print(' '.join(row))
    print('-' * 15)  # Divider between states

#if valid, drops down piece to proper spot (based on board)
#if not valid, just returns false
#if placed in an if statement, doubles as both dropping down piece to proper place, and verifying placement validity
def dropPiece(board, col, symbol):
    # Start checking from the bottom row to the top
    for row in reversed(range(6)):
        if board[row][col] == 'O':  # Check for an empty spot
            board[row][col] = symbol  # Place the piece in the lowest empty spot, simulating a "drop"
            return True
    return False  # Column is full
 
#checks the entire board every time for possible wins for the current player
#inefficient, but easier to implement than a local search, will likely optimize later
def winLogic(board, symbol):
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
    # For this argument using the UR algorithm we set it to 0
    algorithm_param = sys.argv[3] 

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
        # Check if we are using the UR algorithm
        if algorithm != "UR":
            raise ValueError(f"Wrong Algorithm: {algorithm}")
        # Get the symbol for the currrent player
        current_player = lines[1]
        # Create a board making sure there is only 6 rows
        board = [list(line) for line in lines[2:8]]  
        if len(board) != 6:
            raise ValueError("You need 6 rows for the board.")
    except Exception as e:
        print(f"Not reading file: {e}")
        sys.exit(1)
    
    # Start array with nothing to check allowed moves; 
    # if it is zero then its illegal
    allowedMoves = []
    initialBoard = board
    print("Initial Board:") #print initial board for comparison
    printBoard(initialBoard)
    try:
        # Travel through the columns to check for allowed moves
        allowedMoves = [col for col in range(7) if board[0][col] == 'O']    #If top row is full, column cannot be added to
        if not allowedMoves:
            raise ValueError("No valid moves at onset, board is already full")     #Check for errors if no allowed moves
    except Exception as e:
        print(f"Not able to travel through array: {e}")
        sys.exit(1)
    
    # Check for errors if there is an index issue
    if not allowedMoves:
        print("Index issue moves not allowed.")
        sys.exit(1)
    
    # Use the UR algorithm 
    while True:
        allowedMoves = [col for col in range(7) if board[0][col] == 'O']    #check for allowed moves every move
        if not allowedMoves:
            print("Game Over: No Winner")
            break
        chosen_move = random.choice(allowedMoves) #Chooses random valid move 

        #if selected column is not full (aka piece is dropped down correctly)
        if dropPiece(board, chosen_move, current_player):
            if winLogic(board, current_player):     #checks if there is a 4 in a row for the current player
                print(f"FINAL Move Selected: {chosen_move + 1}")
                print(f"Player {current_player} wins!")
                printBoard(board)
                break
            print(f"Player {current_player} chooses column {chosen_move + 1}")
            #printBoard(board)  #only used for testing purposes
        else:
            print(f"Error Coult not place piece in column {chosen_move + 1}")
        #alternates players (always assumed R if current_player somehow isn't R or Y)
        if current_player == 'R':
            current_player = 'Y'
        else:
            current_player = "R"
if __name__ == "__main__":
    main()

'''
Things done:
    -Initalized from command line, taking in appropriate arguments
    -loads game from text file, as well as starting player
    -plays a game randomly, alternating between the two players (R and Y)
    -correctly (if inefficiently) tests the board for win state, ends game and reports winner once found
        -aka Algorithm 1 works
Things to do:
    Submission 1:
        -Comment and clean up code
            -Maybe get the things from main into methods (necessary for Submission 2)
    Submission 2:
        -Set up Verbose, Brief, None controls
        -Change from UR being only valid, to allowing for the 3 algorithms
        -Algorithm 2: Pure Monte Carlo Game Search (PMCGS)
        -Algorithm 3: Upper Confidence bound for Trees (UCT)
        -Part II: Algorithm Tournaments and Evaluation
        -Report
            -Group Member contributions
            -results from part 2       
'''