import curses
from random import shuffle
from menu_functions import create_subwindow
from constants import *

def start(w, player1, player2) -> (str, str):
    curr_sel = 0 
    white = player1
    black = player2
    sw = create_subwindow(w, 10, 25)
    
    while True:
        
        # Draw the menu
        _draw(sw, curr_sel, white, black)

        # Get inputted character
        c = sw.getch()

        # Handle linefeeds
        if c == 10:

            # If user selected to switch
            if curr_sel == 0:
                white, black = black, white

            # If the user wants to continue
            elif curr_sel == 1: 
                del sw; w.touchwin()
                return white, black

            # If the user wants to return to name selection
            elif curr_sel == 2: 
                del sw; w.touchwin()
                return None, None

        # Handle up arrow key
        elif (c == curses.KEY_UP and curr_sel > 0):
            curr_sel -= 1

        # Handle down arrow key
        elif (c == curses.KEY_DOWN and curr_sel < 3):
            curr_sel += 1

def _draw(sw, curr_sel, white, black):

    # Erase the previous drawing
    sw.erase()

    # Color the sub window
    sw.bkgd(" ", curses.color_pair(SM))
    sw.box("|", "-")

    # Get maximum allowed x and y values
    max_y, max_x = sw.getmaxyx()
    
    text = "Choose Colors"
    sw.addstr(1, max_x//2 - len(text)//2,
        text, curses.color_pair(SM))
    
    text = "White: " + white
    sw.addstr(3, max_x//2 - len(text)//2,
        text, curses.color_pair(SM))
    
    text = "Black: " + black
    sw.addstr(4, max_x//2 - len(text)//2,
        text, curses.color_pair(SM))
    
    text = "Swap"
    sw.addstr(6, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 0 else SM))
    
    text = "Continue"
    sw.addstr(7, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 1 else SM))
    
    text = "Back"
    sw.addstr(8, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 2 else SM))
