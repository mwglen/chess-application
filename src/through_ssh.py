import game
import curses
from piece import Color
from position import Position, InvalidMove
from game import GameData

class SSHGameData(GameData):
    def __init__(self):
        # Choose who is white and black
        white = random.choice(["Player", "Computer"])
        black = "Computer"
        white_on_top = True
        if player2 == player1: 
            player2 = "Player"
            white_on_top = False
        
        # Set class attributes
        self.white_on_top = white_on_top
        self.player1 = player1
        self.player2 = player2

# Starts a new local game
def start(w):
    
    # Initialize game data
    gd = GameData(Gamemode.THROUGH_SSH)

    while True:
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

                except InvalidMove as err:
                     gd.msg = str(err)
   
        # Handle backspaces
        elif c == curses.ascii.DEL: 
            gd.input_str = gd.input_str[:-1]

        # Ignore tabs and new lines
        elif c == curses.ascii.TAB: continue
        elif c == curses.ascii.NL: continue

        # Handle characters
        elif curses.ascii.isascii(chr(c)):
            if len(gd.input_str) < 10: 
                gd.input_str += chr(c)

