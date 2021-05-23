from position import Position
from piece import Color
import random
import curses

class Board():

    # Creates a board with the starting position
    def __init__(self, base_window):
        # Choose who is white and black
        player1 = random.choice(["You", "Computer"])
        player2 = "Computer"
        white_on_top = True
        if player2 == player1: 
            player2 = "You"
            white_on_top = False
        
        self.white_on_top = white_on_top
        self.player1 = player1
        self.player2 = player2
        self.position: Position = Position.base()
        self.setup_graphics(base_window) # Must be called last
        
    # This sets up the graphics windows for the board.
    # This must be called anytime the board needs to be resized.
    def setup_graphics(self, base_window):
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
        if self.white_on_top:
            rows = rows[::-1]
            cols = cols[::-1]

        for row in rows:
            for col in cols:
                w = base_window.subwin(height, width, y, x)
                windows[col + row] = w
                x += width
            y += height
            x = int((max_x - width*8)/2)
        self.windows = windows

    def draw(self):
        for (i, col) in enumerate("abcdefgh"):
            for row in "12345678":
                # Get the window corresponding to this square
                w = self.windows[col + row]

                # Get the peice at this square
                piece = self.position.get(col + row)
                
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
