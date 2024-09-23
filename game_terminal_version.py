#! python3
# Game loop and all core logic
'''
Program: Battleship
Description: This program will be a functional two-player game of battleship.
             This file contains the main game loop and core logic.
Output: A game of battleship played in the terminal.
Authors: Brynn Hare, Micah Borghese, Katelyn Accola, Nora Manolescu, and Kyle Johnson
Creation date: 9/4/2024
'''

player1 = 1  # global variable to represent player 1
player2 = 2  # global variable to represent player 2

class Board:

    def __init__(self, player_num):
        self.player_num = player_num  # Assign each player number a corresponding board
        self.board = [["~" for _ in range(10)] for _ in range(10)]  # upon creation, game board should be filled with empty spaces only

    def symbol_key(self):
        # print out the key so that the reader can understand the symbols
        print("Symbol Key for Battleship: ")
        print(f'\tShip: O\n\tShip hit: X\n\tShip sunk: *\n\tOpen spot: ~\n\tMissfire: .\n')

    def display_board(self):
        # Display the current user's board
        print("Here is your board: ")
        print("  " + " ".join(chr(ord('A') + i) for i in range(10)))  # print out letters as column headers
        for i, row in enumerate(self.board):
            formatted_row = ["O" if isinstance(cell, int) else cell for cell in row]
            print(f"{i + 1:2} " + " ".join(formatted_row))

    def display_opponent_board(self):
        # printing out your opponent's board, not displaying their unhit ships
        print("Here is your opponent's board: ")
        print("  " + " ".join(chr(ord('A') + i) for i in range(10)))  # Column labels A-J
        for i, row in enumerate(self.board):
            display_row = ['~' if isinstance(cell, int) else cell for cell in row]
            print(f"{i + 1:2} " + " ".join(display_row))

    def is_empty(self, row, column):
        # Check if spot is free for use in ship placement
        return self.board[row][column] == "~"

    def is_within_bounds(self, row, column):
        # Check if spot is within the 10x10 grid
        return 0 <= row < 10 and 0 <= column < 10

    def is_valid(self, row, column):
        # Check if spot is within range and is empty
        return self.is_within_bounds(row, column) and self.is_empty(row, column)

    def place_ships(self, ship):
        orientation = None
        while orientation not in ['h', 'v']:
            orientation = input("Would you like your ship to be horizontal or vertical?\nEnter 'h' for horizontal. Enter 'v' for vertical.\n").strip().lower()
        
        while True:
            try:
                location = input("Enter the upper leftmost coordinate you would like your ship to be placed at (e.g., A1): ").strip().upper()
                if len(location) == 2:
                    col = ord(location[0]) - ord('A')
                    row = int(location[1]) - 1
                elif len(location) == 3 and location[1:] == "10":
                    col = ord(location[0]) - ord('A')
                    row = 9
                else:
                    raise ValueError("Invalid coordinate format.")
                
                if not self.is_within_bounds(row, col):
                    raise ValueError("Starting coordinate is out of bounds.")

                if orientation == 'h':
                    if col + ship[1] > 10:
                        raise ValueError("Ship will go out of bounds horizontally.")
                    if any(not self.is_empty(row, col + i) for i in range(ship[1])):
                        raise ValueError("Ship overlaps with another ship.")
                    for i in range(ship[1]):
                        self.board[row][col + i] = ship[1]
                else:
                    if row + ship[1] > 10:
                        raise ValueError("Ship will go out of bounds vertically.")
                    if any(not self.is_empty(row + i, col) for i in range(ship[1])):
                        raise ValueError("Ship overlaps with another ship.")
                    for i in range(ship[1]):
                        self.board[row + i][col] = ship[1]
                
                break  # Exit the loop if ship placed successfully

            except ValueError as e:
                print(e)
                print("Invalid placement. Please try again.")

    def fire(self, guess_coordinate, ship):
        try:
            if len(guess_coordinate) == 3 and guess_coordinate[1:] == "10":
                col = ord(guess_coordinate[0]) - ord('A')
                row = 9
            else:
                col = ord(guess_coordinate[0]) - ord('A')
                row = int(guess_coordinate[1]) - 1

            if not self.is_within_bounds(row, col):
                print("Out of bounds. Please select a valid coordinate.")
                return 0

            target_value = self.board[row][col]
            if isinstance(target_value, int):
                self.board[row][col] = "X"
                ship.remaining_units[target_value - 1] -= 1
                if ship.remaining_units[target_value - 1] == 0:
                    return 2  # Ship sunk
                return 1  # Hit but not sunk
            elif target_value == "~":
                self.board[row][col] = "."
                return 0  # Miss
            else:
                print("You already targeted this location.")
                return 0
        except Exception:
            print("Error with the coordinate. Please try again.")
            return 0

    def game_over(self):
        for rows in self.board:
            for space in rows:
                if isinstance(space, int):
                    return False
        return True

# Rest of the classes (Ships, SwitchPlayers, Game) remain the same except any calls to the modified Board methods


