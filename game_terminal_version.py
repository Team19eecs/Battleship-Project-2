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

        
def ai_fire_medium(board, previous_hits, last_hit=None):
    """AI fires randomly until it hits, then fires in orthogonal directions around the hit until the ship is sunk."""
    if last_hit:
        row, col = last_hit
        directions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]  # Up, Down, Left, Right
        
        random.shuffle(directions)  # Randomize the direction choice
        
        for new_row, new_col in directions:
            if board.is_within_bounds(new_row, new_col) and board.board[new_row][new_col] == '~':
                return chr(ord('A') + new_col) + str(new_row + 1)
    
    # If there was no last hit or no adjacent cells available, fire randomly
    return ai_fire_easy(board)

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

if __name__ == '__main__':
    game_mode = display_title_screen()
    boards = [Board(player1), Board(player2)]
    ships = [Ships(player1), Ships(player2)]
    currentplayer = SwitchPlayers()
    startGame = Game(boards, ships, currentplayer)
    
    if game_mode == 1:
        startGame.game_setup(0)
        startGame.game_setup(1)
    else:
        ai_difficulty = choose_ai_difficulty()
        startGame.game_setup(0)
        print("\nThe AI is setting up its board...")
        ships[1].choose_ships()
        ships[1].load_types()
        ai_place_ships(boards[1], ships[1])
        currentplayer.end_turn()
    
    gameOver = False
    last_hit = None
    previous_hits = []
    ai_targeted_coordinates = set()  # Set to track the coordinates the Easy AI has targeted
    
    while not gameOver:
        player_continue = True
        currentplayer.begin_turn()
        currentboard = currentplayer.player_num - 1
        opponentboard = 1 - currentboard
        
        if game_mode == 1 or (game_mode == 2 and currentplayer.player_num == 1):
            boards[currentboard].display_board()
            boards[opponentboard].display_board()

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
                elif fire == 1:
                    print("HIT")
                    player_continue = False
                elif fire == 2:
                    print("SUNK BATTLESHIP")
                    if boards[opponentboard].game_over():
                        print(f"GAME OVER: Player {currentplayer.player_num} wins!")
                        gameOver = True
                        break
                    player_continue = False
                currentplayer.end_turn()

        else:
            if ai_difficulty == 1:
                ai_coordinate = ai_fire_easy(boards[0], ai_targeted_coordinates)  # Pass the targeted coordinates set
            elif ai_difficulty == 2:
                ai_coordinate = ai_fire_medium(boards[0], previous_hits, last_hit)
            elif ai_difficulty == 3:
                ai_coordinate = ai_fire_hard(boards[0])
            
            print(f"AI fires at {ai_coordinate}")
            fire = boards[0].fire(ai_coordinate, ships[0])
            
            if fire == 0:
                print("AI missed!")
                last_hit = None
                player_continue = False  # Ensures the AI turn ends
                currentplayer.end_turn()  # Properly switch back to Player 1
            elif fire == 1:
                print("AI hit your ship!")
                last_hit = (int(ai_coordinate[1:]) - 1, ord(ai_coordinate[0]) - ord('A'))
                previous_hits.append(last_hit)
                player_continue = False  # End the AI's turn
                currentplayer.end_turn()  # Switch back to Player 1
            elif fire == 2:
                print("AI sunk your ship!")
                if boards[0].game_over():
                    print("GAME OVER: AI wins!")
                    gameOver = True
                    break
                player_continue = False  # End the AI's turn
                currentplayer.end_turn()  # Switch back to Player 1
