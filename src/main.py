# Importing necessary modules required for the Battleship game.
# The `Board` class manages the player's board, keeping track of ship placements and fired shots.
# The `Ships` class handles the logic for creating, placing, and tracking ships.
# The `SwitchPlayers` class is responsible for switching between the two players.
# The `Game` class encapsulates the overall game logic, including the flow of turns and checking for game-over conditions.
# The AI functions (`ai_place_ships`, `ai_fire_easy`, `ai_fire_medium`, `ai_fire_hard`) are used to control the AI's behavior at different difficulty levels.
# The `coordinate_to_indices` utility function helps convert human-readable coordinates (e.g., "A5") to board indices.

from board import Board
from ships import Ships
from switch_players import SwitchPlayers
from game import Game
from ai import ai_place_ships, ai_fire_easy, ai_fire_medium, ai_fire_hard
from utilities import coordinate_to_indices

# Player identifiers for distinguishing between player 1 and player 2
player1 = 1
player2 = 2

# This function displays the title screen of the Battleship game to the player.
# It provides a brief welcome message and prompts the user to choose between two game modes:
# 1. Player vs Player (PvP) where both players are human.
# 2. Player vs AI (PvAI) where one player is human, and the other is controlled by an AI.
# The function ensures that the user input is either 1 or 2 by validating the input in a loop.
def display_title_screen():
    print("###############################")
    print("# Welcome to Battleship Game! #")
    print("###############################\n")
    print("Choose a game mode:")
    print("1. Play against another Player")
    print("2. Play against AI\n")
    
    # Loop until the user provides valid input (either 1 or 2). If invalid input is provided,
    # the function prompts the user again until a correct value is entered.
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice not in [1, 2]:  # Ensure input is either 1 or 2
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")  # Notify the user if input is invalid
    return choice  # Return the user's choice of game mode

# This function prompts the user to choose the difficulty level of the AI opponent.
# It offers three difficulty levels:
# 1. Easy: AI fires randomly without strategy.
# 2. Medium: AI starts targeting intelligently after a hit, but with basic logic.
# 3. Hard: AI uses advanced strategy to predict ship placements.
# Like the game mode selection, the function ensures that the user input is valid (either 1, 2, or 3).
def choose_ai_difficulty():
    print("\nChoose AI Difficulty Level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard\n")
    
    # Loop until the user provides valid input (1, 2, or 3). If the input is invalid,
    # the function prompts the user again until a valid difficulty level is selected.
    while True:
        try:
            difficulty = int(input("Enter your choice (1, 2, or 3): "))
            if difficulty not in [1, 2, 3]:  # Ensure input is either 1, 2, or 3
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")  # Notify the user if input is invalid
    return difficulty  # Return the selected difficulty level

