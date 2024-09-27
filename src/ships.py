class Ships:
    # Constructor for initializing the Ships object.
    # Each player has their own instance of Ships, where their ships' data (number, types, and remaining units) are stored.
    # The constructor initializes three attributes: 
    # 1. `player_num` to identify which player owns these ships.
    # 2. `num_ships` to store how many ships the player has (initially 0).
    # 3. `ship_types` and `remaining_units` are initialized as empty lists and will hold the ship types and their hit points.
    def __init__(self, player_num):
        self.player_num = player_num  # Store the player number (either player 1 or player 2)
        self.num_ships = 0  # Number of ships is initially set to 0
        self.ship_types = []  # This list will store the types of ships (each ship type has a specific size)
        self.remaining_units = []  # This list will store how many units (hit points) each ship has remaining

    # This method allows the player to choose the number of ships they want to place on their board.
    # It enforces that the number must be between 1 and 5 and ensures valid input from the user.
    def choose_ships(self):
        while True:
            try:
                # Prompt the player to select how many ships they want to play with (between 1 and 5)
                num_ships = int(input("Choose the number of ships for your board (1-5): "))
                self.num_ships = num_ships  # Store the chosen number of ships
                break  # Exit the loop once a valid number is entered
            except:  # Handle cases where the input isn't a valid integer
                print("Invalid number of ships.")  # Prompt the player to try again
        
        # If the user selects an invalid number outside the range (1-5), prompt them to select a valid number
        while (self.num_ships < 1) or (self.num_ships > 5):
            try:
                # Ask the player to select a valid number of ships
                new_num = int(input("Invalid number of ships. Select a new number: "))
                self.num_ships = new_num  # Store the corrected number of ships
            except:
                self.num_ships = 0  # If input fails again, reset `num_ships` to 0

        # Once a valid number of ships is set, initialize the `remaining_units` list.
        # Each ship starts with a number of hit points equal to its index + 1 (i.e., ship 1 has 1 HP, ship 2 has 2 HP, etc.)
        for i in range(num_ships):
            self.remaining_units.append(i + 1)  # Add the number of hit points to each ship

    # This method loads the ship types and their associated sizes.
    # Each ship's size is determined by its index (e.g., the first ship has size 1, the second ship has size 2, and so on).
    # The `ship_types` list is filled with ships, where each ship is represented by a list containing [1, size].
    def load_types(self):
        i = 1
        # Loop through the number of ships and assign each ship a type and size
        while i < (self.num_ships + 1):  # Loop through the number of ships the player has chosen
            self.ship_types.append([1, i])  # Add the ship type to `ship_types`. Each ship type is a list of [1, ship size]
            i += 1  # Increment to the next ship type