class Ships: 
    #class that handles 1b; assigning the correct number of ships to a user
    def __init__(self, player_num):
        self.player_num = player_num #this will be put in by us each time they switch, to reprsent player 1 or 2
        self.num_ships = 0 #this is provided by the player later (must be numbers 1-5 inclusively)
        self.ship_types = [] #empty list to hold the sizes of the ships
        self.remaining_units = [] #keep track of how many units of a ship have been hit to know when it is sunk

    def choose_ships(self): #the player must select the number of ships they want to have
        while True:    
            try:  
                num_ships = int(input("Choose the number of ships for your board (1-5): "))
                self.num_ships = num_ships
                break
            except: 
                print("Invalid number of ships.")
        while (self.num_ships < 1) or (self.num_ships > 5): #checking for invalid ship values
            try: 
                new_num = int(input("Invalid number of ships. Select a new number: ")) #prompt for another number ***THIS CAN BE CHANGED JUST AN INITIAL PHASE***
                self.num_ships = new_num #assign the new number to be the number of ships
            except: 
                self.num_ships = 0
        for i in range(num_ships): # keep track of how many unsunk units for each ship
            self.remaining_units.append(i+1)

    def load_types(self): #this forms the list with the sizes of the ships
        i = 1 #initializing for the while loop
        while i < (self.num_ships + 1): #while the current ship number is less than one extra than the number of ships chosen
            self.ship_types.append([1, i]) #append to the list. [1, 1] represents 1 x 1. [1, 2] represents 1 x 2...etc.
            i += 1 #increase the while loop


class SwitchPlayers:
    # Can be used any time to switch players
    # The main purpose of this class is to give the players a warning that a turn will switch 
    # This prevents the opposing player's board from displaying, spoiling the secrecy of the game
    def __init__(self):
        # Initialize player by starting with player 1 
        self.player_num = 1
    
    # To change players
    def change(self):
        if self.player_num == 1: 
            self.player_num = 2 # If currently player 1, switch to player 2
        else: 
            self.player_num = 1 # If currently player 2, switch to player 1 
            
    # To begin player's turn 
    def begin_turn(self):
        # Begin player's turn and wait until there is an input
        print("Begin Player", self.player_num,"'s Turn (Press Enter)") 
        input() # Requires user to enter to confirm start of a turn 
        
    # To end player's turn 
    def end_turn(self):
        # Display turn is ending for the player and wait until there is an input
        print("End Player", self.player_num,"'s Turn (Press Enter)") 
        input() # Requires user to enter to confirm end of their turn 

        # Switch players after confirming turn is over 
        self.change() 

# Check if coordinate is valid 
def is_valid_coordinate(coordinate):
    # Check if coordinate has correct number of characters 
    if len(coordinate) < 2 or len(coordinate) > 3:
        return False

    # Store coordinate row and column 
    row = coordinate[0].upper()
    col = coordinate[1:]

    # Check if the row is a letter between A and J (for a 10x10 grid)
    if row < 'A' or row > 'J':
        return False

    # Check if the column is a number between 1 and 10
    if not col.isdigit() or not (1 <= int(col) <= 10):
        return False

    # Otherwise, coordinate is valid 
    return True

class Game:
    def __init__(self, boards, ships, currentplayer):
        self.boards = boards
        self.ships = ships
        self.currentplayer = currentplayer

    # Method where player sets up their board
    def game_setup(self, player): 
        # Prompt current player to begin first turn 
        self.currentplayer.begin_turn() 

        # Print the key & symbols for the games
        self.boards[player].symbol_key()

        # Prompt current player to select number of ships (1-5)
        self.ships[player].choose_ships() 
        self.ships[player].load_types() # Create the list to store current player's ships
        
        # Display the blank board
        self.boards[player].display_board() 

        # Place each of the player's ships 
        for ship in self.ships[player].ship_types: # Iterate over list of ships to place each ship the player has
            self.boards[player].place_ships(ship) # Make the board class write in the ship to the board as its placed
            self.boards[player].display_board() # Display what the updated board looks like after a ship is placed 
        
        # Confirm the end of current player's setup turn and make opponent the new current player
        self.currentplayer.end_turn() 

if __name__ == '__main__':
    boards = [Board(player1), Board(player2)] 
    ships = [Ships(player1), Ships(player2)]
    currentplayer = SwitchPlayers()
    startGame = Game(boards, ships, currentplayer)

    startGame.game_setup(0)
    startGame.game_setup(1)

    gameOver = False
    while not gameOver:
        player_continue = True
        currentplayer.begin_turn()
        currentboard = currentplayer.player_num - 1
        opponentboard = 1 - currentboard
        boards[currentboard].display_board()

        while player_continue:
            boards[opponentboard].display_opponent_board()
            while True:
                guess_coordinate = input("Input the coordinate you want to fire at (e.g., A5 or A10): ").upper()
                if is_valid_coordinate(guess_coordinate):
                    break
                else:
                    print("Invalid coordinate! Please enter a valid coordinate (e.g., A5 or A10).")

            fire = boards[opponentboard].fire(guess_coordinate, ships[opponentboard])
            if fire == 0:
                print("MISS")
                boards[opponentboard].display_opponent_board()
                player_continue = False
                currentplayer.end_turn()
            elif fire == 1:
                print("HIT")
            elif fire == 2:
                print("SUNK BATTLESHIP")
                if boards[opponentboard].game_over():
                    print(f"GAME OVER: Player {currentplayer.player_num} wins!")
                    gameOver = True
                    break