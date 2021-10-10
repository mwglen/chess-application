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
    try: gd = GameData(w, VS_COMPUTER)
    except ReturnToMainMenu: return

    while True:

        # Refresh the screen
        game.draw(w, gd)
        gd.input_str, is_linefeed = edit_text(w, gd.input_str, 10);
        if is_linefeed:
            # Reset msg
            gd.msg = ""
            s = gd.input_str
            gd.input_str = ""

            ### Parse input string ###
            # Flip if requested
            if s == "flip": gd.white_on_top ^= True
            
            # Exit if requested
            elif s == "exit" or s == "quit": return

            else:
                try:
                    # Attempt to make a move
                    gd.position.move_san(s, gd.curr_turn)

                    # Switch whose turn it is
                    if gd.curr_turn == Color.WHITE:
                        gd.curr_turn = Color.BLACK
                    else: gd.curr_turn = Color.WHITE
                    gd.white_on_top ^= True

                except InvalidMove as err:
                    gd.msg = str(err)
