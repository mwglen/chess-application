from position import Position, InvalidMove
from constants import *
import local_game
import vs_computer
import random
import curses
import instructions

# Displays the main menu
def display(w):
   
    curr_sel = 0
    
    while True:
        
        # Draw the menu
        _draw(w, curr_sel)

        # Get inputted character
        c = w.getch()
        
        # Handle linefeeds
        if c == 10:

            # Start selected option
            if curr_sel == 0: vs_computer.start(w)
            elif curr_sel == 1: local_game.start(w)
            elif curr_sel == 2: instructions.display(w)
            elif curr_sel == 3: quit()
        
        # Handle up tabs and arrow keys
        elif (c == curses.KEY_UP and curr_sel > 0): curr_sel -= 1
        elif (c == curses.KEY_DOWN and curr_sel < 3): curr_sel += 1
        elif c == ord('\t'): curr_sel = (curr_sel + 1) % 4

def _draw(w, curr_sel):

    # Erase previous draws
    w.erase();
    
    # Get the size of the window
    max_y, max_x = w.getmaxyx()

    # Color the main window
    w.bkgd(" ", curses.color_pair(MM))
    w.box("|", "-")

    # Add the title
    title = [
        r" _____                   _             _   _____ _                    ",
        r"|_   _|                 (_)           | | /  __ \ |                   ",
        r"  | | ___ _ __ _ __ ___  _ _ __   __ _| | | /  \/ |__   ___  ___ ___  ",
        r"  | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | | |   | '_ \ / _ \/ __/ __| ",
        r"  | |  __/ |  | | | | | | | | | | (_| | | | \__/\ | | |  __/\__ \__ \ ",
        r"  \_/\___|_|  |_| |_| |_|_|_| |_|\__,_|_|  \____/_| |_|\___||___/___/ ",
        r""
    ]
    
    # Used to vertically offset text
    i = -4
    for text in title:
        w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
                curses.color_pair(MM))
        i += 1

    # Add "VS COMPUTER" button
    text = "VS COMPUTER"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(ER if curr_sel == 0 else MM))
    i += 1

    # Add "LOCAL GAME" button
    text = "LOCAL GAME"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(ER if curr_sel == 1 else MM))
    i += 1
    
    # Add "HOW TO PLAY" button
    text = "INSTRUCTIONS"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(ER if curr_sel == 2 else MM))
    i += 1
   
    # Add "QUIT" button
    text = "QUIT"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(ER if curr_sel == 3 else MM))
    i += 1
