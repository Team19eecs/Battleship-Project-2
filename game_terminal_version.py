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

import random

player1 = 1  # global variable to represent player 1
player2 = 2  # global variable to represent player 2

class Board:
    def __init__(self, player_num):
        self.player_num = player_num  
        self.board = [["~" for _ in range(10)] for _ in range(10)]

    def symbol_key(self):
        print("Symbol Key for Battleship: ")
        print(f'\tShip: O\n\tShip hit: X\n\tShip sunk: *\n\tOpen spot: ~\n\tMissfire: .\n')

    def display_board(self):
        print("Here is your board: ")
        print("  " + " ".join(chr(ord('A') + i) for i in range(10)))
        for i, row in enumerate(self.board):
            formatted_row = ["O" if isinstance(cell, int) else cell for cell in row]
            print(f"{i + 1:2} " + " ".join(formatted_row))

    def display_opponent_board(self):
        print("Here is your opponent's board: ")
        print("  " + " ".join(chr(ord('A') + i) for i in range(10)))
        for i, row in enumerate(self.board):
            display_row = ['~' if isinstance(cell, int) else cell for cell in row]
            print(f"{i + 1:2} " + " ".join(display_row))

    def is_empty(self, row, column):
        return self.board[row][column] == "~"

    def is_within_bounds(self, row, column):
        return 0 <= row < 10 and 0 <= column < 10

    def is_valid(self, row, column):
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
                
                break

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
        
    def perform_airstrike(self, row):
        hits = 0
        for col in range(10):
            if isinstance(self.board[row][col], int):
                self.board[row][col] = "X"
                hits += 1
            elif self.board[row][col] == "~":
                self.board[row][col] = "."
        return hits


    def game_over(self):
        for rows in self.board:
            for space in rows:
                if isinstance(space, int):
                    return False
        return True

class Ships:
    def __init__(self, player_num):
        self.player_num = player_num 
        self.num_ships = 0 
        self.ship_types = [] 
        self.remaining_units = [] 

    def choose_ships(self): 
        while True:    
            try:  
                num_ships = int(input("Choose the number of ships for your board (1-5): "))
                self.num_ships = num_ships
                break
            except: 
                print("Invalid number of ships.")
        while (self.num_ships < 1) or (self.num_ships > 5): 
            try: 
                new_num = int(input("Invalid number of ships. Select a new number: ")) 
                self.num_ships = new_num 
            except: 
                self.num_ships = 0
        for i in range(num_ships):
            self.remaining_units.append(i + 1)

    def load_types(self):
        i = 1 
        while i < (self.num_ships + 1): 
            self.ship_types.append([1, i]) 
            i += 1 

class SwitchPlayers:
    def __init__(self):
        self.player_num = 1
    
    def change(self):
        if self.player_num == 1: 
            self.player_num = 2 
        else: 
            self.player_num = 1 
            
    def begin_turn(self):
        print("Begin Player", self.player_num,"'s Turn (Press Enter)") 
        input() 
        
    def end_turn(self):
        print("End Player", self.player_num,"'s Turn (Press Enter)") 
        input()
        self.change() 

def is_valid_coordinate(coordinate):
    if len(coordinate) < 2 or len(coordinate) > 3:
        return False
    row = coordinate[0].upper()
    col = coordinate[1:]
    if row < 'A' or row > 'J':
        return False
    if not col.isdigit() or not (1 <= int(col) <= 10):
        return False
    return True

