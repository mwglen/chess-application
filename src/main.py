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
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
    
    # Create a new board
    b = Board(w)

    # Set the board's position to be the base position
    b.position = Position.base()
    b.position.raw_move("e2", "e4")
    b.position.raw_move("e7", "e5")
    b.position.raw_move("g1", "f3")
    b.position.raw_move("b8", "c6")
    b.position.raw_move("d2", "d4")
    
    # Set up a blank error message
    msg = ""
    while True:
        input_str = ""
        c = ""

        # While not a linefeed
        while c != 10:
            # Refresh the screen
            draw_board(w, b)

            # Add error message
            max_y, max_x = w.getmaxyx()
            w.addstr(max_y - 2, max_x - 2 - len(msg), msg, 
                curses.color_pair(6))
            
            # List players
            w.addstr(1, 2, f"White: {b.player1}")
            w.addstr(1, max_x - 2 - len(f"Black: {b.player2}"), 
                f"Black: {b.player2}")
           
            # Add prompt
            w.addstr(max_y - 2, 2, f"Enter Move: {input_str}")
            
            # Wait for keypress
            c = w.getch()
       
            # Return if escape
            if c == curses.ascii.ESC: return

            # Handle backspaces
            elif c == curses.ascii.DEL: input_str = input_str[:-1]

            # Ignore tabs and new lines
            elif c == curses.ascii.TAB: continue
            elif c == curses.ascii.NL: continue

            # Handle characters
            elif curses.ascii.isascii(chr(c)):
                if len(input_str) < 10: input_str += chr(c)
            
        msg = parse_input(w, b, input_str)

def parse_input(w: curses.window, b: Board, string: str) -> str:
    if string == "flip":
        b.white_on_top ^= True
    elif string == "exit":
        quit()
    else:
        return f"Error: \"{string}\" is not a valid move"
    return ""
    


def draw_board(w: curses.window, b: Board):
            # Erase the previous drawing
            w.erase()
            
            # Color the main window
            w.bkgd(" ", curses.color_pair(1))
            w.box("|", "-")
            
            # Add the title
            w.addstr(0, 0, "Chess Application", 
                    curses.color_pair(1))

            # Build and draw the board
            b.setup_graphics(w)
            b.draw()

curses.wrapper(main)
