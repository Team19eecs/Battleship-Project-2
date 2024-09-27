from utilities import is_valid_coordinate, clear_screen

class Game:
    # Initialize the Game class with boards, ships, and currentplayer objects.
    # Also initializes a `player_hits` array to keep track of consecutive hits for both players (Player 1 and Player 2).
    def __init__(self, boards, ships, currentplayer):
        self.boards = boards  # List of boards, one for each player
        self.ships = ships  # List of ships, one for each player
        self.currentplayer = currentplayer  # SwitchPlayers object to track current player's turn
        self.player_hits = [0, 0]  # Track consecutive hits for each player to trigger airstrikes

    # Setup phase for each player to position their ships on the board.
    # This method takes in a player number and initiates the setup process for that player.
    def game_setup(self, player):
        # Begin the player's setup turn
        self.currentplayer.begin_turn()

        # Display the key for the symbols used on the board (e.g., Ship, Hit, Miss)
        self.boards[player].symbol_key()

        # Player chooses the number of ships they want to place on the board
        self.ships[player].choose_ships()

        # Load the selected ship types (ship sizes) into the player's ship list
        self.ships[player].load_types()

        # Display the board for the player to see before they place ships
        self.boards[player].display_board()

        # For each ship the player has, allow them to place it on the board
        for ship in self.ships[player].ship_types:
            self.boards[player].place_ships(ship)  # Ask the player for coordinates and place the ship
            self.boards[player].display_board()  # Display the board after placing each ship

        clear_screen()  # Clear the screen after the player finishes placing all their ships
        self.currentplayer.end_turn()  # End the player's setup turn

    # Method to check if the player is eligible for an airstrike after 3 consecutive hits.
    # If eligible, allows the player to perform an airstrike on a row.
    def check_airstrike(self, player):
        # Check if the current player has had 3 or more consecutive hits
        if self.player_hits[player] >= 3:
            print("You have earned an airstrike! Choose a row (1-10) to fire at.")
            
            # Loop until a valid row number is chosen for the airstrike
            while True:
                try:
                    row = int(input("Enter row number (1-10) for airstrike: ")) - 1  # Convert to 0-based index
                    if row < 0 or row > 9:
                        raise ValueError("Row must be between 1 and 10.")  # Ensure row is within valid range
                    break
                except ValueError as e:
                    print(e)
                    continue
            
            # Perform the airstrike, which targets all columns in the selected row
            hits = self.boards[1 - player].perform_airstrike(row)
            print(f"Airstrike hit {hits} times on row {row + 1}.")  # Report the number of hits from the airstrike
            self.boards[1 - player].display_opponent_board()  # Show the updated opponent's board

            # Check if the airstrike results in a game win
            if self.boards[1 - player].game_over():
                print(f"GAME OVER: Player {player + 1} wins!")  # Announce the winner
                return True  # Return True to indicate the game is over

            # Reset the hit counter after the airstrike is performed
            self.player_hits[player] = 0

        return False  # Return False to indicate the game continues

    # Main method for managing a player's turn. It handles the process of firing at the opponent's board.
    def take_turn(self, player):
        player_continue = True  # Flag to determine if the player gets additional actions during their turn
        opponent = 1 - player  # Determine the opponent (player 0's opponent is player 1, and vice versa)
        self.boards[opponent].display_opponent_board()  # Display the opponent's board to the player

        # Loop to allow the player to continue taking actions (firing shots) in their turn
        while player_continue:
            # Prompt the player to enter a coordinate where they want to fire
            while True:
                guess_coordinate = input("Input the coordinate you want to fire at (e.g., A5 or A10): ").upper()
                if is_valid_coordinate(guess_coordinate):  # Validate the input coordinate
                    break
                else:
                    print("Invalid coordinate! Please enter a valid coordinate (e.g., A5 or A10).")

            # Fire at the guessed coordinate and determine the result
            fire = self.boards[opponent].fire(guess_coordinate, self.ships[opponent])

            # Check the result of the firing action
            if fire == 0:
                print("MISS")  # No ship hit, missed the shot
                player_continue = False  # End the player's turn
            elif fire == 1:
                print("HIT")  # Successfully hit an opponent's ship
                self.player_hits[player] += 1  # Increment the hit counter for consecutive hits

                # Check if the player has earned an airstrike or if the game has ended
                if self.check_airstrike(player):
                    return True  # Return True to indicate the game is over
                player_continue = False  # End the player's turn after the hit
            elif fire == 2:
                print("SUNK BATTLESHIP")  # The hit resulted in sinking an opponent's ship
                self.player_hits[player] += 1  # Increment the hit counter

                # Check if an airstrike is earned or if the game is over
                if self.check_airstrike(player):
                    return True  # End the game if airstrike wins the game
                if self.boards[opponent].game_over():
                    print(f"GAME OVER: Player {player + 1} wins!")  # Announce the winner
                    return True  # Return True to indicate the game is over
                player_continue = False  # End the player's turn after sinking the ship

        return False  # Return False to indicate the game continues