class Game:
    def __init__(self, boards, ships, currentplayer):
        self.boards = boards
        self.ships = ships
        self.currentplayer = currentplayer
        self.player_hits = [0, 0]  # Track consecutive hits for each player


    def game_setup(self, player): 
        self.currentplayer.begin_turn() 
        self.boards[player].symbol_key()
        self.ships[player].choose_ships() 
        self.ships[player].load_types() 
        self.boards[player].display_board() 
        for ship in self.ships[player].ship_types:
            self.boards[player].place_ships(ship)
            self.boards[player].display_board() 
        self.currentplayer.end_turn() 
        
    def check_airstrike(self, player):
        if self.player_hits[player] >= 3:
            print("You have earned an airstrike! Choose a row (1-10) to fire at.")
            while True:
                try:
                    row = int(input("Enter row number (1-10) for airstrike: ")) - 1
                    if row < 0 or row > 9:
                        raise ValueError("Row must be between 1 and 10.")
                    break
                except ValueError as e:
                    print(e)
                    continue
            
            # Perform the airstrike
            hits = self.boards[1 - player].perform_airstrike(row)
            print(f"Airstrike hit {hits} times on row {row + 1}.")
            self.boards[1 - player].display_opponent_board()
            
            # Check if the game is over after the airstrike
            if self.boards[1 - player].game_over():
                print(f"GAME OVER: Player {player + 1} wins!")
                return True  # Return True to indicate game over

            # Reset the hit counter after the airstrike
            self.player_hits[player] = 0  
        
        return False  # Return False to indicate the game continues

            
    def take_turn(self, player):
        player_continue = True
        opponent = 1 - player
        self.boards[opponent].display_opponent_board()
        
        while player_continue:
            while True:
                guess_coordinate = input("Input the coordinate you want to fire at (e.g., A5 or A10): ").upper()
                if is_valid_coordinate(guess_coordinate):
                    break
                else:
                    print("Invalid coordinate! Please enter a valid coordinate (e.g., A5 or A10).")

            fire = self.boards[opponent].fire(guess_coordinate, self.ships[opponent])
            
            if fire == 0:
                print("MISS")
                # self.player_hits[player] = 0  # Reset the hit counter
                player_continue = False
            elif fire == 1:
                print("HIT")
                self.player_hits[player] += 1
                if self.check_airstrike(player):  # Check for airstrike and game over
                    return True  # End the game if an airstrike results in a win
                player_continue = False
            elif fire == 2:
                print("SUNK BATTLESHIP")
                self.player_hits[player] += 1
                if self.check_airstrike(player):  # Check for airstrike and game over
                    return True  # End the game if an airstrike results in a win
                if self.boards[opponent].game_over():
                    print(f"GAME OVER: Player {player + 1} wins!")
                    return True
                player_continue = False

        return False



def display_title_screen():
    print("###############################")
    print("# Welcome to Battleship Game! #")
    print("###############################\n")
    print("Choose a game mode:")
    print("1. Play against another Player")
    print("2. Play against AI\n")
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice not in [1, 2]:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")
    return choice

def choose_ai_difficulty():
    print("\nChoose AI Difficulty Level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard\n")
    while True:
        try:
            difficulty = int(input("Enter your choice (1, 2, or 3): "))
            if difficulty not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")
    return difficulty

def generate_random_coordinate():
    row = random.randint(0, 9)
    col = random.randint(0, 9)
    return chr(ord('A') + col) + str(row + 1)

def random_orientation():
    return random.choice(['h', 'v'])

def ai_place_ships(board, ships):
    for ship in ships.ship_types:
        placed = False
        while not placed:
            orientation = random_orientation()
            start_coordinate = generate_random_coordinate()
            if len(start_coordinate) == 3 and start_coordinate[1:] == "10":
                col = ord(start_coordinate[0]) - ord('A')
                row = 9
            else:
                col = ord(start_coordinate[0]) - ord('A')
                row = int(start_coordinate[1]) - 1
            try:
                if orientation == 'h':
                    if col + ship[1] > 10 or any(not board.is_empty(row, col + i) for i in range(ship[1])):
                        continue
                    for i in range(ship[1]):
                        board.board[row][col + i] = ship[1]
                else:
                    if row + ship[1] > 10 or any(not board.is_empty(row + i, col) for i in range(ship[1])):
                        continue
                    for i in range(ship[1]):
                        board.board[row + i][col] = ship[1]
                placed = True
            except Exception:
                continue

