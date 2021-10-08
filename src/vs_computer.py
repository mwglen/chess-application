import game
import curses
from piece import Color
from position import Position, InvalidMove
from game import GameData
from menu_functions import edit_text
from constants import *

# Starts a new local game
def start(w):
    
    # Initialize game data
    gd = GameData(w, LOCAL_GAME)

    while True:

        # Refresh the screen
        game.draw(w, gd)

        # Handle linefeeds
        if edit_text(gd.input_str, 10):

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

                except InvalidMove as err:
                     gd.msg = str(err)
