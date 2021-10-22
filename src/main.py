import curses
import curses.ascii
import main_menu
import time
import os

def main(w):
    
    # Clear screen
    w.clear()
    curses.curs_set(0)
    curses.start_color()
    
    ### Define Colors Pairs ###
    # Main Menu Colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    # Chessboard Colors
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
    
    # Error Message During Game
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
    
    # Sub Menu Colors
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)

    # Go to Main Menu
    main_menu.display(w)

os.environ.setdefault('ESCDELAY', '0')
curses.wrapper(main)
