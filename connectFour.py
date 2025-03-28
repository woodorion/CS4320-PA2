# Alan Robles ID: 80647127
import sys
import random

def main():
    # Checking the command line arguments using the argv functions
    # to make sure there is a total of 4, nothing less and nothing more 
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
        board = lines[2:8]  
        if len(board) != 6:
            raise ValueError("You need 6 rows for the board.")
    except Exception as e:
        print(f"Not reading file: {e}")
        sys.exit(1)
    
    # Start array with nothing to check allowed moves; 
    # if it is zero then its illegal
    allowedMoves = []
    try:
        # Travel through the columns to check for allowed moves
        for col in range(7): 
            # If 0 then its not allowed  
            if board[0][col] == 'O':
                allowedMoves.append(col + 1)  
    except Exception as e:
        print(f"Not able to travel through array: {e}")
        sys.exit(1)
    
    # Check for errors if there is an index issue
    if not allowedMoves:
        print("Index issue moves not allowed.")
        sys.exit(1)
    
    # Use the UR algorithm
    try:
        # random choice to check for a random number
        chosen_move = random.choice(allowedMoves)
    except Exception as e:
        print(f"selected move error: {e}")
        sys.exit(1)
    
    print(f"Final Move : {chosen_move}")

if __name__ == "__main__":
    main()
