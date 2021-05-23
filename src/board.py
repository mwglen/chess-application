from position import Position
from piece import Color
import random
import curses
class Board:
    # Creates a new game.
    def __init__(self, w):
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
        self.msg = ""
        self.input_str = ""
        
        self.setup_graphics(w)
        
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

        self.base_window = base_window
        self.windows = windows

    def _draw(self):
        w = self.base_window

        # Erase the previous drawing
        w.erase()
        
        # Color the main window
        w.bkgd(" ", curses.color_pair(1))
        w.box("|", "-")
        
        # Add the title
        w.addstr(0, 0, "Chess Application", 
                curses.color_pair(1))
        
        # Add error message
        max_y, max_x = w.getmaxyx()
        w.addstr(max_y - 2, max_x - 2 - len(self.msg),
            self.msg, curses.color_pair(6))
        
        # List players
        w.addstr(1, 2, f"White: {self.player1}")
        w.addstr(1, max_x - 2 - len(f"Black: {self.player2}"), 
            f"Black: {self.player2}")
       
        # Add prompt
        w.addstr(max_y - 2, 2, f"Enter Move: {self.input_str}")
        

        # Build and draw the board
        self.setup_graphics(w)
        self._draw_board()

    def _draw_board(self):
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
    def play(self):
        while True:
            self.input_str = ""
            # Refresh the screen
            self._draw()

            # While not a linefeed
            while (c := self.base_window.getch()) != 10:
           
                # Return if escape
                if c == curses.ascii.ESC: return

                # Handle backspaces
                elif c == curses.ascii.DEL: 
                    self.input_str = self.input_str[:-1]

                # Ignore tabs and new lines
                elif c == curses.ascii.TAB: continue
                elif c == curses.ascii.NL: continue

                # Handle characters
                elif curses.ascii.isascii(chr(c)):
                    if len(self.input_str) < 10: 
                        self.input_str += chr(c)
                # Refresh the screen
                self._draw()

            self.msg = self._parse_input()
    
    def _parse_input(self) -> str:
        s = self.input_str
        if s == "flip":
            self.white_on_top ^= True
        elif s == "exit" or s == "quit":
            quit()
        else:
            return f"Error: \"{s}\" is not a valid move"
        return ""
    