def ai_fire_easy(board, targeted_coordinates):
    """
    AI fires at a random location that hasn't been targeted yet.
    """
    while True:
        # Generate a random coordinate
        col = random.randint(0, 9)  # Columns range from 0 (A) to 9 (J)
        row = random.randint(0, 9)  # Rows range from 0 (1) to 9 (10)
        
        # Check if this coordinate has been targeted before
        if (row, col) not in targeted_coordinates:
            targeted_coordinates.add((row, col))  # Mark this coordinate as targeted
            return chr(ord('A') + col) + str(row + 1)  # Return the coordinate in proper format (e.g., 'A5')

def ai_fire_hard(board):
    """
    AI fires and always hits a ship's segment on each turn.
    It systematically looks for any part of a ship and targets it directly.
    """
    for row in range(10):
        for col in range(10):
            # Check if the cell contains a part of a ship (integer value) that hasn't been hit
            if isinstance(board.board[row][col], int):
                return chr(ord('A') + col) + str(row + 1)  # Convert to coordinate and return
    return None  # This should never happen as long as there are ship parts left to hit

def coordinate_to_indices(coordinate):
    if len(coordinate) == 3 and coordinate[1:] == "10":
        col = ord(coordinate[0]) - ord('A')
        row = 9
    else:
        col = ord(coordinate[0]) - ord('A')
        row = int(coordinate[1]) - 1
    return row, col

def ai_fire_medium(board, ai_state, ai_targeted_coordinates):
    DIRECTIONS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    if not ai_state['target_mode']:
        # Fire randomly at untargeted coordinates
        while True:
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            if (row, col) not in ai_targeted_coordinates:
                ai_targeted_coordinates.add((row, col))
                coordinate = chr(ord('A') + col) + str(row + 1)
                return coordinate
    else:
        # In target mode, attempt to sink the ship
        # Get initial_hit coordinate
        initial_row, initial_col = ai_state['initial_hit']
        # If direction is None, pick a new direction
        if ai_state['direction'] is None:
            possible_directions = ['up', 'down', 'left', 'right']
            directions_tried = ai_state['directions_tried']
            remaining_directions = [d for d in possible_directions if d not in directions_tried]
            if not remaining_directions:
                # All directions tried, reset target mode
                ai_state['target_mode'] = False
                ai_state['last_hit'] = None
                ai_state['directions_tried'] = []
                ai_state['direction'] = None
                ai_state['steps_in_current_direction'] = 0
                ai_state['initial_hit'] = None
                # Go back to random firing
                return ai_fire_medium(board, ai_state, ai_targeted_coordinates)
            else:
                # Choose a new direction
                ai_state['direction'] = random.choice(remaining_directions)
                ai_state['directions_tried'].append(ai_state['direction'])
                ai_state['steps_in_current_direction'] = 1
        else:
            # Continue in the same direction
            ai_state['steps_in_current_direction'] += 1

        # Calculate next coordinate
        dir_row_delta, dir_col_delta = DIRECTIONS[ai_state['direction']]
        steps = ai_state['steps_in_current_direction']
        new_row = initial_row + dir_row_delta * steps
        new_col = initial_col + dir_col_delta * steps

        # Check bounds and if coordinate has been targeted
        if 0 <= new_row < 10 and 0 <= new_col < 10:
            if (new_row, new_col) not in ai_targeted_coordinates:
                ai_targeted_coordinates.add((new_row, new_col))
                coordinate = chr(ord('A') + new_col) + str(new_row + 1)
                return coordinate
            else:
                # Already targeted, need to try a new direction
                ai_state['direction'] = None
                ai_state['steps_in_current_direction'] = 0
                # Continue in target mode
                return ai_fire_medium(board, ai_state, ai_targeted_coordinates)
        else:
            # Out of bounds, need to try a new direction
            ai_state['direction'] = None
            ai_state['steps_in_current_direction'] = 0
            # Continue in target mode
            return ai_fire_medium(board, ai_state, ai_targeted_coordinates)