# The main program execution begins here.
# This block of code is responsible for initializing the game, setting up the players (or AI), and starting the game loop.
if __name__ == '__main__':
    # Display the title screen and prompt the user to select the game mode.
    # Based on the return value from `display_title_screen()`, the game will either proceed as Player vs Player (PvP)
    # or Player vs AI (PvAI).
    game_mode = display_title_screen()
    
    # Initialize two game boards, one for each player.
    # `Board(player1)` initializes the game board for Player 1, and `Board(player2)` for Player 2.
    # Similarly, two `Ships` instances are created, which manage the placement and status of each player's ships.
    boards = [Board(player1), Board(player2)]
    ships = [Ships(player1), Ships(player2)]
    
    # Initialize the `SwitchPlayers` class, which manages alternating turns between players.
    currentplayer = SwitchPlayers()
    
    # Create an instance of the `Game` class, which handles overall game logic such as taking turns, checking for game over,
    # and managing the interaction between boards, ships, and players.
    startGame = Game(boards, ships, currentplayer)

    # Setup phase for Player vs Player or Player vs AI based on the selected game mode.
    # If the game mode is 1 (PvP), both players will manually place their ships.
    if game_mode == 1:
        # Player 1 sets up their ships by placing them on their board.
        startGame.game_setup(0)
        # Player 2 sets up their ships next.
        startGame.game_setup(1)
    else:
        # If game mode is 2 (PvAI), prompt the player to choose the AI difficulty level.
        ai_difficulty = choose_ai_difficulty()
        
        # Human player (Player 1) sets up their ships.
        startGame.game_setup(0)
        print("\nThe AI is setting up its board...")
        
        # The AI chooses and places its ships on its board.
        # `choose_ships()` handles AI's decision of which ships to place, and `load_types()` loads ship types for AI.
        # `ai_place_ships()` is responsible for placing the AI's ships randomly on the board.
        ships[1].choose_ships()
        ships[1].load_types()
        ai_place_ships(boards[1], ships[1])  # AI places its ships randomly on its board.
        
        # End the player's turn after setup to allow AI to begin its turn in the game loop.
        currentplayer.end_turn()
    
    # Initialize game variables for tracking the state of the game and AI.
    gameOver = False  # Boolean flag indicating if the game has ended
    last_hit = None   # Tracks the last hit made by a player
    previous_hits = []  # List to track previous hit coordinates
    ai_targeted_coordinates = set()  # A set to track the coordinates that the AI has already targeted, preventing repeated shots.
    
    # Initialize the AI state for medium and hard difficulty modes. The AI will use this state to intelligently 
    # select which coordinate to fire at based on previous hits and misses. The `target_mode` flag indicates whether
    # the AI is currently trying to sink a ship after a successful hit. Other parameters like `directions_tried` and 
    # `steps_in_current_direction` help the AI navigate around a hit ship to find the rest of it.
    ai_state = {
        'last_hit': None,
        'target_mode': False,  # Whether AI is actively targeting after a hit
        'directions_tried': [],  # Tracks directions AI has already tried
        'direction': None,  # The direction in which AI is currently firing
        'steps_in_current_direction': 0,  # How many steps the AI has taken in the current direction
        'initial_hit': None  # Stores the first hit's coordinates to help AI retrace its strategy if needed
    }
    
    # Main game loop. The game continues until one player or the AI sinks all the opponent's ships, 
    # which triggers the game over condition.
    while not gameOver:
        player_continue = True
        currentplayer.begin_turn()  # Start the current player's turn.
        
        # Determine the current and opponent board indices based on the current player's turn.
        current_board_index = currentplayer.player_num - 1  # Index of the current player's board
        opponent_board_index = 1 - current_board_index  # Index of the opponent's board
        
        # If it's a human player's turn (either in PvP or PvAI where Player 1 is human), allow them to fire.
        if game_mode == 1 or (game_mode == 2 and currentplayer.player_num == 1):
            boards[current_board_index].display_board()  # Display the current player's board.
            
            # The player takes their turn using the `take_turn()` method from the `Game` class.
            # This method handles input, firing at the opponent's board, and determining if the game is over.
            gameOver = startGame.take_turn(current_board_index)
            if gameOver:
                break  # Exit the game loop if the game is over.
            currentplayer.end_turn()  # End the player's turn after firing.

        else:
            # If it's the AI's turn (Player vs AI mode), the AI will fire at the human player's board.
            if ai_difficulty == 1:
                # Easy difficulty: AI randomly selects a coordinate to fire at, without any strategic logic.
                ai_coordinate = ai_fire_easy(boards[0], ai_targeted_coordinates)  # Track AI's fired coordinates to avoid duplicates.
            elif ai_difficulty == 2:
                # Medium difficulty: AI uses basic strategy after hitting a ship. It targets adjacent coordinates intelligently.
                ai_coordinate = ai_fire_medium(boards[0], ai_state, ai_targeted_coordinates)
            elif ai_difficulty == 3:
                # Hard difficulty: AI uses advanced algorithms to predict and fire at ship placements.
                ai_coordinate = ai_fire_hard(boards[0])

            # AI fires at the chosen coordinate and the result of the shot is processed.
            print(f"AI fires at {ai_coordinate}")
            fire_result = boards[0].fire(ai_coordinate, ships[0])  # `fire()` returns the result of the AI's shot (miss, hit, or sink).
            row, col = coordinate_to_indices(ai_coordinate)  # Convert the AI's coordinate to board indices.
            
            # AI shot result handling based on the fire result.
            # If AI misses, the targeting mode is reset (if applicable), and the turn ends.
            if fire_result == 0:  # Missed shot
                print("AI missed!")
                if ai_state['target_mode']:
                    # If AI was in targeting mode, reset the targeting direction and stop tracking hits in the current direction.
                    ai_state['direction'] = None
                    ai_state['steps_in_current_direction'] = 0
                else:
                    # If not in targeting mode, reset the last hit and targeting state.
                    ai_state['last_hit'] = None
                    ai_state['target_mode'] = False
                currentplayer.end_turn()  # End the AI's turn after a miss.
            elif fire_result == 1:  # Hit shot
                print("AI hit your ship!")
                # If AI was not already in targeting mode, enter targeting mode and start tracking the hit.
                if not ai_state['target_mode']:
                    ai_state['target_mode'] = True
                    ai_state['last_hit'] = (row, col)  # Update last hit coordinates for AI's strategy.
                    ai_state['initial_hit'] = (row, col)  # Record the initial hit to return if needed.
                    ai_state['directions_tried'] = []  # Reset directions tried for targeting.
                    ai_state['direction'] = None  # Reset current direction for AI's firing.
                    ai_state['steps_in_current_direction'] = 0  # Reset steps in current direction.
                else:
                    # Update the last hit if already in targeting mode.
                    ai_state['last_hit'] = (row, col)
                # Check if the human player has lost the game after the AI's hit.
                if boards[0].game_over():
                    print("GAME OVER: AI wins!")  # If the AI sinks all ships, declare the AI as the winner.
                    gameOver = True
                    break  # Exit the game loop.
                currentplayer.end_turn()  # AI ends turn after a successful hit.
            elif fire_result == 2:  # AI sunk a ship
                print("AI sunk your ship!")
                # If AI sinks a ship, reset targeting mode and stop tracking hits.
                if boards[0].game_over():
                    print("GAME OVER: AI wins!")  # Declare the AI as the winner if all ships are sunk.
                    gameOver = True
                    break  # Exit the game loop.
                ai_state['target_mode'] = False  # Reset AI targeting mode.
                ai_state['last_hit'] = None  # Reset last hit coordinates.
                ai_state['initial_hit'] = None  # Reset initial hit.
                ai_state['directions_tried'] = []  # Clear the list of tried directions.
                ai_state['direction'] = None  # Reset current direction.
                ai_state['steps_in_current_direction'] = 0  # Reset steps in current direction.
                currentplayer.end_turn()  # End the AI's turn after sinking a ship.
