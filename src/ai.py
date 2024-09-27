import random
from utilities import random_orientation, generate_random_coordinate

# Function for AI to place ships on the board
def ai_place_ships(board, ships):
    # For each ship in the ship types, attempt to place it on the board randomly
    for ship in ships.ship_types:
        placed = False
        while not placed:
            # Randomly choose orientation (horizontal/vertical) and starting coordinate
            orientation = random_orientation()
            start_coordinate = generate_random_coordinate()

            # Parse the start coordinate (handling cases like A10)
            if len(start_coordinate) == 3 and start_coordinate[1:] == "10":
                col = ord(start_coordinate[0]) - ord('A')  # Convert column letter to index (A=0, B=1,...)
                row = 9  # Row 10 is index 9
            else:
                col = ord(start_coordinate[0]) - ord('A')  # Convert column letter to index
                row = int(start_coordinate[1]) - 1  # Convert row to 0-based index

            try:
                # Handle horizontal placement
                if orientation == 'h':
                    if col + ship[1] > 10 or any(not board.is_empty(row, col + i) for i in range(ship[1])):
                        continue  # Skip to next iteration if placement isn't valid
                    for i in range(ship[1]):
                        board.board[row][col + i] = ship[1]  # Place ship horizontally on the board

                # Handle vertical placement
                else:
                    if row + ship[1] > 10 or any(not board.is_empty(row + i, col) for i in range(ship[1])):
                        continue  # Skip to next iteration if placement isn't valid
                    for i in range(ship[1]):
                        board.board[row + i][col] = ship[1]  # Place ship vertically on the board

                placed = True  # Mark the ship as placed successfully
            except Exception:
                continue  # In case of any error, skip and try again

# AI fires randomly at untargeted locations (Easy Mode)
def ai_fire_easy(board, targeted_coordinates):
    """
    AI fires at a random untargeted location.
    """
    while True:
        # Generate random column and row
        col = random.randint(0, 9)  # Columns from 0 (A) to 9 (J)
        row = random.randint(0, 9)  # Rows from 0 (1) to 9 (10)

        # Check if the chosen coordinate has been targeted before
        if (row, col) not in targeted_coordinates:
            targeted_coordinates.add((row, col))  # Mark the coordinate as targeted
            return chr(ord('A') + col) + str(row + 1)  # Return the coordinate in the correct format (e.g., 'A5')

# AI targets ship segments directly (Hard Mode)
def ai_fire_hard(board):
    """
    AI fires and always hits a ship's segment.
    It systematically searches for any ship segment and targets it.
    """
    for row in range(10):
        for col in range(10):
            # If the cell contains part of a ship (int) and hasn't been hit yet
            if isinstance(board.board[row][col], int):
                return chr(ord('A') + col) + str(row + 1)  # Convert to coordinate format and return
    return None  # Return None if no ship segment is left (this should not happen if game isn't over)

# AI uses a mix of random firing and systematic targeting (Medium Mode)
def ai_fire_medium(board, ai_state, ai_targeted_coordinates):
    """
    AI fires at random until it hits a ship, then switches to target mode.
    Systematically continues to fire at adjacent cells to sink the ship.
    """
    # Define movement directions: up, down, left, right
    DIRECTIONS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    # If AI isn't in target mode, it fires randomly
    if not ai_state['target_mode']:
        while True:
            col = random.randint(0, 9)  # Random column
            row = random.randint(0, 9)  # Random row
            if (row, col) not in ai_targeted_coordinates:  # Check if the coordinate hasn't been targeted
                ai_targeted_coordinates.add((row, col))  # Mark as targeted
                coordinate = chr(ord('A') + col) + str(row + 1)
                return coordinate

    # In target mode, attempt to sink the hit ship
    else:
        initial_row, initial_col = ai_state['initial_hit']  # Get the initial hit coordinate

        # If no direction chosen yet, pick a new direction to try
        if ai_state['direction'] is None:
            possible_directions = ['up', 'down', 'left', 'right']
            directions_tried = ai_state['directions_tried']
            remaining_directions = [d for d in possible_directions if d not in directions_tried]
            
            # If all directions have been tried, reset target mode
            if not remaining_directions:
                ai_state['target_mode'] = False
                ai_state['last_hit'] = None
                ai_state['directions_tried'] = []
                ai_state['direction'] = None
                ai_state['steps_in_current_direction'] = 0
                ai_state['initial_hit'] = None
                return ai_fire_medium(board, ai_state, ai_targeted_coordinates)  # Go back to random firing
            else:
                ai_state['direction'] = random.choice(remaining_directions)  # Choose a new direction
                ai_state['directions_tried'].append(ai_state['direction'])  # Mark direction as tried
                ai_state['steps_in_current_direction'] = 1  # Reset steps in this direction

        # Continue in the chosen direction to find more ship segments
        else:
            ai_state['steps_in_current_direction'] += 1  # Increment steps in the current direction

        # Calculate the next coordinate in the current direction
        dir_row_delta, dir_col_delta = DIRECTIONS[ai_state['direction']]
        steps = ai_state['steps_in_current_direction']
        new_row = initial_row + dir_row_delta * steps
        new_col = initial_col + dir_col_delta * steps

        # Check if the new coordinate is within bounds and hasn't been targeted yet
        if 0 <= new_row < 10 and 0 <= new_col < 10:
            if (new_row, new_col) not in ai_targeted_coordinates:
                ai_targeted_coordinates.add((new_row, new_col))  # Mark as targeted
                coordinate = chr(ord('A') + new_col) + str(new_row + 1)
                return coordinate
            else:
                # Already targeted, need to pick a new direction
                ai_state['direction'] = None
                ai_state['steps_in_current_direction'] = 0
                return ai_fire_medium(board, ai_state, ai_targeted_coordinates)  # Continue targeting mode
        else:
            # Out of bounds, need to try a new direction
            ai_state['direction'] = None
            ai_state['steps_in_current_direction'] = 0
            return ai_fire_medium(board, ai_state, ai_targeted_coordinates)  # Continue targeting mode