if __name__ == '__main__':
    # Display the title screen and choose the game mode
    game_mode = display_title_screen()
    
    # Initialize the boards, ships, and player switching mechanism
    boards = [Board(player1), Board(player2)]
    ships = [Ships(player1), Ships(player2)]
    currentplayer = SwitchPlayers()
    
    # Create the main Game instance
    startGame = Game(boards, ships, currentplayer)

    # Setup phase for player vs player or player vs AI
    if game_mode == 1:
        # Player vs Player setup
        startGame.game_setup(0)
        startGame.game_setup(1)
    else:
        # Player vs AI setup
        ai_difficulty = choose_ai_difficulty()
        startGame.game_setup(0)  # Setup for the human player
        print("\nThe AI is setting up its board...")
        ships[1].choose_ships()
        ships[1].load_types()
        ai_place_ships(boards[1], ships[1])  # AI sets up its board
        currentplayer.end_turn()
    
    # Game loop
    gameOver = False
    last_hit = None
    previous_hits = []
    ai_targeted_coordinates = set()  # Set to track the coordinates the AI has targeted
    # Initialize AI state for medium difficulty
    ai_state = {
        'last_hit': None,
        'target_mode': False,
        'directions_tried': [],
        'direction': None,
        'steps_in_current_direction': 0,
        'initial_hit': None
    }
    
    while not gameOver:
        player_continue = True
        currentplayer.begin_turn()
        current_board_index = currentplayer.player_num - 1
        opponent_board_index = 1 - current_board_index
        
        if game_mode == 1 or (game_mode == 2 and currentplayer.player_num == 1):
            # Player's turn (Player vs Player or Player vs AI with human playing)
            boards[current_board_index].display_board()
            boards[opponent_board_index].display_board()

            # Use the Game class's method to handle the turn
            gameOver = startGame.take_turn(current_board_index)
            if gameOver:
                break
            currentplayer.end_turn()

        else:
            # AI's turn
            if ai_difficulty == 1:
                ai_coordinate = ai_fire_easy(boards[0], ai_targeted_coordinates)  # Pass the targeted coordinates set
            elif ai_difficulty == 2:
                ai_coordinate = ai_fire_medium(boards[0], ai_state, ai_targeted_coordinates)
            elif ai_difficulty == 3:
                ai_coordinate = ai_fire_hard(boards[0])

            print(f"AI fires at {ai_coordinate}")
            fire_result = boards[0].fire(ai_coordinate, ships[0])
            row, col = coordinate_to_indices(ai_coordinate)

            if fire_result == 0:
                print("AI missed!")
                if ai_state['target_mode']:
                    ai_state['direction'] = None
                    ai_state['steps_in_current_direction'] = 0
                else:
                    ai_state['last_hit'] = None
                    ai_state['target_mode'] = False
                currentplayer.end_turn()
            elif fire_result == 1:
                print("AI hit your ship!")
                if not ai_state['target_mode']:
                    ai_state['target_mode'] = True
                    ai_state['last_hit'] = (row, col)
                    ai_state['initial_hit'] = (row, col)
                    ai_state['directions_tried'] = []
                    ai_state['direction'] = None
                    ai_state['steps_in_current_direction'] = 0
                else:
                    ai_state['last_hit'] = (row, col)
                # Check if the AI has won after a hit
                if boards[0].game_over():
                    print("GAME OVER: AI wins!")
                    gameOver = True
                    break
                currentplayer.end_turn()
            elif fire_result == 2:
                print("AI sunk your ship!")
                if boards[0].game_over():
                    print("GAME OVER: AI wins!")
                    gameOver = True
                    break  # Ensure game loop exits when AI wins
                ai_state['target_mode'] = False
                ai_state['last_hit'] = None
                ai_state['initial_hit'] = None
                ai_state['directions_tried'] = []
                ai_state['direction'] = None
                ai_state['steps_in_current_direction'] = 0
                currentplayer.end_turn()
