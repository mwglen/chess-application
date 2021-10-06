from position import Position, InvalidMove
from piece import Color
from enum import Enum, auto
import random
import curses

class Gamemode(Enum):
    VS_COMPUTER = auto()
    LOCAL_GAME = auto()
    THROUGH_SSH = auto()

class GameData:
    def __init__(self, gm: Gamemode):
        # Choose who is white and black
        player1 = random.choice(["Player", "Computer"])
        player2 = "Computer"
        white_on_top = True
        if player2 == player1: 
            player2 = "Player"
            white_on_top = False

        # Set class attributes
        self.white_on_top = white_on_top
        self.player1 = player1
        self.player2 = player2
        self.position: Position = Position.base()
        self.curr_turn = Color.WHITE
        self.input_str = ""
        self.msg = ""

def draw(w, gd):
    
    # Get maximum allowed x and y values
    max_y, max_x = w.getmaxyx()
    
    # Erase the previous drawing
    w.erase()
    
    # Color the main window
    w.bkgd(" ", curses.color_pair(1))
    w.box("|", "-")
    
    # Add the title
    text = "Terminal Chess"
    w.addstr(0, max_x//2 - len(text)//2, text, 
            curses.color_pair(1))
    
    # Add error message
    w.addstr(max_y - 2, max_x - 2 - len(gd.msg),
        gd.msg, curses.color_pair(6))
    
    # List players
    w.addstr(1, 2, f"White: {gd.player1}")
    w.addstr(1, max_x - 2 - len(f"Black: {gd.player2}"), 
        f"Black: {gd.player2}")
   
    # Add prompt
    w.addstr(max_y - 2, 2, f"Enter Move: {gd.input_str}")
    

    # Build and draw the board
    sw = _create_subwindows(w, gd)
    _draw_board(gd, sw)

# Starts a new game vs the computer
# This sets up the graphics windows for the board.
# This must be called anytime the board needs to be resized.
def _create_subwindows(base_window, gd):
    windows = {}
    bs = 6 # The border size
    max_y, max_x = base_window.getmaxyx()
    if ((max_x - bs) / 8)*2 < (max_y - bs)/8:
        width = int((max_x - bs) / 8)
        height = int(width / 2)
    else:
        height = int((max_y - bs)/ 8)
        width = height * 2

    y = int((max_y - height*8)/2)
    x = int((max_x - width*8)/2)

    rows = "12345678"
    cols = "abcdefgh"
    cols = cols[::-1]
    if gd.white_on_top:
        rows = rows[::-1]
        cols = cols[::-1]

    for row in rows:
        for col in cols:
            w = base_window.subwin(height, width, y, x)
            windows[col + row] = w
            x += width
        y += height
        x = int((max_x - width*8)/2)

    return windows

def _draw_board(gd, sw):
    for (i, col) in enumerate("abcdefgh"):
        for row in "12345678":
            # Get the subwindow corresponding to this square
            w = sw[col + row]

            # Get the peice at this square
            piece = gd.position.get(col + row)
            
            # Choose the square's colors
            if (int(row) % 2 == 0) ^ (i % 2 == 0):
                # white text, white background
                w.bkgd(" ", curses.color_pair(2))
                if piece and piece.color == Color.BLACK:
                    # black text, white background
                    w.bkgd(" ", curses.color_pair(3))
            else:
                # white text, black background
                w.bkgd(" ", curses.color_pair(4))
                if piece and piece.color == Color.BLACK:
                    # black text, black background
                    w.bkgd(" ", curses.color_pair(5))
            
            # Draw the piece if needed
            if piece:
                height, width = w.getmaxyx()
                w.addch(int(height/2), int(width/2), 
                    piece.type.as_letter(),curses.A_BOLD)
