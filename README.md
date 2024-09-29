**System Requirements**
Recommended Compiler: Visual Studio Code
Programming Language: Python 3
Required Libraries: No external libraries are evident from the snippet; only standard Python libraries (random).

**How to Run**
1. Download the src file
2. Open it in Visual Studio Code (or any other compiler)
3. Run the main.py file in the terminal

**Program Structure**
Start the Game:

When the program is executed, the title screen appears, welcoming you to the Battleship Game.
You are prompted to select a game mode:
Press 1 for Player vs Player.
Press 2 for Player vs AI.
AI Difficulty Selection (if Player vs AI):

If you select Player vs AI, you will then choose the AI difficulty level:
1 for Easy: The AI selects random coordinates to fire.
2 for Medium: The AI combines random firing with a target mode to improve accuracy when it hits a ship.
3 for Hard: The AI always targets a ship segment.

Game Setup:

Each player takes turns to place their ships on their respective boards:
You will be prompted to choose the number of ships (1 to 5).
For each ship, choose the orientation ('h' for horizontal or 'v' for vertical) and specify the starting coordinate (e.g., A1).
In Player vs AI, the human player sets up their board first, and the AI places its ships automatically.

Gameplay:

Players take turns firing at the opponent's board:
Enter a coordinate (e.g., B5) to target where you think your opponent's ship is located.
The game will inform you if you hit (HIT), missed (MISS), or sunk a battleship (SUNK BATTLESHIP).

Airstrike Feature:

When a player lands three consecutive hits, they earn an airstrike.
You will be prompted to choose a row (1-10) to target the entire row, increasing your chances of hitting multiple ship segments.
End of Game:

The game continues until one player's ships are entirely sunk.
The program announces the winner, displaying "GAME OVER: Player X wins!" or "GAME OVER: AI wins!" if the AI wins.
