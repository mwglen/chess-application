import curses
import curses.ascii
from position import Position
from board import Board
from pgn_parser import pgn, parser
import time

def main(w):
    # Clear screen
    w.clear()
    curses.curs_set(0)
    curses.start_color()

    # Define colors pairs
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
    
    # Create a new board
    board = Board(w)

    # Set the board's position to be the base position
    board.position = Position.base()
    board.position.raw_move("e2", "e4")
    board.position.raw_move("e7", "e5")
    board.position.raw_move("g1", "f3")
    board.position.raw_move("b8", "c6")
    board.position.raw_move("d2", "d4")
    
    while True:
        # Display the board
        refresh_screen(w, board)

        input_str = ""
        c = ""

        # While not a linefeed
        while c != 10:
            max_y, max_x = w.getmaxyx()
            w.addstr(max_y - 2, 2, f"Enter Move: {input_str}")
            
            # Wait for keypress
            c = w.getch()
       
            # Return if escape
            if c == curses.ascii.ESC: return

            # Handle backspaces
            elif c == curses.ascii.DEL: input_str = input_str[:-1]

            # Ignore tabs
            elif c == curses.ascii.TAB: continue

            # Handle characters
            elif curses.ascii.isascii(chr(c)):
                if len(input_str) < 20: input_str += chr(c)
            
            refresh_screen(w, board)

def refresh_screen(w: curses.window, board: Board):
            # Erase the previous drawing
            w.erase()
            
            # Color the main window
            w.bkgd(" ", curses.color_pair(1))
            w.box("|", "-")
            
            # Add the title
            w.addstr(0, 0, "Chess Application", 
                    curses.color_pair(1))

            # Build and draw the board
            board.setup_graphics(w)
            board.draw()

curses.wrapper(main)
