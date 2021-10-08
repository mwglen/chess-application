import game
import curses
from piece import Color
from position import Position, InvalidMove
from game import GameData

class LocalGameData(GameData):
    def __init__(self):
        self.white_on_top = True
        self.white = "Player 1"
        self.black = "Player 2"
    

# Starts a new local game
def start(w):

    # Ask the user who is white and black
    white, black = game.player_setup()
    
    # Initialize game data
    gd = LocalGameData()

    while not text_edit(gd.input_str, 10):
        # Refresh the screen
        game.draw(w, gd)

        # Get a character
        c = w.getch()
        
        # Handle linefeeds
        if c == 10:
            # Reset msg
            gd.msg = ""
            s = gd.input_str
            gd.input_str = ""

            ### Parse input string ###
            # Flip if requested
            if s == "flip": gd.white_on_top ^= True
            
            # Exit if requested
            elif s == "exit" or s == "quit": return

            # Parse input string as a move 
            else:
                try:
                    # Attempt to make a move
                    gd.position.move_san(s, gd.curr_turn)

                    # Switch whose turn it is
                    if gd.curr_turn == Color.WHITE:
                        gd.curr_turn = Color.BLACK
                    else: gd.curr_turn = Color.WHITE

                    # Flip board
                    gd.white_on_top ^= True

                except InvalidMove as err:
                     gd.msg = str(err)
