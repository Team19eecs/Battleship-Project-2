import os
import random

# Function to validate if a given coordinate is valid (e.g., A1, B10)
def is_valid_coordinate(coordinate):
    if len(coordinate) < 2 or len(coordinate) > 3:  # Coordinate must be 2 or 3 characters long (like A1, B10)
        return False
    row = coordinate[0].upper()  # Extract row (A-J)
    col = coordinate[1:]  # Extract column (1-10)

    # Check if row is between 'A' and 'J'
    if row < 'A' or row > 'J':
        return False
    # Check if column is a number between 1 and 10
    if not col.isdigit() or not (1 <= int(col) <= 10):
        return False
    return True

# Convert a board coordinate (e.g., A5) into row and column indices (for accessing the board array)
def coordinate_to_indices(coordinate):
    if len(coordinate) == 3 and coordinate[1:] == "10":  # Handle case for column 10
        col = ord(coordinate[0]) - ord('A')  # Convert column letter to index (A=0, B=1,...)
        row = 9  # Row 10 is index 9
    else:
        col = ord(coordinate[0]) - ord('A')  # Convert column letter to index
        row = int(coordinate[1]) - 1  # Convert row to 0-based index
    return row, col

# Generate a random valid coordinate for the board (e.g., A1, J10)
def generate_random_coordinate():
    row = random.randint(0, 9)  # Random row (0-9 corresponds to 1-10)
    col = random.randint(0, 9)  # Random column (0-9 corresponds to A-J)
    return chr(ord('A') + col) + str(row + 1)  # Convert to board coordinate (e.g., A5)

# Randomly choose an orientation for ship placement (horizontal or vertical)
def random_orientation():
    return random.choice(['h', 'v'])  # 'h' for horizontal, 'v' for vertical

# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # Use 'cls' for Windows, 'clear' for other OSes
