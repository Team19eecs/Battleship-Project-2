from utilities import clear_screen

class SwitchPlayers:
    # Constructor initializes the class with the current player's number, starting with Player 1 by default.
    def __init__(self):
        self.player_num = 1  # Player 1 starts first

    # This method switches the current player.
    # If the current player is 1, it changes to 2; if it's 2, it changes back to 1.
    # This ensures alternating turns between the two players.
    def change(self):
        if self.player_num == 1:
            self.player_num = 2  # Switch to Player 2
        else:
            self.player_num = 1  # Switch back to Player 1

    # This method is called at the beginning of a player's turn.
    # It prompts the player to press "Enter" to start their turn, displaying a message indicating which player's turn it is.
    def begin_turn(self):
        print("Begin Player", self.player_num, "'s Turn (Press Enter)")  # Inform the player it's their turn
        input()  # Wait for the player to press Enter to start their turn

    # This method is called at the end of a player's turn.
    # It prompts the player to press "Enter" to end their turn, clears the screen, and then switches to the other player.
    def end_turn(self):
        print("End Player", self.player_num, "'s Turn (Press Enter)")  # Inform the player that their turn is ending
        input()  # Wait for the player to press Enter before ending the turn
        clear_screen()  # Clears the console screen to prevent the next player from seeing the previous player's board/actions
        self.change()  # Call the `change()` method to switch to the other player
