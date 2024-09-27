class Board:
    # The constructor initializes the game board for a specific player (either player 1 or player 2).
    # The board is a 10x10 grid filled with "~", which represents open water.
    # The `player_num` parameter helps track the board's owner, and the board is represented as a 2D list.
    def __init__(self, player_num):
        self.player_num = player_num  # Store the player number (either player 1 or player 2)
        self.board = [["~" for _ in range(10)] for _ in range(10)]  # Initialize a 10x10 grid filled with "~" (open water)

    # This method displays a key to help players understand the symbols used on the board.
    # It shows the symbol meanings for ships, hits, misses, and open spots.
    def symbol_key(self):
        print("Symbol Key for Battleship: ")
        print(f'\tShip: O\n\tShip hit: X\n\tShip sunk: *\n\tOpen spot: ~\n\tMissfire: .\n')

    # This method displays the current player's own board. It shows the layout of ships and hits/misses.
    # The top row shows column letters (A-J), and each row shows the corresponding row number and ship positions.
    def display_board(self):
        print("Here is your board: ")
        print("  " + " ".join(chr(ord('A') + i) for i in range(10)))  # Print column headers (A-J)
        for i, row in enumerate(self.board):
            # Replace ship integers with "O" to represent ship positions, keeping other symbols unchanged
            formatted_row = ["O" if isinstance(cell, int) else cell for cell in row]
            print(f"{i + 1:2} " + " ".join(formatted_row))  # Print row numbers and the row content

    # This method displays the opponent's board from the player's perspective.
    # The opponent's ships are hidden (shown as "~"), but hits and misses are visible.
    def display_opponent_board(self):
        print("Here is your opponent's board: ")
        print("  " + " ".join(chr(ord('A') + i) for i in range(10)))  # Print column headers (A-J)
        for i, row in enumerate(self.board):
            # Hide ship positions and only show hits, misses, and empty spots
            display_row = ['~' if isinstance(cell, int) else cell for cell in row]
            print(f"{i + 1:2} " + " ".join(display_row))

    # This method checks if a particular board position is empty (i.e., contains a "~").
    # It returns True if the position is open and False otherwise.
    def is_empty(self, row, column):
        return self.board[row][column] == "~"

    # This method checks if a given coordinate is within the bounds of the 10x10 board.
    # It returns True if the row and column are within the valid range (0-9) and False if they are out of bounds.
    def is_within_bounds(self, row, column):
        return 0 <= row < 10 and 0 <= column < 10

    # This method checks if a given coordinate is both within bounds and empty.
    # It's used to ensure that ships are placed within valid and unoccupied spaces.
    def is_valid(self, row, column):
        return self.is_within_bounds(row, column) and self.is_empty(row, column)

    # This method allows a player to place a ship on their board.
    # It asks the player to input the ship's orientation (horizontal or vertical) and the starting coordinate for placement.
    # It checks for valid placement (i.e., within bounds and no overlap with other ships).
    def place_ships(self, ship):
        orientation = None
        # Loop until the player selects a valid orientation (horizontal or vertical)
        while orientation not in ['h', 'v']:
            orientation = input("Would you like your ship to be horizontal or vertical?\nEnter 'h' for horizontal. Enter 'v' for vertical.\n").strip().lower()
        
        # Loop until a valid ship placement is entered
        while True:
            try:
                # Ask the player to enter the starting coordinate for the ship placement (e.g., "A1")
                location = input("Enter the upper leftmost coordinate you would like your ship to be placed at (e.g., A1): ").strip().upper()
                # Convert the input into board coordinates (row, column) and validate the format
                if len(location) == 2:  # Handles coordinates like A1, B3, etc.
                    col = ord(location[0]) - ord('A')
                    row = int(location[1]) - 1
                elif len(location) == 3 and location[1:] == "10":  # Handles coordinates like A10
                    col = ord(location[0]) - ord('A')
                    row = 9
                else:
                    raise ValueError("Invalid coordinate format.")

                # Check if the starting coordinate is within the board bounds
                if not self.is_within_bounds(row, col):
                    raise ValueError("Starting coordinate is out of bounds.")

                # For horizontal placement, check if the ship fits within bounds and does not overlap other ships
                if orientation == 'h':
                    if col + ship[1] > 10:
                        raise ValueError("Ship will go out of bounds horizontally.")
                    if any(not self.is_empty(row, col + i) for i in range(ship[1])):  # Check for overlapping ships
                        raise ValueError("Ship overlaps with another ship.")
                    for i in range(ship[1]):  # Place the ship on the board
                        self.board[row][col + i] = ship[1]
                
                # For vertical placement, check if the ship fits within bounds and does not overlap other ships
                else:
                    if row + ship[1] > 10:
                        raise ValueError("Ship will go out of bounds vertically.")
                    if any(not self.is_empty(row + i, col) for i in range(ship[1])):  # Check for overlapping ships
                        raise ValueError("Ship overlaps with another ship.")
                    for i in range(ship[1]):  # Place the ship on the board
                        self.board[row + i][col] = ship[1]
                
                break  # Exit the loop after successfully placing the ship

            except ValueError as e:
                # If there is an error during ship placement, show the error and prompt the user to try again
                print(e)
                print("Invalid placement. Please try again.")

    # This method processes a player's shot at the opponent's board.
    # It takes a coordinate as input and checks if the shot hits, misses, or sinks a ship.
    # It returns 0 for a miss, 1 for a hit, and 2 for a sunk ship.
    def fire(self, guess_coordinate, ship):
        try:
            # Convert the input coordinate (e.g., "A1") into board indices (row, column)
            if len(guess_coordinate) == 3 and guess_coordinate[1:] == "10":
                col = ord(guess_coordinate[0]) - ord('A')
                row = 9
            else:
                col = ord(guess_coordinate[0]) - ord('A')
                row = int(guess_coordinate[1]) - 1

            # Check if the shot is within the board's bounds
            if not self.is_within_bounds(row, col):
                print("Out of bounds. Please select a valid coordinate.")
                return 0

            target_value = self.board[row][col]  # Get the value of the board cell at the shot coordinate
            if isinstance(target_value, int):  # If the shot hits a ship (represented by an integer)
                self.board[row][col] = "X"  # Mark the hit with an "X"
                ship.remaining_units[target_value - 1] -= 1  # Decrease the remaining parts of the hit ship
                if ship.remaining_units[target_value - 1] == 0:
                    return 2  # Ship is sunk
                return 1  # Ship is hit but not sunk
            elif target_value == "~":  # If the shot misses (open water)
                self.board[row][col] = "."  # Mark the miss with a "."
                return 0  # Miss
            else:  # If the player already fired at this spot
                print("You already targeted this location.")
                return 0
        except Exception:
            # If an invalid coordinate is provided, catch the error and prompt the player to try again
            print("Error with the coordinate. Please try again.")
            return 0

    # This method performs an airstrike on a selected row.
    # The airstrike targets all columns in the row and marks hits and misses.
    # It returns the number of hits achieved in that row.
    def perform_airstrike(self, row):
        hits = 0  # Initialize a hit counter
        for col in range(10):
            if isinstance(self.board[row][col], int):  # If there is a ship in the current cell, hit it
                self.board[row][col] = "X"
                hits += 1  # Increment the hit counter for each hit
            elif self.board[row][col] == "~":  # If the cell is open water, mark it as a miss
                self.board[row][col] = "."
        return hits  # Return the total number of hits in the row

    # This method checks if the game is over by verifying if there are any ships remaining on the board.
    # It returns True if all ships have been hit and sunk, and False if any ships remain.
    def game_over(self):
        for rows in self.board:  # Iterate through each row on the board
            for space in rows:  # Check each space in the row
                if isinstance(space, int):  # If any space contains part of a ship (an integer), the game is not over
                    return False
        return True  # If no ships remain, return True indicating the game is over
